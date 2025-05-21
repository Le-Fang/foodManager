import React, { useState, useEffect } from 'react';
import './HomePage.css';
import config from './config';

const HomePage = () => {
    const [foodItems, setFoodItems] = useState([]);
    const [newItem, setNewItem] = useState({ name: '', quantity: '', expiration_date: '' });
    const [generatedText, setGeneratedText] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    // Fetch food items on component mount
    useEffect(() => {
        fetchFoodItems();
    }, []);

    // Simulated fetch function for food items
    const fetchFoodItems = async () => {
        const endpoint = `${config.BASE_URL}/food`;
        try {
            const response = await fetch(endpoint, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                setFoodItems(data.foods);
            } else if (response.status === 401) {
                // Handle unauthorized access
                console.error('Unauthorized access. Please log in again.');
            } else {
                console.error('Failed to fetch food items:', response.statusText);
            }
        } catch (error) {
            console.error('Error fetching food items:', error);
        }
    };

    // Handle changes to the new item form
    const handleNewItemChange = (e) => {
        const { name, value } = e.target;
        setNewItem({ ...newItem, [name]: value });
    };

    // Add a new food item
    const handleAddItem = async (e) => {
        e.preventDefault();
        if (!newItem.name || !newItem.quantity || !newItem.expiration_date) return;
        
        const endpoint = `${config.BASE_URL}/food`;
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify(newItem),
            });
            
            const data = await response.json();
            if (response.status == 201) {
                const addedItem = data.new_item;
                setFoodItems([...foodItems, addedItem]);
                setNewItem({ name: '', quantity: '', expiration_date: '' });
                console.log('Food item added successfully:', addedItem);
            } else {
                console.error('Failed to add food item:', data.message, data.errors);
            }
        } catch (error) {
            console.error('Error adding food item:', error);
        }
    };

    // handle delete food item
    const handleDeleteItem = async (id) => {
        const endpoint = `${config.BASE_URL}/food`;
        try {
            const response = await fetch(endpoint, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify({"food_id": id}),
            });
            
            if (response.ok) {
                // Remove the item from state
                setFoodItems(foodItems.filter(item => item.id !== id));
            }
        } catch (error) {
            console.error('Error deleting food item:', error);
        }
    };

    // handle quantity change
    const handleQuantityChange = async (id, newQuantity) => {
        if (newQuantity <= 0) {
            // If quantity is zero or negative, delete the item
            handleDeleteItem(id);
            return;
        }
        
        const endpoint = `${config.BASE_URL}/food`;
        try {
            const target_item = foodItems.find(item => item.id === id);
            const newData = {"food_id": id, "quantity": newQuantity, "expiration_date": new Date(target_item.expiration_date).toISOString().split('T')[0], "name": target_item.name};
            const response = await fetch(endpoint, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
                body: JSON.stringify(newData),
            });

            
            if (response.ok) {
                // Update the item quantity in state
                setFoodItems(foodItems.map(item => 
                    item.id === id ? { ...item, quantity: newQuantity } : item
                ));
            }
        } catch (error) {
            console.error('Error updating food item quantity:', error);
        }
    };

    // Generate text from backend
    const handleGenerate = async () => {
        setIsLoading(true);
        
        // Replace with actual API call
        try {
            // Simulated backend response
            const response = await new Promise(resolve =>
                setTimeout(() => resolve({
                    ok: true,
                    json: () => Promise.resolve({
                        text: "Here's a meal plan based on your food items:\n" +
                                 "- Apple pie using your 5 apples\n" +
                                 "- French toast using milk and bread\n" +
                                 "Consider consuming bread soon as it expires in a few days."
                    })
                }), 1000)
            );
            
            if (response.ok) {
                const data = await response.json();
                setGeneratedText(data.text);
            }
        } catch (error) {
            console.error('Error generating text:', error);
        } finally {
            setIsLoading(false);
        }
    };
    
    // Calculate days until expiration
    const getDaysUntilExpiration = (expirationDate) => {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const expDate = new Date(expirationDate);
        const diffTime = expDate - today;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays;
    };

    // Get expiration indicator based on days until expiration
    const getExpirationIndicator = (expirationDate) => {
        const daysLeft = getDaysUntilExpiration(expirationDate);
        
        if (daysLeft < 0) {
            return { text: "Expired!", className: "expired-indicator" };
        } else if (daysLeft <= 3) {
            return { text: "Soon!", className: "soon-indicator" };
        } else if (daysLeft <= 7) {
            return { text: "This week", className: "week-indicator" };
        } else {
            return { text: "Safe", className: "safe-indicator" };
        }
    };

    // Sort food items by expiration date
    const sortByExpirationDate = () => {
        const sortedItems = [...foodItems].sort((a, b) => 
            new Date(a.expiration_date) - new Date(b.expiration_date)
        );
        setFoodItems(sortedItems);
    };

    // Sort items when they are loaded
    useEffect(() => {
        if (foodItems.length > 0) {
            sortByExpirationDate();
        }
    }, [foodItems.length]);

    return (
        <div className="home-container">
            <h1>Food Manager</h1>
            
            <div className="main-content">
                <div className="food-list-container">
                    <h2>Inventory</h2>
                    <div className="scrollable-table">
                        <table className="food-table">
                            <thead>
                                <tr>
                                    <th>Item Name</th>
                                    <th>Quantity</th>
                                    <th>Expiration Date</th>
                                    <th>Status</th>
                                    <th>Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {foodItems.map((item) => {
                                    const indicator = getExpirationIndicator(item.expiration_date);
                                    return (
                                        <tr key={item.id}>
                                            <td>{item.name}</td>
                                            <td>
                                                <div className="quantity-controls">
                                                    <button 
                                                        className="quantity-btn" 
                                                        onClick={() => handleQuantityChange(item.id, parseInt(item.quantity) - 1)}
                                                    >
                                                        -
                                                    </button>
                                                    {item.quantity}
                                                    <button 
                                                        className="quantity-btn" 
                                                        onClick={() => handleQuantityChange(item.id, parseInt(item.quantity) + 1)}
                                                    >
                                                        +
                                                    </button>
                                                </div>
                                            </td>
                                            <td>{item.expiration_date}</td>
                                            <td>
                                                <span className={indicator.className}>
                                                    {indicator.text}
                                                </span>
                                            </td>
                                            <td>
                                                <button 
                                                    className="delete-btn" 
                                                    onClick={() => handleDeleteItem(item.id)}
                                                >
                                                    Delete
                                                </button>
                                            </td>
                                        </tr>
                                    );
                                })}
                                <tr>
                                    <td>
                                        <input
                                            type="text"
                                            name="name"
                                            value={newItem.name}
                                            onChange={handleNewItemChange}
                                            placeholder="Item name"
                                        />
                                    </td>
                                    <td>
                                        <input
                                            type="text"
                                            name="quantity"
                                            value={newItem.quantity}
                                            onChange={handleNewItemChange}
                                            placeholder="Quantity"
                                        />
                                    </td>
                                    <td colSpan="3">
                                        <input
                                            type="date"
                                            name="expiration_date"
                                            value={newItem.expiration_date}
                                            onChange={handleNewItemChange}
                                        />
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <button className="add-item-btn" onClick={handleAddItem}>Add Item</button>
                </div>

                <div className="chatbox-container">
                    <h2>Meal Suggestions</h2>
                    <button 
                        className="generate-btn" 
                        onClick={handleGenerate}
                        disabled={isLoading}
                    >
                        {isLoading ? 'Generating...' : 'Generate Suggestions'}
                    </button>
                    {generatedText && (
                        <div className="generated-text-box">
                            {generatedText.split('\n').map((line, index) => (
                                <p key={index}>{line}</p>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default HomePage;