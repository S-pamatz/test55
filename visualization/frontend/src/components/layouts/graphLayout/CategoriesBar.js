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
    setButtonPosition({
      top: rect.bottom,
      left: rect.left,
      width: rect.width,
      height: rect.height,
    });

    if (activeModalContent === contentType) {
      setActiveModalContent(null);
    } else {
      setActiveModalContent(contentType);
    }

    setIsButtonClicked(true);
  };

  return (
    <span className="categoriesBar">
      <Modal
        content={"Universities"}
        position={buttonPosition}
        image={<img src={UniversityIcon} alt="University" />}
        setActiveModalContent={setActiveModalContent}
      />

      <Modal
        content={"Departments"}
        position={buttonPosition}
        image={<img src={DepartmentsIcon} alt="University" />}
        setActiveModalContent={setActiveModalContent}
      />

      <Modal
        content={"Intrests"}
        position={buttonPosition}
        image={<img src={Interests} alt="University" />}
        setActiveModalContent={setActiveModalContent}
      />

      <Modal
        content={"Projects"}
        position={buttonPosition}
        image={<img src={Projects} alt="University" />}
        setActiveModalContent={setActiveModalContent}
      />

      <Modal
        content={"Publications"}
        position={buttonPosition}
        image={<img src={Sponsors} alt="University" />}
        setActiveModalContent={setActiveModalContent}
      />
    </span>
  );
};

export default CategoriesBar;
