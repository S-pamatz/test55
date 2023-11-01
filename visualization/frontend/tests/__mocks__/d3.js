// __mocks__/d3.js

const d3Mock = {
  select: jest.fn(() => {
    const chainableMethods = {
      selectAll: jest.fn().mockReturnThis(),
      select: jest.fn().mockReturnThis(),
      remove: jest.fn().mockReturnThis(),
      append: jest.fn().mockReturnThis(),
      attr: jest.fn().mockReturnThis(),
      data: jest.fn().mockReturnThis(),
      enter: jest.fn().mockReturnThis(),
      call: jest.fn().mockReturnThis(),
      text: jest.fn().mockReturnThis(),
      on: jest.fn().mockReturnThis(),
    };

    return {
      ...chainableMethods,
      on: jest.fn((event, callback) => {
        if (event === "mouseover") {
          // Simulate mouseover event for testing
          callback();
        }
        return chainableMethods;
      }),
      text: jest.fn().mockReturnThis(),
      attr: jest.fn((name, value) => {
        if (name === "data-full-text") {
          return "Full Text";
        }
        return chainableMethods;
      }),
    };
  }),
  forceSimulation: jest.fn(() => {
    const chainableMethods = {
      force: jest.fn().mockReturnThis(),
      alphaDecay: jest.fn().mockReturnThis(),
      velocityDecay: jest.fn().mockReturnThis(),
      on: jest.fn().mockReturnThis(), 
    };
    return chainableMethods;
  }),
  forceLink: jest.fn(() => ({
    id: jest.fn().mockReturnThis(),
    distance: jest.fn().mockReturnThis(),
    strength: jest.fn().mockReturnThis(),
  })),
  forceManyBody: jest.fn().mockReturnThis(),
  forceCollide: jest.fn(() => ({
    radius: jest.fn().mockReturnThis(),
  })),
  forceX: jest.fn(() => ({
    strength: jest.fn().mockReturnThis(),
  })),
  forceY: jest.fn(() => ({
    strength: jest.fn().mockReturnThis(),
  })),
  forceManyBody: jest.fn(() => ({
    strength: jest.fn().mockReturnThis(),
    distanceMin: jest.fn().mockReturnThis(),
    distanceMax: jest.fn().mockReturnThis(),
  })),
  drag: jest.fn(() => ({
    on: jest.fn().mockReturnThis(),
  })),
  zoom: jest.fn(() => {
    const chainableMethods = {
      on: jest.fn().mockReturnThis(),
      // Add any other methods or properties needed for zoom functionality
    };
    return chainableMethods;
  }),

};

module.exports = d3Mock;
