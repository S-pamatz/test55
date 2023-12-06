//modal.js
import React, { useState } from "react";
import "./modal.css";
import { nodesLibrary } from "../../data/nodeLibrary";
import GraphContext from "../../data/GraphContext";
import Uni from "../../../assets/UniversityW.png";

const Modal = ({ content, image }) => {
  const ctx = React.useContext(GraphContext);

  const [buttons, setButtons] = useState(<></>);
  const [expanded, setExpanded] = useState(false);

  const handleCloseButtonClick = () => {
    if (!expanded) {
      setButtons(
        <div>
          <div onClick={(e) => e.stopPropagation()}>
            {getmModalBoday(content).map((item, index) => (
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
      );
    } else {
      setButtons(<></>);
    }
    setExpanded(!expanded);
  };

  const handleItemButtonClick = (item) => {
    const newItem = {
      ...item,
      icon: Uni,
      expanded: false,
      fx: 500,
      fy: 400,
      depth: 1,
    };
    ctx.setStartingNode(newItem);
  };

  if (!content) return null;

  const getmModalBoday = (keyword) => {
    var allElements = [];
    var keywordId;
    if (keyword === "Departments") {
      // get the Id of the Others node
      var othersId;
      for (const node of nodesLibrary) {
        if (node.Name === "Others") {
          othersId = node.id;
          break;
        }
      }
      for (const node of nodesLibrary) {
        if (node.parent === 7) {
          allElements.push(node);
        }
      }

      for (const node of nodesLibrary) {
        if (node.parent === othersId) {
          allElements.push(node);
        }
      }
      return allElements;
    }

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

  return (
    <div>
      <div className="modalContainer">{buttons}</div>
      <button
        className="categoryButton"
        onClick={(e) => handleCloseButtonClick("University", e)}
      >
        {image}
        {content}
      </button>
    </div>
  );
};
export default Modal;
