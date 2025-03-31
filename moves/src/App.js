import React from "react";
// import LoginSignup from "./Components/LoginSignup/LoginSignup";
// import CloudAI from "./Components/CloudAI/CloudAI";
//import CloudAI from "./Components/Homepage/Homepage";
import Homepage from "./Components/Homepage/Homepage";
//import LoginSignup from "./Components/LoginSignup/LoginSignup";

function App() {
  // const [loggedIn, setLoggedIn] = useState(false);

  return (
    <Homepage />

    /* {loggedIn ? (
        <Homepage />
      ) : (
        <LoginSignup onLoginSuccess={() => setLoggedIn(true)} />