// GraphContext.js
// Description: This file contains the context provider for the graph.
import React, { createContext, useState } from "react";
import {
  expandNode,
  collapseNode,
  expandNodeUsingFilteredEntries,
} from "./handleNodeClick";
import { filterEntries } from "./getDataFromBackend";
import University from "../../assets/UniversityW.png";
import { nodesLibrary } from "./nodeLibrary";
const GraphContext = createContext({
  nodes: [],
  links: [],
  selectedNode: null,
  onNodeClick: (clickedNode) => {},
  onSearchClick: (search) => {},
  updateNode: (index, newProps) => {},
  setStartingNode: (newNode) => {},
});

export const GraphContextProvider = (props) => {
  const [nodes, setNodes] = useState([
    { id: 0, Name: "wsu", icon: University, expanded: false, fx: 500, fy: 400, depth: 0},
  ]);
  const [links, setLinks] = useState([]);

  const updateNode = (index, newProps) => {
    const updatedNodes = [...nodes];
    updatedNodes[index] = { ...updatedNodes[index], ...newProps };
    setNodes(updatedNodes);
  };

  const setStartingNode = (newNode) => {
    // You can add logic here if needed.
    setNodes([newNode]);
  };

  // const contextValue = {
  //   nodes: nodes,
  //   updateNode: updateNode,
  //   // ... any other values/functions
  // };

  const [selectedNode, setSelectedNode] = useState(null);

  const handleNodesClick = async (clickedNode) => {

    if (clickedNode.depth === 2 && clickedNode != null ) {
      setSelectedNode(clickedNode);
    }

    if (clickedNode.depth >= 2) {
      return; // Early return if the node is not a top-level node
    }
    let updatedNodes, updatedLinks;
    if (clickedNode.expanded) {
      ({ updatedNodes, updatedLinks } = collapseNode(
        nodes,
        links,
        clickedNode
      ));
    } else {
      if (clickedNode.depth >= 1 ) { // If the node is a top-level node (depth = 1) and it is not expanded, expand it
        try {
          const filteredEntries = await filterEntries(clickedNode.Name);
          ({ updatedNodes, updatedLinks } = expandNodeUsingFilteredEntries(
            nodes,
            links,
            clickedNode,
            filteredEntries
          ));
        } catch (error) {
          console.error("Error expanding node:", error);
          return;
        }
      } else { // If the node is a top-level node (depth = 0) and it is not expanded, expand it using the nodeLibrary
        ({ updatedNodes, updatedLinks } = expandNode(
          nodes,
          links,
          clickedNode, nodesLibrary
        ));
      }
    }

    setNodes(updatedNodes);
    setLinks(updatedLinks);
  };

  const handleSearchClick = async (search) => {
    if (!search) return; // If search is empty, do nothing

    try {
      const filteredEntries = await filterEntries(search);

      if (!filteredEntries || filteredEntries.length === 0) return;

      const entry = filteredEntries[0];

      // Insert or find Department node
      let departmentNode = nodes.find(
        (node) => node.Name === entry.Department
      );
      if (!departmentNode) {
        departmentNode = {
          id: nodes.length,
          Name: entry.Department,
          expanded: false,
          fill: '#9D2235',
        };
        nodes.push(departmentNode);
        links.push({ source: 0, target: departmentNode.id }); // 0 is the ID for WSU
      } else {
        departmentNode.fill = '#9D2235';
      }

      // Insert or find the Name node and link it to the Department
      let nameNode = nodes.find((node) => node.Name === entry.Name);
      if (!nameNode) {
        nameNode = {
          id: nodes.length,
          Name: entry.Name,
          expanded: false,
          fill: '#9D2235',
        };
        nodes.push(nameNode);
        links.push({ source: departmentNode.id, target: nameNode.id });
      } else {
        nameNode.fill = '#9D2235';
      }

      // Update state
      setNodes([...nodes]);
      setLinks([...links]);
    } catch (error) {
      console.error("Error searching and expanding nodes:", error);
    }
  };

  return (
    <GraphContext.Provider
      value={{
        nodes: nodes,
        links: links,
        selectedNode: selectedNode,
        onNodeClick: handleNodesClick,
        onSearchClick: handleSearchClick,
        updateNode: updateNode, 
        setStartingNode: setStartingNode,
      }}
    >
      {props.children}
    </GraphContext.Provider>
  );
};
export default GraphContext;
