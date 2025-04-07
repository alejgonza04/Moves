import React from "react";
// import LoginSignup from "./Components/LoginSignup/LoginSignup";
import CloudAI from "./Components/CloudAI/CloudAI";

function App() {
  // const [loggedIn, setLoggedIn] = useState(false);

  return (
    <div>
      {/* {loggedIn ? (
        <Homepage />
      ) : (
        <LoginSignup onLoginSuccess={() => setLoggedIn(true)} />
      )} */}
      <CloudAI />
    </div>
  );
}
export default App;
