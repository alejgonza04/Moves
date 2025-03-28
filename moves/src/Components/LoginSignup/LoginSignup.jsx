import React, { useState } from 'react';
import './LoginSignup.css';
import title from '../Assets/logo.png';

const LoginSignup = () => {
  const [action, setAction] = useState("Login");
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async () => {
    if (action === "Sign Up") {
      console.log("Signing up...");

      try {
        const res = await fetch("http://127.0.0.1:5555/signup", {
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
        console.log("Signup response:", data.message);
        alert(data.message);
      } catch (err) {
        console.error("Signup failed:", err);
        alert("Signup failed. Please try again.");
      }
    } else {
      console.log("Logging in...");
      // TODO: Add login functionality here
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

      {action === "Sign Up" ? null : (
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
  );
};

export default LoginSignup;
