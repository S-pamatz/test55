//app.js
const csv = require("csv-parser");
const fs = require("fs");
const express = require("express");
const cors = require("cors");
const { start } = require("repl");
const app = express();

const PORT = 3004;
//for unitTesting
let server;
const data = [];

function startServer() {
  return new Promise((resolve) => {
    server = app.listen(PORT, () => {
      console.log(`Server started on http://localhost:${PORT}`);
      resolve();
    });
  });
}
function stopServer() {
  return new Promise((resolve) => {
    if (server) {
      server.close(() => {
        console.log('Server stopped');
        resolve();
      });
    } else {
      console.error('Server instance not available.');
      resolve();
    }
  });
}
function loadDataFromCSV() {
  return new Promise((resolve, reject) => {
    fs.createReadStream("./data.csv")
      .pipe(csv())
      .on("data", (row) => {
        // Assign miscellaneous value to undefined or empty attributes
        const newRow = {
          Interest: row["Please select which primary CEREO theme best describes your area of interest:"] || "miscellaneous",
          Department: row["Department"] || "miscellaneous",
          Name: row["Name"] || "miscellaneous",
          Membership: row["Please indicate the kind of membership"] || "miscellaneous",
          WSUCampus: row["WSU Campus"] || "miscellaneous",
          Email: row["Email"] || "miscellaneous",
          URL: row["URL"] || "miscellaneous"
        };
        data.push(newRow);  
      })
      .on("end", () => {
        console.log("CSV file successfully loaded.");
        resolve();
      })
      .on("error", reject);
  });
}


loadDataFromCSV();

// Enable CORS for all routes
app.use(cors());

app.get("/search", (req, res) => {
  try {
    const inputValue = req.query.inputValue;

    if (typeof inputValue !== 'string') {
      console.error("Invalid inputValue:", inputValue);
      return res.status(400).json({ error: 'Invalid input value' });
    }

    // Perform filtering based on the inputValue
    const filteredData = data.filter((entry) => {
      return (
        (entry.Department?.toLowerCase() ?? '').includes(inputValue.toLowerCase()) ||
        (entry.Interest?.toLowerCase() ?? '').includes(inputValue.toLowerCase()) ||
        (entry.Name?.toLowerCase() ?? '').includes(inputValue.toLowerCase()) ||
        (entry.Membership?.toLowerCase() ?? '').includes(inputValue.toLowerCase()) ||
        (entry.WSUCampus?.toLowerCase() ?? '').includes(inputValue.toLowerCase()) ||
        (entry.Email?.toLowerCase() ?? '').includes(inputValue.toLowerCase()) ||
        (entry.URL?.toLowerCase() ?? '').includes(inputValue.toLowerCase())
      );
    });
    console.log(filteredData);
    res.json(filteredData);
  } catch (error) {
    console.error("Error fetching and filtering data:", error);
    res.status(500).json({ error: error.toString() });
  }
});

// Get all unique departments
app.get("/unique-departments", (req, res) => {
  const uniqueDepartments = [...new Set(data.map((entry) => entry.Department))];
  console.log(uniqueDepartments);
  res.json(uniqueDepartments);
});

// Get all unique interests
app.get("/unique-interests", (req, res) => {
  const uniqueInterests = [
    ...new Set(
      data.map((entry) => {
        const interestString = entry["Interest"];
        const match = /^([^<]+)/.exec(interestString);
        return match ? match[1].trim() : interestString;
      })
    ),
  ];

  res.json(uniqueInterests);
});


startServer();

module.exports = {
  app,
  startServer,
  stopServer,
  loadDataFromCSV
};