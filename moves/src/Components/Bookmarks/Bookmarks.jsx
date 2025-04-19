import React from "react";

function Bookmarks({ bookmarkedUsers }) {
  return (
    <div>
      <h2>Bookmarks</h2>
      {bookmarkedUsers.length === 0 ? (
        <p>No bookmarks yet!</p>
      ) : (
        <div>
          {bookmarkedUsers.map((user, index) => (
            <div key={index}>
              <img src={user.imgUrl} alt={user.name} style={{ width: "150px", height: "150px" }} />
              <h4>{user.name}, {user.age}</h4>
              <p>{user.work}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Bookmarks;
