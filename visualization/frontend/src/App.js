// App.js
import Header from "./components/layouts/Header";
import Footer from "./components/layouts/Footer";
import classes from "./App.module.css";
import ForceDirectGraph from "./components/graphComponents/ForceDirectGraph";
import Sidebar from "./components/layouts/graphLayout/LeftSidebar";
import NodeInforightSidebar from "./components/layouts/graphLayout/RightSidebar";
import CategoriesBar from "./components/layouts/graphLayout/CategoriesBar";
import "./index.css";
import { populateNodesWithUniqueData } from "./components/data/uniqueData";



function App()  {
  populateNodesWithUniqueData();
  return (
    <div>
      {/* <Header /> */}
      <div className={classes.app}>
        <div className={classes.centerContainer}>
          <div className={classes.graph}>
            <ForceDirectGraph />
            <div className={classes.sidebar}>
              <Sidebar />
              <NodeInforightSidebar />
              <CategoriesBar />
            </div>
          </div>
        </div>
      </div>
      {/* <Footer /> */}
    </div>
  );
}

export default App;
