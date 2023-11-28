
import nodesLibrary from "../data/nodeLibrary";
import { filterEntries } from "../data/getDataFromBackend";
import { expandNode, expandNodeUsingFilteredEntries, collapseNode } from "../data/handleNodeClick";

const batchExpandNodeLogic = async (logicNode, localNodes, localLinks) => {
    console.log("localNodes: ", localNodes);
    console.log("localLinks: ", localLinks);
    if (!localNodes.find(n => n.id === logicNode.id)) {
        console.error(`Node not found in local array: ${logicNode.id}`);
        return { localNodes, localLinks }; // Exit the function
    }
    let updatedNodes = [...localNodes];
    let updatedLinks = [...localLinks];
    // for when node is selected from filter
    const parentNode = nodesLibrary.find(
      (node) => node.id === logicNode.parent
    );
    const isParentNode =
      parentNode && (parentNode.Name === "WSU" || parentNode.Name === "Others");
    const isInNodeLibrary = nodesLibrary.some(
      (node) => node.Name === logicNode.Name
    );

    if (logicNode.node === "affilate") {
    //   if (!isInNodeLibrary) {
    //     setSelectedNode(logicNode);
    //   }
      // Return current state if no expansion is needed
      return { updatedNodes, updatedLinks };
    }

    if (logicNode.node === "affilate") {
      return; // Early return if the node is not a top-level node
    }
    if (logicNode.expanded) {
      ({ updatedNodes, updatedLinks } = collapseNode(localNodes, localLinks, logicNode));
    } else {
      if (logicNode.id === 46) {
        ({ updatedNodes, updatedLinks } = expandNode(
          localNodes,
          localLinks,
          logicNode,
          nodesLibrary
        ));
      } else if (logicNode.depth >= 2 || isParentNode) {
        try {
          const filteredEntries = await filterEntries(logicNode.Name);
          ({ updatedNodes, updatedLinks } = expandNodeUsingFilteredEntries(
            localNodes,
            localLinks,
            logicNode,
            filteredEntries
          ));
        } catch (error) {
          console.error("Error expanding node:", error);
          return;
        }
      } else {
        // If the node is a top-level node (depth = 0) and it is not expanded, expand it using the nodeLibrary
        ({ updatedNodes, updatedLinks } = expandNode(
          localNodes,
          localLinks,
          logicNode,
          nodesLibrary
        ));
        const nodeIndex = updatedNodes.findIndex(n => n.id === logicNode.id);
        updatedNodes[nodeIndex] = { ...updatedNodes[nodeIndex], expanded: true };
      }
    }
    return { updatedNodes, updatedLinks };
  };

export default batchExpandNodeLogic;