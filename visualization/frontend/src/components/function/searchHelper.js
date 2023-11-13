import { useContext } from "react";
import GraphContext from "../data/GraphContext";

// searchHelper.js
export const findBestMatchingNode = (search, nodes) => {
  if (!search) return null;

  const searchWords = search.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "")
                            .toLowerCase()
                            .split(/\s+/)
                            .map(word => word.trim());

  let bestMatchNode = null;
  let highestScore = 0;

  nodes.forEach(node => {
    const nodeWords = node.Name.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "")
                               .toLowerCase()
                               .split(/\s+/)
                               .map(word => word.trim());

    let score = searchWords.reduce((acc, searchWord) => {
      return acc + (nodeWords.includes(searchWord) ? 1 : 0);
    }, 0);

    if (score > highestScore) {
      highestScore = score;
      bestMatchNode = node;
    }
  });

  return bestMatchNode;
};

export const useHighlightPath = () => {
  const highlightPath = (nodes, links, targetNode, highlightColor) => {
      let updatedNodes = [...nodes];
      let updatedLinks = [...links];

      const highlightNodeAndParents = (currentNode) => {
          const nodeIndex = updatedNodes.findIndex(node => node.id === currentNode.id);
          if (nodeIndex !== -1) {
              updatedNodes[nodeIndex] = { ...updatedNodes[nodeIndex], fill: highlightColor };

              const parentNodeId = updatedNodes[nodeIndex].parent;
              if (parentNodeId !== null && parentNodeId !== undefined) {
                  const parentNode = updatedNodes.find(node => node.id === parentNodeId);
                  if (parentNode) {
                      // Highlight the link between the current node and its parent
                      const linkIndex = updatedLinks.findIndex(link => 
                          link.source.id  === currentNode.id && 
                          link.target.id  === currentNode.parent
                      );
                      console.log(linkIndex);
                      console.log(updatedLinks);
                      if (linkIndex !== -1) {
                          updatedLinks[linkIndex] = { ...updatedLinks[linkIndex], stroke: highlightColor, strokeWidth: '3px' };
                      }

                      highlightNodeAndParents(parentNode);
                  }
              }
          }
      };

      highlightNodeAndParents(targetNode);
      return { updatedNodes, updatedLinks };
  };

  return highlightPath;
};