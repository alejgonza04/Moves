import React, {useState} from 'react'
import './LoginSignup.css'

// Import Images from Assets such as app icon, username icon, email icon, password icon //
import title from '../Assets/logo.png'

const LoginSignup = () => {

  // Utilize this video as a resources to create login page:
  const [action,setAction] = useState("Login");
  return (
    <div className='container'>
      <div className='header'>
        <img src={title} alt="App Logo" className='logo'/>
        <div className='underline'></div>
        </div>
      <div className='inputs'>
        {action==="Login"?<div></div>: <div className='input'>
          <input type='text' placeholder='Name'/>
        </div>}
        <div className='input'>
          <input type='email' placeholder='Email'/>
        </div>
        <div className='input'>
          <input type='password' placeholder='Password'/>
        </div>
      </div>
      {action==="Sign Up"?<div></div>:  <div className="forgot-password">Lost Password? <span>Click Here!</span></div>}
      <div className="submit-container">
        <div className={action==="Login"?"submit gray":"submit"} onClick={()=>{setAction("Sign Up")}}>Sign Up</div>
        <div className={action==="Sign Up"?"submit gray":"submit"} onClick={()=>{setAction("Login")}}>Login</div>
      </div>
    </div>
      
  );
};

export default LoginSignup