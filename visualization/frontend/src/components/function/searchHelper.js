import { useContext } from "react";
import GraphContext from "../data/GraphContext";

export const useHighlightPath = () => {
    const ctx = useContext(GraphContext);
    const nodes = ctx.nodes;
    

    const highlightPath = (targetNode) => {
        console.log("targetNode: ", targetNode);

        // Create a new array with updated nodes
        const updatedNodes = nodes.map(node => {
            if (node.id === targetNode.id || node.id === targetNode.parent) {
                return { ...node, fill: "red" };
            }
            return node;
        });

        return updatedNodes;
    };

    return  highlightPath ;

};

// export const useHighlightPath = () => {
//   const { nodes, links, setNodes, setLinks } = useContext(GraphContext);

//   const changeNodeColor = (nodeId, color) => {
//     const node = nodes.find((node) => node.id === nodeId);
//     if (node) {
//       node.fill = color;
//     }
//   };

//   const changeLinkColorAndThickness = (source, target, color, thickness) => {
//     const link = links.find((link) => link.source === source && link.target === target);
//     if (link) {
//       link.color = color;
//       link.thickness = thickness;
//     }
//   };

//   const recursivelyHighlight = (node) => {
//     if (node) {
//       changeNodeColor(node.id, "red");
//       if (node.parent !== undefined) {
//         changeLinkColorAndThickness(node.parent, node.id, "red", 2); // Change color and thickness of link
//         const parentNode = nodes.find((n) => n.id === node.parent);
//         recursivelyHighlight(parentNode);
//       }
//     }
//   };

//   return { highlightPath: recursivelyHighlight };
// };

