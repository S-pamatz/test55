
import React from 'react';
import './Popup.css'; // Your custom CSS styles

const Popup = ({ children, onClose }) => {
  return (
    <div className="popup-background">
      <div className="popup-container">
        <button className="close-btn" onClick={onClose}>Close</button>
        {children}
      </div>
    </div>
  );
};

export default Popup;