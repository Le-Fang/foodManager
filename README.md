# Food Manager

A personal project built using Flask, React, and LangGraph for ingredient management, powered by a RAG agent for recipe generations.

## Tech Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Flask-JWT-Extended**: JWT authentication
- **Redis**: Session storage
- **LangGraph**: AI agent framework
- **OpenAI API**: AI-powered recipe generation

### Frontend
- **React**: Frontend framework
- **Vite**: Build tool and development server

### Database
- **SQLite**: Local database (development)
- **Redis**: Session and caching layer


## Features

### 🥘 Inventory Management
- **Add Food Items**: Add food items with name, quantity, and expiration date
- **View Inventory**: Display all food items in a sortable table format
- **Update Quantities**: Modify food item quantities directly from the interface
- **Delete Items**: Remove food items from your inventory
- **Expiration Tracking**: Visual indicators for items expiring soon (red for expired, yellow for this week, green for safe)

### 🤖 AI-Powered Recipe Suggestions
- **Smart Recipe Generation**: Get meal suggestions based on your current inventory
- **RAG Agent Integration**: Uses LangGraph and OpenAI API for intelligent recipe recommendations
- **Interactive Chat Interface**: Clean chatbox UI for recipe suggestions

### 🔐 User Authentication
- **Secure Login/Registration**: JWT-based authentication system
- **Session Management**: Persistent login sessions with Redis backend

### 📱 Modern Web Interface
- **Responsive Design**: Clean, modern React frontend built with Vite
- **Real-time Updates**: Dynamic inventory updates without page refresh
- **Intuitive UX**: Easy-to-use forms and interactive elements
- **Loading States**: Visual feedback during API operations

### ⚡ Technical Features
- **Rate Limiting**: API endpoints protected with rate limiting
- **RESTful API**: Well-structured backend API with proper HTTP status codes
- **Database Integration**: SQLite database with SQLAlchemy ORM
- **Form Validation**: Client and server-side validation
- **Error Handling**: Comprehensive error handling and user feedback
