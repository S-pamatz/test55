// nodeLibrary.js
// affilate = [{id: __, Name: ___, Department: ___, Interest: ___, Email: ___, WSU Campus: ___, URL: ___}]
import { getUniqueDepartments, getUniqueInterests, getData } from './getDataFromBackend';
import University from "../../assets/UniversityW.png";

export let nodesLibrary = [
  // posible root nodes
  { id: 0, Name: "Universities",  icon: University, expanded: false,  depth: 0 , fx:500, fy:400},
  { id: 1, Name: "Entities",  icon: University, expanded: false, fx: 500, fy: 400, depth: 0 },
  { id: 2, Name: "Interests",  icon: University, expanded: false, fx: 500, fy: 400, depth: 0 },
  { id: 3, Name: "Projects",  icon: University, expanded: false, fx: 500, fy: 400, depth: 0 },
  { id: 4, Name: "Publications",  icon: University, expanded: false, fx: 500, fy: 400, depth: 0 },
  { id: 5, Name: "Departments",  icon: University, expanded: false, fx: 500, fy: 400, depth: 0 },
  // possible children nodes of Universities
  { id: 6, Name: "WSU",  icon: University, expanded: false,  depth: 0 , parent: 0},
  { id: 7, Name: "Oregon State",  icon: University, expanded: false,  depth: 0, parent: 0 },
  // possible children nodes of Entities
  { id: 8, Name: "Sponsors",  icon: University, expanded: false,  depth: 0, parent: 1 },
  { id: 9, Name: "Partners",  icon: University, expanded: false,  depth: 0, parent: 1 },
  { id: 10, Name: "Universities Colleges",  icon: University, expanded: false,  depth: 0, parent: 1 },
  // possible children nodes of sponsors
  { id: 11, Name: "Ecol",  icon: University, expanded: false,  depth: 0, parent: 8 },
  { id: 12, Name: "NASA",  icon: University, expanded: false,  depth: 0, parent: 8 },
  { id: 13, Name: "USDA",  icon: University, expanded: false,  depth: 0, parent: 8 },
  { id: 14, Name: "USAID",  icon: University, expanded: false,  depth: 0, parent: 8 },
  { id: 15, Name: "NSF",  icon: University, expanded: false,  depth: 0, parent: 8 },
  // possible children nodes of partners
  { id: 16, Name: "NM University",  icon: University, expanded: false,  depth: 0, parent: 9 },
  { id: 17, Name: "CA Merced Universiy",  icon: University, expanded: false,  depth: 0, parent: 9 },
  { id: 18, Name: "Cairo Universiy",  icon: University, expanded: false,  depth: 0, parent: 9 },
  // possible children nodes of Universities Colleges
  { id: 19, Name: "WSU(1)",  icon: University, expanded: false,  depth: 0, parent: 10 },
  { id: 20, Name: "UNM",  icon: University, expanded: false,  depth: 0, parent: 10 },
  { id: 21, Name: "UO",  icon: University, expanded: false,  depth: 0, parent: 10 },
  { id: 22, Name: "UI",  icon: University, expanded: false,  depth: 0, parent: 10 },
  // possible children nodes of WSU 19
  { id: 23, Name: "Faculty",  icon: University, expanded: false,  depth: 0, parent: 19 },
  { id: 24, Name: "Non-Faculty",  icon: University, expanded: false,  depth: 0, parent: 19 },
  // possible children nodes for Projects
  { id: 25, Name: "Project 1",  icon: University, expanded: false,  depth: 0, parent: 3 },
  { id: 26, Name: "Project 2",  icon: University, expanded: false,  depth: 0, parent: 3 },
  // possible children nodes for Publications
  { id: 27, Name: "Event",  icon: University, expanded: false,  depth: 0, parent: 4 },
  { id: 28, Name: "Journal Article",  icon: University, expanded: false,  depth: 0, parent: 4 },
  // possible children nodes for projects 1
  { id: 29, Name: "Publication",  icon: University, expanded: false,  depth: 0, parent: 25 },
  { id: 30, Name: "People",  icon: University, expanded: false,  depth: 0, parent: 25 },
  { id: 31, Name: "Interest",  icon: University, expanded: false,  depth: 0, parent: 25 },
  // possible children nodes for publication 1
  { id : 32, Name: "People",  icon: University, expanded: false,  depth: 0, parent: 27 },
  { id: 35, Name: "People",  icon: University, expanded: false,  depth: 0, parent: 28 },
  { id: 36, Name: "Interest",  icon: University, expanded: false,  depth: 0, parent: 28 },
  { id: 37, Name: "Entities",  icon: University, expanded: false,  depth: 0, parent: 28 },
  

];

export const populateNodesWithUniqueData = async () => {
  try {
    // Fetch unique departments and interests
    const uniqueDepartments = await getUniqueDepartments();
    const uniqueInterests = await getUniqueInterests();
    // ******************************************************
    const data = await getData();
    console.log("data", data);
    // ******************************************************
    // Limit the number of departments to 10
    // const limitedUniqueDepartments = uniqueDepartments.slice(0, 10);
  
    // Determine the starting ID for the new nodes based on the current length of nodesLibrary
    let currentId = nodesLibrary.length;

    // Iterate over limitedUniqueDepartments (which has at most 10 departments) and add them to nodesLibrary
    for (const department of uniqueDepartments) {
      nodesLibrary.push({
        id: currentId,
        Name: department,
        parent: 6,  // Assuming wsu node id as the parent
        expanded: false,
        fx: null,
        fy: null,
        depth: 1
      });
      currentId++;
    }

    // Iterate over unique interests and add them to nodesLibrary
    for (const interest of uniqueInterests) {
      nodesLibrary.push({
        id: currentId,
        Name: interest,
        parent: 2,  // Assuming Interests node id as the parent
        expanded: false,
        fx: null,
        fy: null,
        depth: 1
      });
      currentId++;
    }

  } catch (error) {
    console.error("Error populating nodes with unique data:", error);
  }
};
