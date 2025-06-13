import requests
from bs4 import BeautifulSoup
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from pathlib import Path

class DocumentScraper:
    """
    A class to scrape content from web pages and store it in a FAISS index.
    This class uses BeautifulSoup for scraping, LangChain's text splitter for chunking,
    and OpenAI embeddings for vectorization.
    """

    def __init__(self):
        self.docs = []
        self.text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=250)
        self.embeddings = OpenAIEmbeddings()
        self.script_dir = Path(__file__).parent

    def scrape(self, url: str):
        """Scrape content from a given URL and append it in self.docs."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')
            self.soup_clean_up(soup)
            main_content = soup.find(id="structured-project-content_1-0")
            if main_content:
                text = main_content.get_text(separator='\n', strip=True)
            elif soup.find('article'):
                text = soup.find('article').get_text(separator='\n', strip=True)
            elif soup.find('main'):
                text = soup.find('main').get_text(separator='\n', strip=True)
            elif soup.find('body'):
                text = soup.find('body').get_text(separator='\n', strip=True)
            else:
                # Fallback to the entire page content if main content is not found
                text = soup.get_text(separator='\n', strip=True)
            doc = Document(page_content=text, metadata={"source_url": url})

            split_docs = self.text_splitter.split_documents([doc])
            self.docs.extend(split_docs)
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
        except Exception as e:
            print(f"Error processing {url}: {e}")
        
        return
    
    def soup_clean_up(self, soup):
        """Clean up the BeautifulSoup object by removing unwanted elements."""
        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()

        # Remove Wikipedia-specific clutter
        for element in soup.find_all(class_=['navbox', 'infobox', 'sidebar', 'metadata']):
            element.decompose()

        # Remove elements with common unwanted IDs
        for element in soup.find_all(id=['toc', 'catlinks', 'external-links', 'references']):
            element.decompose()

        # Remove citation links like [1], [2], etc.
        for sup in soup.find_all('sup', class_='reference'):
            sup.decompose()

        return

    def store_to_index(self, index_name="faiss_recipes_index"):
        """Store the scraped content in a FAISS index."""
        if len(self.docs) == 0:
            print("No documents to store in the index.")
            return
        try:
            vector_store = FAISS.from_documents(self.docs, self.embeddings)
            vector_store.save_local(self.script_dir / index_name)
            self.docs = []
        except Exception as e:
            print(f"Error storing to index: {e}")
        return


    def append_to_index(self, index_name="faiss_recipes_index"):
        """Append the scraped content to an existing FAISS index.
        
        Args:
            index_name: Name of the index to append to
            
        Returns:
            bool: True if successful, False otherwise
        """
        if len(self.docs) == 0:
            print("No documents to append to the index.")
            return True
        
        try:
            vector_store = FAISS.load_local(self.script_dir / index_name, self.embeddings, allow_dangerous_deserialization=True)
            
            vector_store.add_documents(self.docs)
            
            vector_store.save_local(self.script_dir / index_name)
            self.docs = []  # Clear the docs after appending
            return True
        except Exception as e:
            print(f"Error appending to index: {e}")
            return False

    

