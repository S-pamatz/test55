import React, { useContext, useState } from "react";
import GraphContext from "../../../data/GraphContext";
import Popup from "../../UIComponents/Popup";

const ExpandAllNodeButton = () => {
    const ctx = useContext(GraphContext);
    
    const [showPopup, setShowPopup] = useState(false);
    const [popupContent, setPopupContent] = useState(null);
  
    // This function now combines expanding all nodes and showing the popup
    const handleButtonClick = () => {
      // Call the context method to expand all nodes
      ctx.expandAllNodes();

      // Set the content for the popup and show it
      setPopupContent(<p>All nodes are being expanded. This may take a while...</p>);
      setShowPopup(true);
    };
    
    return (
        <div>
            <button className="expand-all-nodes-button" onClick={handleButtonClick}>
                Expand All Nodes
            </button>
            {showPopup && <Popup onClose={() => setShowPopup(false)}>{popupContent}</Popup>}
        </div>
    );
};

export default ExpandAllNodeButton;
