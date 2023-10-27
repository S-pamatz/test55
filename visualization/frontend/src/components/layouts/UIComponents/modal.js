//modal.js
import React from "react";
import "./modal.css";
import { nodesLibrary } from "../../data/nodeLibrary";
import GraphContext from "../../data/GraphContext";
import Uni from "../../../assets/UniversityW.png";


const Modal = ({ content, position, setActiveModalContent }) => {
  const ctx = React.useContext(GraphContext);
  const handleCloseButtonClick = () => {
    setActiveModalContent(null);
  };


  const handleItemButtonClick = (item) => {
    const newItem = {
      ...item,          
      icon: Uni,        
      expanded: false,
      fx: 500,
      fy: 400,
      depth: 1
    };
    ctx.setStartingNode(newItem);
  };

  if (!content) return null;

  const getmModalBoday = (keyword) => {
    var allElements = [];
    var keywordId;
    // find the id of the keyword
    for (const node of nodesLibrary) {
      if (node.Name === keyword) {
        keywordId = node.id;
        break;
      }
    }
    // if a node has the id as a parent node then add it to the allElements
    for (const node of nodesLibrary) {
      if (node.parent === keywordId) {
        allElements.push(node);
      }
    }
    return allElements;
  };
  let modalTitle, modalBody;
  switch (content) {
    case "University":
      modalTitle = "Universities";
      modalBody = getmModalBoday("Universities");
      break;
    case "Departments":
      modalTitle = "Entities";
      modalBody = getmModalBoday("Departments");
      break;
    case "Interests":
      modalTitle = "Interests";
      modalBody = getmModalBoday("Interests");
      break;
    case "Projects":
      modalTitle = "Projects";
      modalBody = [{ Name: "Fly me to the Moon" }]
      break;
    case "Sponsors":
      modalTitle = "Publications";
      modalBody = [{ Name: "Space Oddity" }]
      break;
    default:
      modalTitle = "";
      modalBody = "";
  }

  const modalStyles = position
  ? {
      top: position.top - 800 + "px",
      left:
        Math.min(
          position.left + position.width / 2 + 90,
          window.innerWidth -
            110 
        ) + "px",
      transform: "translate(-60%, -100%)",
    }
  : {};


  return (
    <div className="modal-container">
    <div className="modal modal-open" style={modalStyles}>
      <button className="closeButton" onClick={handleCloseButtonClick}>×</button>
      <button className="categoriesButton" onClick={handleCloseButtonClick}>
        {modalTitle}
      </button>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {modalBody.map((item, index) => (
          <button
            key={index}
            className="modalContentButton"
            onClick={() => handleItemButtonClick(item)}
          >
            {item.Name}
          </button>
        ))}
      </div>
    </div>
    </div>
  );
};
export default Modal;
