// Sidebar.js
import React, { useState, useContext } from "react";
import GraphContext from "../../data/GraphContext";
import classes from "./LeftSidebar.module.css";
import gearIcon from "../../assets/icons8-gear-48.png";
import viewIcon from "../../assets/icons8-view-48.png";
import categoryIcon from "../../assets/icons8-category-30.png";
import backArrow from "../../assets/icons8-back-arrow-30.png"; // Import the back arrow icon
import searchIcon from "../../assets/icons8-search.svg";
import { FaSearch } from "react-icons/fa";

const Sidebar = () => {
  const [activeView, setActiveView] = useState("");
  const [expanded, setExpanded] = useState(false); // new state for expansion
  const ctx = useContext(GraphContext);

  const handleButtonClick = (index) => {
    const currentNode = ctx.nodes[index];

    const newFill = currentNode.fill === "green" ? "red" : "green";
    ctx.updateNode(index, { fill: newFill });
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
  }
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      ctx.onSearchClick(search);
    }
  };

  const getSearch = (e) => {
    e.preventDefault();
    ctx.onSearchClick(search);
  }


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
        <>
          <h3>Entries</h3>
          <ul>
            {ctx.nodes.map((node, index) => (
              <li key={index}>
                <button onClick={() => handleButtonClick(index)}>
                  {node.Name}
                </button>
              </li>
            ))}
          </ul>
        </>
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
            <button className={classes.searchButton} onClick={getSearch}>
              <FaSearch />
            </button>
          </div>
        </>
      )}
      {/* TODO: Add content for other icons as needed */}
    </div>
  );
};

export default Sidebar;
