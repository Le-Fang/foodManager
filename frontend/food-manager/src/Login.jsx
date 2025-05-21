import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';
import config from './config';
import { useEffect } from 'react';

const Login = ({ onLogin }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData, // keep other fields unchanged
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = isRegistering
      ? `${config.BASE_URL}/register`
      : `${config.BASE_URL}/login`;
      
      const payload = {
        username: formData.username,
        password: formData.password
      };
      
      if (isRegistering) {
        payload.email = formData.email;
      }

      // This will be replaced with actual API call
      // simulate API response
      // console.log(`Attempting to ${isRegistering ? 'register' : 'login'} with:`, payload);
      
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || 'Authentication failed');
      }
      
      if (isRegistering) {
        alert('Registration successful! Please login.');
        setIsRegistering(false);
        setFormData({
          ...formData,
          email: ''
        });
      } else {
        // Call the parent component's onLogin handler with user info
        onLogin(
          formData.username,
          data.access_token,
          data.refresh_token,
          navigate
        );
      }
      
    } catch (err) {
      setError(err.message || 'An error occurred during authentication');
      console.error('Authentication error:', err);
    } finally {
      setLoading(false);
    }
  };

  const toggleAuthMode = () => {
    setIsRegistering(!isRegistering);
    setError('');
  };

  // Check if user is already logged in
  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      navigate('/home');  // Redirect to home page
    }
  }, [navigate]);

  return (
    <div className="auth-container">
      <h2>{isRegistering ? 'Create Account' : 'Login'}</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit} className="auth-form">
        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        
        {isRegistering && (
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
        )}
        
        <button type="submit" disabled={loading} className="auth-button">
          {loading ? 'Processing...' : isRegistering ? 'Register' : 'Login'}
        </button>
      </form>
      
      <div className="auth-switch">
        {isRegistering ? (
          <p>
            Already have an account?{" "}
            <button onClick={toggleAuthMode} className="text-button">
              Login
            </button>
          </p>
        ) : (
          <p>
            Don't have an account?{" "}
            <button onClick={toggleAuthMode} className="text-button">
              Register
            </button>
          </p>
        )}
      </div>
    </div>
  );
};

export default Login;