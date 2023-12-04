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
import {
  findBestMatchingNode,
  useHighlightPath,
} from "../function/searchHelper";
import batchExpandNodeLogic from "../function/batchExpandNodeLogic";

const GraphContext = createContext({
  nodes: [],
  links: [],
  selectedNode: null,
  expandAllNodes: () => {},
  setNodes: (newNodes) => {},
  onNodeClick: (clickedNode) => {},
  onSearchClick: (search) => {},
  updateNode: (index, newProps) => {},
  setStartingNode: (newNode) => {},
});

export const GraphContextProvider = (props) => {
  const [nodes, setNodes] = useState([
    {
      id: 1,
      Name: "Universities",
      icon: University,
      expanded: false,
      fx: 500,
      fy: 400,
      depth: 0,
    },
  ]);
  const [links, setLinks] = useState([]);

  const updateNode = (index, newProps) => {
    const updatedNodes = [...nodes];
    updatedNodes[index] = { ...updatedNodes[index], ...newProps };
    setNodes(updatedNodes);
  };

  const setStartingNode = (newNode) => {
    setNodes([newNode]);
    setLinks([]);
  };

  const [selectedNode, setSelectedNode] = useState(null);

  const highlightPath = useHighlightPath();

  const handleNodesClick = async (clickedNode) => {
    let updatedNodes = [];
    let updatedLinks = [];

    if (clickedNode.node === "searchNode") {
      ({ updatedNodes, updatedLinks } = await expandNodeLogic(clickedNode, "Affiliate"));
    } else {
      // Add 'await' to wait for the async function to resolve
      ({ updatedNodes, updatedLinks } = await expandNodeLogic(clickedNode, "Normal"));
    }

    // Check if the returned values are defined
    if (!updatedNodes || !updatedLinks) return;

    // Update the state with the new values
    setNodes(updatedNodes);
    setLinks(updatedLinks);
  };

  const handleSearchClick = async (search) => {
    if (!search) return;
    const highlightColor = "#4d4d4d";

    let updatedNodes = [...nodes];
    let updatedLinks = [...links];

    // Use the search helper function to find the best matching node
    const bestMatchNode = findBestMatchingNode(search, nodes);

    if (bestMatchNode) {
      const result = highlightPath(
        updatedNodes,
        updatedLinks,
        bestMatchNode,
        highlightColor
      );
      updatedNodes = result.updatedNodes;
      updatedLinks = result.updatedLinks;
    } else {
      try {
        const filteredEntries = await filterEntries(search);
        console.log("nodes: ", nodes);
        console.log("updatedNodes: ", updatedNodes);
        updatedNodes = [];
        updatedLinks = [];
        if (!filteredEntries || filteredEntries.length === 0) return;

        const entry = filteredEntries[0];

        let nameNode = {
          id: 0,
          Name: entry.Name,
          Interest: entry.Interest,
          Department: entry.Department,
          Email: entry.Email,
          Membership: entry.Membership,
          URL: entry.URL,
          WSUCampus: entry.WSUCampus,
          expanded: false,
          node: "searchNode",
          fx: 500,
          fy: 400,
        };
        updatedNodes.push(nameNode);
        updatedLinks.push({ source: updatedNodes[0].id, target: nameNode.id });
      } catch (error) {
        console.error("Error searching and expanding nodes:", error);
      }
    }
    setNodes([...updatedNodes]);
    setLinks([...updatedLinks]);
  };
  const expandAllNodes = async (currentNodes, tempNodes, tempLinks) => {
    if (!currentNodes || currentNodes.length === 0) {
      return { tempNodes, tempLinks };
    }

    for (const node of currentNodes) {
      // Check if the node exists in the tempNodes array
      if (!tempNodes.find((n) => n.id === node.id)) {
        console.error(`Node not found: ${node.id}`);
        continue; // Skip to the next node
      }

      if (!node.expanded && node.node !== "affiliate") {
        console.log("tempNodes: ", tempNodes);
        const { updatedNodes, updatedLinks } = await batchExpandNodeLogic(
          node,
          tempNodes,
          tempLinks
        );
        tempNodes = updatedNodes;
        tempLinks = updatedLinks;

        // Get newly added child nodes to expand next
        const newChildNodes = tempNodes.filter(
          (n) => n.parent === node.id && n.node !== "affiliate"
        );

        // Recursively expand child nodes
        const result = await expandAllNodes(
          newChildNodes,
          tempNodes,
          tempLinks
        );
        tempNodes = result.tempNodes;
        tempLinks = result.tempLinks;
      }
    }

    return { tempNodes, tempLinks };
  };

  const startExpandAllNodes = async () => {
    const { tempNodes, tempLinks } = await expandAllNodes(
      nodes,
      [...nodes],
      [...links]
    );
    setNodes(tempNodes);
    setLinks(tempLinks);
  };

  const expandNodeLogic = async (logicNode, expandType) => {
    if (!nodes.find((n) => n.id === logicNode.id)) {
      console.error(`Node not found: ${logicNode.id}`);
      return; // Exit the function
    }
    let updatedNodes = [...nodes];
    let updatedLinks = [...links];
    // for when node is selected from filter
    const parentNode = nodesLibrary.find(
      (node) => node.id === logicNode.parent
    );
    const isParentNode =
      parentNode && (parentNode.Name === "WSU" || parentNode.Name === "Others");
    const isInNodeLibrary = nodesLibrary.some(
      (node) => node.Name === logicNode.Name
    );

    if (logicNode.node === "affilate" || logicNode.node === "searchNode") {
      if (!isInNodeLibrary) {
        setSelectedNode(logicNode);
      }
      // Return current state if no expansion is needed
      return { updatedNodes, updatedLinks };
    }

    if (logicNode.node === "affilate") {
      return; // Early return if the node is not a top-level node
    }
    if (logicNode.expanded) {
      ({ updatedNodes, updatedLinks } = collapseNode(nodes, links, logicNode));
    } else {
      if (expandType === "Normal") {
        if (logicNode.Name === "Others") {
          ({ updatedNodes, updatedLinks } = expandNode(
            nodes,
            links,
            logicNode,
            nodesLibrary
          ));
        } else if (logicNode.depth >= 2 || isParentNode) {
          try {
            const filteredEntries = await filterEntries(logicNode.Name);
            ({ updatedNodes, updatedLinks } = expandNodeUsingFilteredEntries(
              nodes,
              links,
              logicNode,
              filteredEntries
            ));
          } catch (error) {
            console.error("Error expanding node:", error);
            return;
          }
        }else {
          // If the node is a top-level node (depth = 0) and it is not expanded, expand it using the nodeLibrary
          ({ updatedNodes, updatedLinks } = expandNode(
            nodes,
            links,
            logicNode,
            nodesLibrary
          ));
        }
      } else {
        // If the node is a top-level node (depth = 0) and it is not expanded, expand it using the nodeLibrary
        ({ updatedNodes, updatedLinks } = expandNode(
          nodes,
          links,
          logicNode,
          nodesLibrary
        ));
      }
    }
    return { updatedNodes, updatedLinks };
  };

  return (
    <GraphContext.Provider
      value={{
        nodes: nodes,
        links: links,
        selectedNode: selectedNode,
        setNodes: setNodes,
        expandAllNodes: startExpandAllNodes,
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
