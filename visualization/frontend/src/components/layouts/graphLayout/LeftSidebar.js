// Sidebar.js
import React, { useState, useContext } from "react";
import GraphContext from "../../data/GraphContext";
import classes from "./LeftSidebar.module.css";
import gearIcon from "../../../assets/icons8-gear-48.png";
import viewIcon from "../../../assets/icons8-view-48.png";
import categoryIcon from "../../../assets/icons8-category-30.png";
import backArrow from "../../../assets/icons8-back-arrow-30.png"; // Import the back arrow icon
import searchIcon from "../../../assets/Search.png";
import { FaSearch } from "react-icons/fa";
import { nodesLibrary } from "../../data/nodeLibrary";
import ExpandAllNodeButton from "./LeftSidebarComponent/ExpandAllNodeButton";
import Popup from "../UIComponents/Popup";

const Sidebar = () => {
  const [activeView, setActiveView] = useState("");
  const [expanded, setExpanded] = useState(false); // new state for expansion
  const ctx = useContext(GraphContext);

  const handleButtonClick = (nodeName) => {
    //find the node with the name
    var node;
    for (const n of nodesLibrary) {
      if (n.Name === nodeName) {
        node = n;
        break;
      }
    }
    ctx.setStartingNode(node);
  };

  const handleIconClick = (view) => {
    setActiveView(view);
    setExpanded(true); // set expanded to true when any icon is clicked
  };

  const handleBackClick = () => {
    setActiveView("");
    setExpanded(false); // reset expanded to false when back arrow is clicked
  };

  // Search functionality

  const [search, setSearch] = React.useState("");

  const updateSearch = (e) => {
    setSearch(e.target.value);
  };
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      ctx.onSearchClick(search);
    }
  };

  const [showPopup, setShowPopup] = useState(false);
  const [popupContent, setPopupContent] = useState(null);

  // Function to handle search button click
  const handleSearchClick = () => {
    // Perform the search or show instructions for search
    ctx.onSearchClick(search);

    // Set the content for the popup and show it
    setPopupContent(<p>If the search node is in the graph, the search will highlight its path.
      If the node is not in the graph, the search node will become the main node.</p>); 
    setShowPopup(true); // Show the popup
  };

  return (
    <div className={expanded ? classes.expandedSidebar : classes.sidebar}>
      {expanded ? (
        <button onClick={handleBackClick} className={classes.backButton}>
          <img src={backArrow} alt="Back" />
        </button>
      ) : null}

      {!expanded && ( // Conditional rendering based on the expanded state
        <div className={classes.icons}>
          {/* <img src={categoryIcon} alt="Category" onClick={() => handleIconClick('category')}/> */}
          <img
            src={searchIcon}
            alt="Search"
            onClick={() => handleIconClick("search")}
          />
          <img
            src={viewIcon}
            alt="View"
            onClick={() => handleIconClick("view")}
          />
          <img
            src={gearIcon}
            alt="Settings"
            onClick={() => handleIconClick("settings")}
          />
        </div>
      )}

      {activeView === "view" && (
        <div className={classes.view}>
          <h3>Entries</h3>
          <ul>
            <li>
              <button
                className={classes.button}
                onClick={handleButtonClick.bind(this, "Entities")}
              >
                Entities
              </button>
            </li>
            <li>
              <button
                className={classes.button}
                onClick={handleButtonClick.bind(this, "Universities")}
              >
                Universities
              </button>
            </li>
            <li>
              <button
                className={classes.button}
                onClick={handleButtonClick.bind(this, "Interests")}
              >
                Interests
              </button>
            </li>
            <li>
              <button
                className={classes.button}
                onClick={handleButtonClick.bind(this, "Projects")}
              >
                Projects
              </button>
            </li>
            <li>
              <button
                className={classes.button}
                onClick={handleButtonClick.bind(this, "Publications")}
              >
                Publications
              </button>
            </li>
          </ul>
        </div>
      )}
      {activeView === "search" && (
        <>
          <div className={classes.search}>
            <input
              type="text"
              className={classes.searchBox}
              value={search}
              placeholder="Search"
              onChange={updateSearch}
              onKeyPress={handleKeyPress}
            />
            <button
              className={classes.searchButton}
              onClick={handleSearchClick}
            >
              <FaSearch />
            </button>
          </div>
          {showPopup && (
            <Popup onClose={() => setShowPopup(false)}>{popupContent}</Popup>
          )}
        </>
      )}
      {activeView === "settings" && (
        <div className={classes.settings}>
          <h3>Settings</h3>
          <ExpandAllNodeButton />
        </div>
      )}
    </div>
  );
};

export default Sidebar;
