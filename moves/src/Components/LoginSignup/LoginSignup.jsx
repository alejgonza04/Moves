import React from 'react'
import './LoginSignup.css'

// Import Images from Assets such as app icon, username icon, email icon, password icon //

const LoginSignup = () => {
  return (
    <div className='container'>
      <div className='header'>
        <div className='text'>Moves</div>
        <div className='underline'></div>
      </div>
      <div className='inputs'>
        <div className='input'>
          <input type='text' placeholder='Name'/>
        </div>
        <div className='input'>
          <input type='email' placeholder='Email Id'/>
        </div>
        <div className='input'>
          <input type='password' placeholder='Password'/>
        </div>
      </div>

      <div className="forgot-password">Lost Password? <span>Click Here!</span></div>
      <div className="submit-container">
        <div className="submit">Sign Up</div>
        <div className="submit">Login</div>
      </div>
    </div>
      
  );
};

export default LoginSignup
