import React, { useState } from 'react';
import './LoginSignup.css';
import title from '../Assets/logo.png';

const LoginSignup = ({ onLoginSuccess = () => {} }) => {
  const [action, setAction] = useState("Login");
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async () => {
    const endpoint = action === "Sign Up" ? "signup" : "login";

    console.log(`${action} attempt:`, {
      username: name,
      email: email,
      password: password
    });

    try {
      const res = await fetch(`http://127.0.0.1:5555/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username: name,
          email: email,
          password: password
        })
      });

      const data = await res.json();
      console.log(`${action} response:`, data.message);

      if (res.ok) {
        alert(data.message);
        onLoginSuccess(); // call the prop function on success
      } else {
        alert(`${action} failed: ${data.message}`);
      }
    } catch (err) {
      console.error(`${action} request failed:`, err);
      alert(`${action} failed. Please try again.`);
    }
  };

  return (
    <div className='login-page-background'>
      <div className='container'>
        <div className='header'>
          <img src={title} alt="App Logo" className='logo' />
          <div className='underline'></div>
        </div>

        <div className='inputs'>
          {action === "Sign Up" && (
            <div className='input'>
              <input
                type='text'
                placeholder='Name'
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
          )}
          <div className='input'>
            <input
              type='email'
              placeholder='Email'
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className='input'>
            <input
              type='password'
              placeholder='Password'
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
        </div>

        {action === "Login" && (
          <div className="forgot-password">
            Lost Password? <span>Click Here!</span>
          </div>
        )}

        <div className="submit-container">
          <div
            className={action === "Login" ? "submit gray" : "submit"}
            onClick={() => setAction("Sign Up")}
          >
            Sign Up
          </div>
          <div
            className={action === "Sign Up" ? "submit gray" : "submit"}
            onClick={() => setAction("Login")}
          >
            Login
          </div>
        </div>

        <div className="submit submit-main" onClick={handleSubmit}>
          Submit
        </div>
      </div>
    </div>
  );
};

export default LoginSignup;
