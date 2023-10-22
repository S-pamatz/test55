// getDataFromBackend.js
// Description: This file contains functions that make requests to the backend to get data.
// make a request to the backend to get all the entries
export const filterEntries = (valueToFilterBy) => {
  return new Promise((resolve, reject) => {
    fetch(`/search?inputValue=${valueToFilterBy}`)
      .then((response) => response.json())
      .then((filteredEntries) => {
        if (!Array.isArray(filteredEntries)) {
          console.error("Error: filteredEntries is not an array");
          reject("Error: filteredEntries is not an array");
        } else {
          resolve(filteredEntries);
        }
      })
      .catch((error) => {
        console.error("Error fetching and filtering data:", error);
        reject(error);
      });
  });
};
// make a request to the backend to get the unique departments
export const getUniqueDepartments = () => {
  return new Promise((resolve, reject) => {
    fetch("/unique-departments")
      .then((response) => response.json())
      .then((uniqueDepartments) => {
        if (!Array.isArray(uniqueDepartments)) {
          console.error("Error: uniqueDepartments is not an array");
          reject("Error: uniqueDepartments is not an array");
        } else {
          resolve(uniqueDepartments);
        }
      })
      .catch((error) => {
        console.error("Error fetching unique departments:", error);
        reject(error);
      });
  });
};
// make a request to the backend to get the unique interests
export const getUniqueInterests = () => {
  return new Promise((resolve, reject) => {
    fetch("/unique-interests")
      .then((response) => response.json())
      .then((uniqueInterests) => {
        if (!Array.isArray(uniqueInterests)) {
          console.error("Error: uniqueInterests is not an array");
          reject("Error: uniqueInterests is not an array");
        } else {
          resolve(uniqueInterests);
        }
      })
      .catch((error) => {
        console.error("Error fetching unique interests:", error);
        reject(error);
      });
  });
};
