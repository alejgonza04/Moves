import React from "react";
// import LoginSignup from "./Components/LoginSignup/LoginSignup";
// import CloudAI from "./Components/CloudAI/CloudAI";
//import CloudAI from "./Components/Homepage/Homepage";
import Homepage from "./Components/Homepage/Homepage";

function App() {
  // const [loggedIn, setLoggedIn] = useState(false);

  return (
    <div>
      {/* {loggedIn ? (
        <Homepage />
      ) : (
        <LoginSignup onLoginSuccess={() => setLoggedIn(true)} />
      )} */}
      <Homepage />
    </div>
  );
}
export default App;
