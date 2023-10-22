module.exports = {
    testEnvironment: 'jsdom',
    moduleFileExtensions: ['js', 'jsx'],
    testPathIgnorePatterns: ['/node_modules/'],
    transform: {
      '^.+\\.(js|jsx)?$': 'babel-jest',
      "\\.(jpg|jpeg|png|gif|webp|svg)$": "jest-transform-stub",
    },
    moduleNameMapper: {
      '\\.(css|less|scss|sss|styl)$': '<rootDir>/node_modules/jest-css-modules',
    },
    setupFilesAfterEnv: ['<rootDir>/setupTests.js'],
  };
  