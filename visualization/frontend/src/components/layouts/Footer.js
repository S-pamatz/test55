import React from "react";
import classes from "./Footer.module.css";

function Footer() {
  return (
    <footer className={classes.footer}>
      <div className={`${classes.container} ${classes.flexContainer}`}>
        <div className={classes.copyright}>
          &copy; {new Date().getFullYear()} Washington State University |{" "}
          <a
            href="https://cereo.wsu.edu/privacy-policy/"
            className={classes.link}
          >
            Privacy Policy
          </a>
        </div>
        <div className={classes.footerContent}>
          <ul>
            <li><a href="https://cereo.wsu.edu/" className={classes.link}>CEREO Home</a></li>
            <li className={classes.separator}>|</li>
            <li><a href="https://cereo.wsu.edu/contact-us/" className={classes.link}>Contact Us</a></li>
            <li className={classes.separator}>|</li>
            <li><a href="https://cereo.wsu.edu/category/archived/" className={classes.link}>News & Events</a></li>
            <li className={classes.separator}>|</li>
            <li><a href="https://cereo.wsu.edu/invitation-to-participate/" className={classes.link}>Participate</a></li>
            <li className={classes.separator}>|</li>
            <li><a href="https://cereo.wsu.edu/resources/" className={classes.link}>Resources</a></li>
          </ul>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
