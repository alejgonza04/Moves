import React, { useState } from "react";
import Homepage from "./Components/Homepage/Homepage";
import Bookmarks from "./Components/Bookmarks/Bookmarks";
import LoginSignup from "./Components/LoginSignup/LoginSignup";
import "./App.css"; // Only styling here

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [bookmarkedUsers, setBookmarkedUsers] = useState([]);
  const [activeTab, setActiveTab] = useState("homepage");

  const handleSwipeRight = (user) => {
    setBookmarkedUsers((prev) => [...prev, user]);
  };

  const handleSignOut = () => {
    setLoggedIn(false);
    setBookmarkedUsers([]);
    setActiveTab("homepage");
  };

  if (!loggedIn) {
    return (
      <div className="login-page-background">
        <LoginSignup onLoginSuccess={() => setLoggedIn(true)} />
      </div>
    );
  }

  return (
    <div className="app-container">
      <div className="tab-buttons">
        <button onClick={() => setActiveTab("homepage")}>Homepage</button>
        <button onClick={() => setActiveTab("bookmarks")}>Bookmarks</button>
        <button onClick={handleSignOut}>Sign Out</button>
      </div>

      {activeTab === "homepage" ? (
        <Homepage onSwipeRight={handleSwipeRight} />
      ) : (
        <Bookmarks bookmarkedUsers={bookmarkedUsers} />
      )}
    </div>
  );
}

export default App;
