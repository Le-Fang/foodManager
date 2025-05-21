import './App.css'
import Login from './Login'
import Header from './Header'
import About from './About'
import ErrorPage from './ErrorPage'
import HomePage from './HomePage'
import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');

  const handleLogin = (username, access_token, refresh_token, navigate) => {
    setIsLoggedIn(true)
    setUsername(username)
    localStorage.setItem('username', username);
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    // navigate to the about page after login
    navigate('/home')
  };
  const handleLogout = (navigate) => {
    setIsLoggedIn(false)
    setUsername('')
    localStorage.removeItem('username');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    // navigate to the login page after logout
    navigate('/')
  };

  // Check if user is already logged in when the app loads
  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setIsLoggedIn(true);
      setUsername(storedUsername);
    }
  }, []);

  return (
    <Router>
      <Header isLoggedIn={isLoggedIn} username={username} onLogout={handleLogout}/>
      <Routes>
        <Route path="/" element={<Login onLogin={handleLogin}/>} />
        <Route path="/about" element={<About />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="*" element={<ErrorPage />} />
      </Routes>
    </Router>
  );
};

export default App
