//CategoriesBar.js
// CategoriesBar.js
import React from "react";
import "./CategoriesBar.css";
import UniversityIcon from "../../../assets/UniversityB.png";
import DepartmentsIcon from "../../../assets/DepartmentB.png";
import Interests from "../../../assets/InterestB.png";
import Projects from "../../../assets/ProjectB.png";
import Sponsors from "../../../assets/SponsorsB.png";
import Modal from "../UIComponents/modal";

const CategoriesBar = () => {
  const [activeModalContent, setActiveModalContent] = React.useState(null);
  const [buttonPosition, setButtonPosition] = React.useState(null);
  const [isButtonClicked, setIsButtonClicked] = React.useState(false);

  const handleButtonClick = (contentType, event) => {
    const rect = event.currentTarget.getBoundingClientRect();
    setButtonPosition({ top: rect.top, left: rect.left, width: rect.width });

    

    if (activeModalContent === contentType) {
        setActiveModalContent(null);
    } else {
        setActiveModalContent(contentType);
    }
    
    setIsButtonClicked(true);
};


  return (
    <div className="categoriesBar" >
      <button
        className="categoryButton"
        onClick={(e) => handleButtonClick("University", e)}
      >
        <img src={UniversityIcon} alt="University" />
        Universities
      </button>
      <button
        className="categoryButton"
        onClick={(e) => handleButtonClick("Departments", e)}
      >
        <img src={DepartmentsIcon} alt="Entities" />
        Entities
      </button>
      <button
        className="categoryButton"
        onClick={(e) => handleButtonClick("Interests", e)}
      >
        <img src={Interests} alt="Interests" />
        Interests
      </button>
      <button
        className="categoryButton"
        onClick={(e) => handleButtonClick("Projects", e)}
      >
        <img src={Projects} alt="Projects"/>
        Projects
      </button>
      <button
        className="categoryButton"
        onClick={(e) => handleButtonClick("Sponsors", e)}
      >
        <img src={Sponsors} alt="Publications" />
        Publications
      </button>
      <Modal
        content={activeModalContent}
        position={buttonPosition}
        setActiveModalContent={setActiveModalContent}
      />
    </div>
  );
};

export default CategoriesBar;
