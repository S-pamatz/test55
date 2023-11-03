import  nodesLibrary  from './nodeLibrary';
import {
    getUniqueDepartments,
    getUniqueInterests,
    getData,
  } from "./getDataFromBackend";
import University from "../../assets/UniversityW.png";

export const populateNodesWithUniqueData = async () => {
    try {
      // Fetch unique departments and interests
      const uniqueDepartments = await getUniqueDepartments();
      const uniqueInterests = await getUniqueInterests();
      // ******************************************************
      // const data = await getData();
      // console.log("data", data);
      // ******************************************************
      // Limit the number of departments to 10
      // const limitedUniqueDepartments = uniqueDepartments.slice(0, 10);
  
      // Determine the starting ID for the new nodes based on the current length of nodesLibrary
      let currentId = nodesLibrary.length;
  
      // Iterate over limitedUniqueDepartments (which has at most 10 departments) and add them to nodesLibrary
      for (const department of uniqueDepartments.slice(0, 10)) {
        nodesLibrary.push({
          id: currentId,
          Name: department,
          parent: 6, // Assuming wsu node id as the parent
          expanded: false,
          fx: null,
          fy: null,
          depth: 1,
        });
        currentId++;
      }
  
      let otherId = currentId;
  
      nodesLibrary.push({
        id: otherId,
        Name: "Others",
        parent: 6, // Assuming wsu node id as the parent
        expanded: false,
        fx: null,
        fy: null,
        depth: 0,
      });
      currentId++;
  
      for (const department of uniqueDepartments.slice(
        10,
        uniqueDepartments.length
      )) {
        nodesLibrary.push({
          id: currentId,
          Name: department,
          parent: otherId, // Assuming wsu node id as the parent
          expanded: false,
          fx: null,
          fy: null,
          depth: 1,
        });
        currentId++;
      }
  
      // Iterate over unique interests and add them to nodesLibrary
      for (const interest of uniqueInterests) {
        nodesLibrary.push({
          id: currentId,
          Name: interest,
          parent: 2, // Assuming Interests node id as the parent
          expanded: false,
          fx: null,
          fy: null,
          depth: 1,
        });
        currentId++;
      }
    } catch (error) {
      console.error("Error populating nodes with unique data:", error);
    }
  };
  