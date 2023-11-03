module.exports = {
    testEnvironment: 'jsdom',
    moduleFileExtensions: ['js', 'jsx'],
    testPathIgnorePatterns: ['/node_modules/'],
    transform: {
      '^.+\\.(js|jsx)?$': 'babel-jest',
      "\\.(jpg|jpeg|png|gif|webp|svg)$": "jest-transform-stub",
    },
    "moduleNameMapper": {
      "\\.(css|less|scss|sss|styl)$": "identity-obj-proxy"
    },
    setupFilesAfterEnv: ['<rootDir>/setupTests.js'],
  };
  