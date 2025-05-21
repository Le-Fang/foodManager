import React from 'react';
import { Link } from 'react-router-dom';
import './ErrorPage.css';

const ErrorPage = ({ statusCode, message }) => {
    // Set default values if not provided
    const errorCode = statusCode || '404';
    const errorMessage = message || 'Page not found';

    return (
        <div className="error-container">
            <div className="error-content">
                <h1>Error {errorCode}</h1>
                <p>{errorMessage}</p>
                <p>Something went wrong. Please try again or return to the home page.</p>
                <Link to="/" className="home-link">Go Home</Link>
            </div>
        </div>
    );
};

export default ErrorPage;