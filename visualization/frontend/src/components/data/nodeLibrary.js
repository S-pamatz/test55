// nodeLibrary.js
// affilate = [{id: __, Name: ___, Department: ___, Interest: ___, Email: ___, WSU Campus: ___, URL: ___}]
import { getUniqueDepartments, getUniqueInterests } from './getDataFromBackend';
import Uni from "../assets/University.png";
export let nodesLibrary = [
  { id: 0, Name: "wsu",  icon: Uni, expanded: false, fx: 500, fy: 400, depth: 0 },
  { id: 1, Name: "Interests",  icon: Uni, expanded: false, fx: 500, fy: 400, depth: 0 },
  { id: 2, Name: "Departments",  icon: Uni, expanded: false, fx: 500, fy: 400, depth: 0 },
  { id: 3, Name: "People",  icon: Uni, expanded: false, fx: 500, fy: 400, depth: 0 },
  { id: 4, Name: "Projects",  icon: Uni, expanded: false, fx: 500, fy: 400, depth: 0 },
  { id: 5, Name: "Sponsors",  icon: Uni, expanded: false, fx: 500, fy: 400, depth: 0 },
  { id: 6, Name: "Partners",  icon: Uni, expanded: false, fx: 500, fy: 400, depth: 0 },
  { id: 7, Name: "University",  icon: Uni, expanded: false, fx: 500, fy: 400, depth: 0 },
];

export const populateNodesWithUniqueData = async () => {
  try {
    // Fetch unique departments and interests
    const uniqueDepartments = await getUniqueDepartments();
    const uniqueInterests = await getUniqueInterests();
  
    // Limit the number of departments to 10
    const limitedUniqueDepartments = uniqueDepartments.slice(0, 10);
  
    // Determine the starting ID for the new nodes based on the current length of nodesLibrary
    let currentId = nodesLibrary.length;

    // Iterate over limitedUniqueDepartments (which has at most 10 departments) and add them to nodesLibrary
    for (const department of limitedUniqueDepartments) {
      nodesLibrary.push({
        id: currentId,
        Name: department,
        parent: 0 ,  // Assuming wsu node id as the parent
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
        parent: 1,  // Assuming Interests node id as the parent
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
