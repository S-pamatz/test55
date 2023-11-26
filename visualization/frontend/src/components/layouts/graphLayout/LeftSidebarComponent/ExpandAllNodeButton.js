import React, { useContext } from "react";
import GraphContext from "../../../data/GraphContext";

const ExpandAllNodeButton = () => {
    const ctx = useContext(GraphContext);
    
    const expandAllNodes = () => {
        ctx.expandAllNodes();
    };
    
    return (
        <button className="expand-all-nodes-button" onClick={expandAllNodes}>
        Expand All Nodes
        </button>
    );
    };

export default ExpandAllNodeButton;