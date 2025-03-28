import React, { useState } from 'react';
import './LoginSignup.css';
import title from '../Assets/logo.png';

const LoginSignup = () => {
  const [action, setAction] = useState("Login");

  const handleSubmit = () => {
    if (action === "Login") {
      console.log("Logging in...");
      // TODO: Call login API or function here
    } else {
      console.log("Signing up...");
      // TODO: Call signup API or function here
    }
  };

  return (
    <div className='container'>
      <div className='header'>
        <img src={title} alt="App Logo" className='logo' />
        <div className='underline'></div>
      </div>

      <div className='inputs'>
        {action === "Login" ? null : (
          <div className='input'>
            <input type='text' placeholder='Name' />
          </div>
        )}
        <div className='input'>
          <input type='email' placeholder='Email' />
        </div>
        <div className='input'>
          <input type='password' placeholder='Password' />
        </div>
      </div>

      {action === "Sign Up" ? null : (
        <div className="forgot-password">
          Lost Password? <span>Click Here!</span>
        </div>
      )}

      <div className="submit-container">
        <div className={action === "Login" ? "submit gray" : "submit"} onClick={() => setAction("Sign Up")}>
          Sign Up
        </div>
        <div className={action === "Sign Up" ? "submit gray" : "submit"} onClick={() => setAction("Login")}>
          Login
        </div>
      </div>

      {/* ✅ Submit button here */}
      <div className="submit submit-main" onClick={handleSubmit}>
        Submit
      </div>
    </div>
  );
};

export default LoginSignup;
