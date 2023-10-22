import React from "react";
import ReactDOM from "react-dom/client";

import "./index.css";
import App from "./App";
import  {GraphContextProvider}  from './components/data/GraphContext';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <GraphContextProvider>
    <App />
  </GraphContextProvider>
);

