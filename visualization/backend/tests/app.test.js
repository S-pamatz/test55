//app.test.js
//Instruction to run test
// In app.js comment out line 114
// cd int the backend folder
// run npm test
const request = require('supertest');
const { app, startServer, stopServer, loadDataFromCSV } = require('../app');

beforeAll(async () => {
  await loadDataFromCSV();
  await startServer();
}, 10000);  // 10 seconds


afterAll(async () => {
  await stopServer();
});



describe("GET /search", () => {

  it("should filter data based on the query parameter", async () => {
    const inputValue = "Karen Weathermon"; // replace with a sample input value

    const response = await request(app).get(`/search?inputValue=${inputValue}`);

    expect(response.status).toBe(200);

    // assuming you expect an array response
    expect(Array.isArray(response.body)).toBe(true);

    // You can add more assertions based on your expected response
    // For example, checking if every returned entry contains the inputValue in the right places
    response.body.forEach((entry) => {
      const interestValue = entry["Please select which primary CEREO theme best describes your area of interest:"];
      expect(
        entry.Department.toLowerCase().includes(inputValue.toLowerCase()) ||
          interestValue.toLowerCase().includes(inputValue.toLowerCase()) ||
          entry.Name.toLowerCase().includes(inputValue.toLowerCase())
      ).toBe(true);
    });
  });
  it("should filter data based on the query parameter", async () => {
    const inputValue = "Civil Engineering"; // replace with a sample input value

    const response = await request(app).get(`/search?inputValue=${inputValue}`);

    expect(response.status).toBe(200);

    // assuming you expect an array response
    expect(Array.isArray(response.body)).toBe(true);

    // You can add more assertions based on your expected response
    // For example, checking if every returned entry contains the inputValue in the right places
    response.body.forEach((entry) => {
      const interestValue = entry["Please select which primary CEREO theme best describes your area of interest:"];
      expect(
        entry.Department.toLowerCase().includes(inputValue.toLowerCase()) ||
          interestValue.toLowerCase().includes(inputValue.toLowerCase()) ||
          entry.Name.toLowerCase().includes(inputValue.toLowerCase())
      ).toBe(true);
    });
  });
  it("should filter data based on the query parameter", async () => {
    const inputValue = "Sustainability and the Environment"; // replace with a sample input value

    const response = await request(app).get(`/search?inputValue=${inputValue}`);

    expect(response.status).toBe(200);

    // assuming you expect an array response
    expect(Array.isArray(response.body)).toBe(true);

    // You can add more assertions based on your expected response
    // For example, checking if every returned entry contains the inputValue in the right places
    response.body.forEach((entry) => {
      const interestValue = entry["Please select which primary CEREO theme best describes your area of interest:"];
      expect(
        entry.Department.toLowerCase().includes(inputValue.toLowerCase()) ||
          interestValue.toLowerCase().includes(inputValue.toLowerCase()) ||
          entry.Name.toLowerCase().includes(inputValue.toLowerCase())
      ).toBe(true);
    });
  });

});

describe("GET /unique-departments", () => {

  it("should return all unique departments", async () => {
    const response = await request(app).get('/unique-departments');

    expect(response.status).toBe(200);
    expect(Array.isArray(response.body)).toBe(true);

    // Check if every item is unique
    const uniqueItems = [...new Set(response.body)];
    expect(uniqueItems.length).toEqual(response.body.length);
  });

});

describe("GET /unique-interests", () => {

  it("should return all unique interests", async () => {
    const response = await request(app).get('/unique-interests');

    expect(response.status).toBe(200);
    expect(Array.isArray(response.body)).toBe(true);

    // Check if every item is unique
    const uniqueItems = [...new Set(response.body)];
    expect(uniqueItems.length).toEqual(response.body.length);
  });

});