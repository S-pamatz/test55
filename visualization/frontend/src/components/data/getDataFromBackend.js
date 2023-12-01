// getDataFromBackend.js
// Description: This file contains functions that make requests to the backend to get data.

// Define the base URL of the backend server
//const backendBaseUrl = "http://172.232.172.160:3004"; // Replace with your actual backend URL
const backendBaseUrl = "http://localhost:3004";
const remoteServer = "https://cereo.azurewebsites.net";

// Function to make a request to the backend to get all the entries
export const filterEntries = (valueToFilterBy) => {
  return new Promise((resolve, reject) => {
    // Make a fetch request to the backend's /search endpoint
    // fetch(`${backendBaseUrl}/search?inputValue=${valueToFilterBy}`)
    fetch(`${remoteServer}/search?inputValue=${valueToFilterBy}`)
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

// Function to make a request to the backend to get the unique departments
export const getUniqueDepartments = () => {
  return new Promise((resolve, reject) => {
    // Make a fetch request to the backend's /unique-departments endpoint
    fetch(`${remoteServer}/returnUniqueDepart`)
      .then((response) => response.json())
      .then((uniqueDepartments) => {
        // console.log("uniqueDepartments", uniqueDepartments);
        if (!Array.isArray(uniqueDepartments)) {
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

export const getUniqueInterests = () => {
  return new Promise((resolve, reject) => {
    // Make a fetch request to the backend's /unique-interests endpoint
    fetch(`${remoteServer}/search_Unique_interests`)
      .then((response) => response.json())
      .then((responseData) => {
        const uniqueInterests = responseData.data;
        console.log("uniqueInterests", uniqueInterests);
        if (!Array.isArray(uniqueInterests)) {
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

export const getData = () => {
  return new Promise((resolve, reject) => {
    fetch(`${remoteServer}/jsnDerulo`)
      .then((response) => response.json())
      .then((data) => {
        // console.log("data", data);
        if (!Array.isArray(data)) {
          console.error("Error: data is not an array");
          reject("Error: data is not an array");
        } else {
          resolve(data);
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        reject(error);
      });
  });
};
