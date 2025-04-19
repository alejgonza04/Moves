import React, { useState } from "react";
import Homepage from "./Components/Homepage/Homepage";
import Bookmarks from "./Components/Bookmarks/Bookmarks"; // ✅ make sure file is named Bookmarks.jsx

function App() {
  const [bookmarkedUsers, setBookmarkedUsers] = useState([]);
  const [activeTab, setActiveTab] = useState("homepage");

  const handleSwipeRight = (user) => {
    setBookmarkedUsers((prev) => [...prev, user]);
  };

  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "10px",
          margin: "20px 0",
        }}
      >
        <button onClick={() => setActiveTab("homepage")}>Homepage</button>
        <button onClick={() => setActiveTab("bookmarks")}>Bookmarks</button>
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
