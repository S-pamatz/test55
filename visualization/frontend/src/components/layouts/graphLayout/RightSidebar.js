//RightSidebar.js
import React, { useContext, useState, useEffect } from "react";
import GraphContext from "../../data/GraphContext";
import "./RightSidebar.css";
import CloseIcon from "../../../assets/icons8-back-arrow-30.png";

const NodeInfoRightSidebar = () => {
  const { selectedNode } = useContext(GraphContext);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true); 

  useEffect(() => {
    // Whenever selectedNode changes, open the sidebar
    setIsSidebarOpen(true);
  }, [selectedNode]);

  const handleSidebarToggle = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  if (!selectedNode) {
    return ;
  }

  return (
    <div className={isSidebarOpen ? "sidebar" : "sidebarClosed"}>
      <button onClick={handleSidebarToggle} className="closeButton">
        <img src={CloseIcon} alt="Close Sidebar" />
      </button>
      {isSidebarOpen && (
        <div className="NodeInfo">
          <span>
            <h2>{selectedNode.Name}</h2>
          </span>
          <div>
            <h4>WSU Campus: </h4>
            <div>{selectedNode.WSUCampus}</div>
            <h4>Site:</h4>
            <div>{selectedNode.URL}</div>
            <h4>Email:</h4>
            <div>{selectedNode.Email}</div>
            <h4>Interest:</h4>
            <div>{selectedNode.Interest}</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default NodeInfoRightSidebar;