import React, { useState, useEffect } from 'react';
import './CloudAI.css';

const moods = [
  { emoji: "🎉", label: "Party" },
  { emoji: "☕️", label: "Coffee" },
  { emoji: "🏋🏻‍♂️", label: "Workout" },
  { emoji: "🛍️", label: "Shopping" },
  { emoji: "🥙", label: "Food" },
  { emoji: "🧗", label: "Adventurous" },
];

const CloudAI = () => {
  const [selectedMood, setSelectedMood] = useState(null);
  const [customMood, setCustomMood] = useState("");

  //When page loads gets user's current location
  useEffect(()=>{
    let coordinates;
    navigator.geolocation.getCurrentPosition((position)=>{
      coordinates = JSON.stringify({longitude: position.coords.longitude, latitude: position.coords.latitude});
      console.log(coordinates);
      try
      {
        fetch("http://127.0.0.1:5555/locationmood", {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: coordinates
        });
      }
      catch(e)
      {
        console.log(e);
      }
    });
    
    
  },[])

  const handleMoodClick = (mood) => {
    setSelectedMood(mood.label);
    alert(`You selected: ${mood.label}`);
  };

  const handleCustomMoodSubmit = () => {
    if (customMood.trim()) {
      alert(`You typed: ${customMood}`);
    }
  };

  return (
    <div className="homepage-container">
      <div className="cloud">☁️</div>
      <h2>What's the move for today?</h2>

      <div className="mood-options">
        {moods.map((mood, index) => (
          <button
            key={index}
            className={`mood-button ${selectedMood === mood.label ? 'selected' : ''}`}
            onClick={() => handleMoodClick(mood)}
          >
            {mood.emoji} <span>{mood.label}</span>
          </button>
        ))}
      </div>

      <div className="mood-input-container">
        <input
          type="text"
          className="mood-cloud-input"
          placeholder="What's the Move? ☁️"
          value={customMood}
          onChange={(e) => setCustomMood(e.target.value)}
        />
        <button className="submit-mood" onClick={handleCustomMoodSubmit}>
          Submit
        </button>
      </div>
    </div>
  );
};

export default CloudAI;