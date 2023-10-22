//CategoriesBar.js
// CategoriesBar.js
import React from "react";
import "./CategoriesBar.css";
import UniversityIcon from "../../assets/University.png";
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
        <img src={UniversityIcon} alt="icon 1" />
        University
      </button>
      <button
        className="categoryButton"
        onClick={(e) => handleButtonClick("Departments", e)}
      >
        {/* <img src="path/to/icon2.png" alt="icon 2" /> */}
        Departments
      </button>
      <button
        className="categoryButton"
        onClick={(e) => handleButtonClick("Interests", e)}
      >
        {/* <img src="path/to/icon2.png" alt="icon 2" /> */}
        Interests
      </button>
      <button
        className="categoryButton"
        onClick={(e) => handleButtonClick("Departments", e)}
      >
        {/* <img src="path/to/icon2.png" alt="icon 2" /> */}
        Projects
      </button>
      <button
        className="categoryButton"
        onClick={(e) => handleButtonClick("Departments", e)}
      >
        {/* <img src="path/to/icon2.png" alt="icon 2" /> */}
        Sponsors
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
