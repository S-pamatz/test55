import React from "react";
import "./Header.module.css";
import WsuLogo from "../../assets/wsu-white-logo-red-background.png";
import { FaSearch } from "react-icons/fa";
import GraphContext from "../data/GraphContext";

const Header = () => {
  const ctx = React.useContext(GraphContext);

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

  const getSearch = (e) => {
    e.preventDefault();
    ctx.onSearchClick(search);
  };

  return (
    <header className={classes.header}>
      <div className={classes.wsulogo}>
        <img
          src={WsuLogo}
          alt="Washington State University"
          style={{ height: "100%" }}
        />
      </div>
      <div className={classes.content}>
        <h4 className={classes.title}>Washington State University</h4>
        <div className={classes.helfulLinks}>
          <h4 className={classes.title}>
            <a href="https://foundation.wsu.edu/give/?fund=0b6a7c4f-71f0-4d95-b843-5a26abf439f3&cat=idonate_programs&area=idonate_office_of_research_and_graduate_school&utm_campaign=center-for-environmental-research-education-and-outreach-cereo-excellence-fund">
              Give
            </a>
          </h4>
          <h4 className={classes.title}>
            <a href="https://cereo.wsu.edu/invitation-to-participate/">Apply</a>
          </h4>
          <h4 className={classes.title}>
            <a href="https://cereo.wsu.edu/contact-us/">Locations</a>
          </h4>
          <h4 className={classes.title}>
            <a href="https://cereo.wsu.edu/category/archived/">
              News and Events
            </a>
          </h4>
        </div>
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
      </div>
    </header>
  );
};

export default Header;
