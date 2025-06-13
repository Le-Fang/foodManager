from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from typing_extensions import TypedDict, Literal
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
import numpy as np
from pathlib import Path

class RecipeAgent:
    """
    A class to generate recipes based on user-provided ingredients.
    This class uses a state graph to manage the recipe generation process,
    including retrieval of source material, recipe generation, and validation.
    It utilizes LangChain's vector store for similarity search and OpenAI's LLM for recipe generation.
    """

    def build_graph(self):
        "build the state graph for recipe generation"

        class State(TypedDict):
            recipe: str # recipe provided to the users
            ingredients: list[str] # ingredients provided by the user
            source: str # retrieved source
            source_url: str # URL of the source
            is_recipe_valid: bool # whether the recipe is valid or not
            recipe_feedback: str # feedback on the generated recipe
        
        class RecipeCheck(BaseModel):
            is_valid: bool = Field(..., description="Indicates if the recipe is valid")
            feedback: str = Field(..., description="feedback about the recipe validity")
        
        def retrieve(state: State):
            """Retrieve a recipe based on the provided state."""
            query = f"Ingredients: {', '.join(state['ingredients'])}"
            results = self.vector_store.similarity_search_with_score(query, k=10)
            if results:
                # use softmax to add some randomness to the selection
                scores = np.array([score for _, score in results])
                scores = np.exp(scores - np.max(scores))
                scores /= np.sum(scores)
                selected_index = np.random.choice(len(results), p=scores)
                doc, _ = results[selected_index]

                state['source'] = doc.page_content
                state['source_url'] = doc.metadata.get('source_url', 'Unknown')
            else:
                state['source'] = 'No source found'
                state['source_url'] = 'No URL found'
        
            return state
        
        def generate_recipe(state: State):
            """Generate a recipe based on the retrieved source."""
            if state.get('recipe_feedback'):
                prompt = f"""You are an expert chef tasked with improving a recipe based on specific feedback.

                    **ORIGINAL RECIPE:**
                    {state['recipe']}

                    **FEEDBACK TO ADDRESS:**
                    {state['recipe_feedback']}

                    **INSTRUCTIONS:**
                    - Fix only the issues mentioned in the feedback
                    - Maintain the original recipe's style and structure where possible
                    - Ensure all measurements, temperatures, and cooking times are accurate
                    - Keep instructions clear and easy to follow
                    - If ingredients need to be added or removed, explain why

                    Please provide the corrected recipe that addresses all the feedback points."""
        
                res = self.llm.invoke(prompt)
            else:
                prompt = f"""You are a professional chef creating a recipe based on source material and available ingredients.

                    **SOURCE MATERIAL:**
                    {state['source']}

                    **AVAILABLE INGREDIENTS:**
                    {', '.join(state['ingredients'])}

                    **REQUIREMENTS:**
                    - Create a complete, practical recipe using the available ingredients
                    - Include exact measurements and cooking times
                    - Provide clear, step-by-step instructions
                    - Be concise and focused on the ingredients provided
                    - Ensure the recipe is safe and achievable for home cooks
                    - If the source material contains multiple recipes, choose the most suitable one
                    - If ingredients are missing from the source, suggest reasonable substitutions
                    - If the source is not suitable for a recipe, create a new one based on the ingredients
                    - Do not include any personal opinions or unnecessary information

                    **FORMAT:**
                    Please structure the recipe with:
                    1. Recipe title
                    2. Prep time and cook time
                    3. Ingredients list with measurements
                    4. Step-by-step instructions
                    5. Any helpful tips or notes

                    Generate the recipe now."""
                res = self.llm.invoke(prompt)
            state['recipe'] = res.content
            return state
        
        def validate_recipe(state: State):
            """Validate the generated recipe."""
            prompt = f"""You are a professional chef and recipe validator. Your task is to evaluate the quality and correctness of a recipe.

                Please analyze the following recipe and determine if it is valid, safe, and well-structured.

                **RECIPE TO VALIDATE:**
                {state['recipe']}

                **ORIGINAL SOURCE DOCUMENTS:**
                {state['source']}

                **EVALUATION CRITERIA:**
                1. **Safety**: Are the cooking temperatures, times, and methods safe?
                2. **Completeness**: Does it include all necessary ingredients, quantities, and steps?
                3. **Clarity**: Are the instructions clear and easy to follow?
                4. **Accuracy**: Do the cooking methods and times make sense for the ingredients?
                5. **Consistency**: Does the recipe match the source material appropriately?

                **REQUIREMENTS:**
                - If the recipe is valid, mark it as valid with minimal feedback
                - If invalid, provide specific, actionable feedback on what needs to be fixed
                - Focus on critical issues that would prevent successful cooking
                - Be concise but thorough in your feedback

                Evaluate the recipe now."""
            llm_validator = self.llm.with_structured_output(RecipeCheck)
            res = llm_validator.invoke(prompt)
            state['is_recipe_valid'] = res.is_valid
            state['recipe_feedback'] = res.feedback
            return state

        def route_recipe(state: State):
            """Route the recipe based on its validity."""
            if state.get('is_recipe_valid', False):
                return True
            else:
                return False
        
        graph_builder = StateGraph(State)
        graph_builder.add_node("retrieve", retrieve)
        graph_builder.add_node("generate_recipe", generate_recipe)
        graph_builder.add_node("validate_recipe", validate_recipe)
        
        graph_builder.add_edge(START, "retrieve")
        graph_builder.add_edge("retrieve", "generate_recipe")
        graph_builder.add_edge("generate_recipe", "validate_recipe")
        graph_builder.add_conditional_edges(
            "validate_recipe",
            route_recipe,
            {
                True: END,
                False: "generate_recipe"
            }
        )

        graph = graph_builder.compile()
        return graph


    def __init__(self, index_name="faiss_recipes_index"):
        self.index_name = index_name
        self.embeddings = OpenAIEmbeddings()

        # Load the FAISS index from the same directory as this script
        script_dir = Path(__file__).parent
        index_path = script_dir  /  index_name
        if not Path(index_path).exists():
            raise FileNotFoundError(f"Index file {index_name} does not exist. Please run the scraper first.")
        
        self.vector_store = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
        self.llm = init_chat_model("openai:gpt-4.1", temperature=0.0)
        self.graph = self.build_graph()
    
    def generate_recipe(self, foods) -> dict:
        """Generate a recipe based on the provided ingredients."""
        ingredients = [food['name'] for food in foods if food['quantity'] > 0]
        if not ingredients:
            return {"recipe": "No valid ingredients provided."}
        state = {
            "ingredients": ingredients
        }
        
        # invoke the graph
        final_state = self.graph.invoke(state)
        
        return final_state
    
    


    
