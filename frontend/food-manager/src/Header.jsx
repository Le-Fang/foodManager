import React from 'react';
import './Header.css';
import { Link, useNavigate } from 'react-router-dom';

const Header = ({isLoggedIn, username, onLogout}) => {
    const navigate = useNavigate();
    return (
        <header>
            <h1 className="title">Food Manager</h1>
            <nav>
                <ul className="nav-list">
                    {isLoggedIn ? (
                        <>
                            <li className="nav-item"><span>Welcome, {username}!</span></li>
                            <li className="nav-item"><button onClick={() => navigate("/home")} className="button">Home</button></li>
                            <li className="nav-item"><button onClick={() => navigate("/about")} className="button">About</button></li>
                            <li className="nav-item"><button onClick={() => onLogout(navigate)} className="button">Logout</button></li>
                        </>
                    ) : (
                        <>
                            <li className="nav-item"><Link to="/about">About</Link></li>
                            <li className="nav-item"><Link to="/">Login</Link></li>
                        </>
                    )
                    }
                </ul>
            </nav>
        </header>
    );
};

export default Header;