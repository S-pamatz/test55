// handleNodeClick.js
// Description: This file contains the functions that are called when a node is clicked.
import Department from "../../assets/DepartmentW.png";
import Scholar from "../../assets/ScholarW.png";

// This function finds the descendants of a node and returns them in an array
export const findDescendants = (nodes, parentNode) => {
  let descendants = [];
  nodes.forEach((node) => {
    if (node.parent === parentNode.id) {
      descendants.push(node);
      descendants = descendants.concat(findDescendants(nodes, node));
    }
  });
  return descendants;
};

export const expandNodeUsingFilteredEntries = (
  nodes,
  links,
  clickedNode,
  filteredEntries
) => {
  let updatedNodes = [...nodes];
  let updatedLinks = [...links];
  const maxId = Math.max(...nodes.map((node) => node.id));
  const newNodes = filteredEntries.map((entry, index) => {
    console.log(entry);
    const name = entry.Name.split(" ");
    const affilateName = `${name[1]}, ${name[0]}`;
    return {
      id: maxId + 1 + index,
      userId: entry.id,
      Name: affilateName,
      Interest: entry.Interest,
      Department: entry.Department,
      Email: entry.Email,
      Membership: entry.Membership,
      URL: entry.URL,
      WSUCampus: entry.WSUCampus,
      expanded: false,
      parent: clickedNode.id,
      depth: clickedNode.depth + 1,
      radius: clickedNode.radius / 4,
      node: "affilate",
    };
  });

  newNodes.forEach((newNode) => {
    updatedLinks.push({
      source: newNode.id,
      target: clickedNode.id,
    });
  });

  const clickedNodeIndex = updatedNodes.findIndex(
    (n) => n.id === clickedNode.id
  );
  if (clickedNodeIndex !== -1) {
    updatedNodes[clickedNodeIndex].expanded = true;
  }

  updatedNodes = [...updatedNodes, ...newNodes];
  return { updatedNodes, updatedLinks };
};
// filter out the descendants of the clicked node with id and return the updated nodes and links
export const collapseNode = (nodes, links, clickedNode) => {
  if (!nodes.find((n) => n.id === clickedNode.id)) {
    return { updatedNodes: nodes, updatedLinks: links };
  }
  if (!clickedNode.expanded) {
    return { updatedNodes: nodes, updatedLinks: links };
  }
  const descendants = findDescendants(nodes, clickedNode);
  const descendantIds = descendants.map((n) => n.id);

  const updatedNodes = nodes.filter((n) => !descendantIds.includes(n.id));
  const updatedLinks = links.filter(
    (link) =>
      !descendantIds.includes(link.source.id) &&
      !descendantIds.includes(link.target.id)
  );

  const nodeIndex = updatedNodes.findIndex((n) => n.id === clickedNode.id);
  updatedNodes[nodeIndex] = { ...clickedNode, expanded: false };

  return { updatedNodes, updatedLinks };
};
// This is the function that will be called when a node is clicked
export const expandNode = (nodes, links, clickedNode, nodeLibrary) => {
  let updatedNodes = [...nodes];
  let updatedLinks = [...links];
  if (clickedNode.expanded) {
    return { updatedNodes, updatedLinks };
  }
  const children = nodeLibrary
    .filter((n) => n.parent === clickedNode.id)
    .map((child) => {
      return {
        ...child,
        depth: clickedNode.depth + 1,
        // radius: clickedNode.radius /2
      };
    });
  children.forEach((child) => {
    updatedLinks.push({
      source: child.id,
      target: clickedNode.id,
    });
  });
  updatedNodes = [...updatedNodes, ...children];

  const clickedNodeIndex = updatedNodes.findIndex(
    (n) => n.id === clickedNode.id
  );
  if (clickedNodeIndex !== -1) {
    updatedNodes[clickedNodeIndex] = {
      ...updatedNodes[clickedNodeIndex],
      expanded: true,
    };
  }
  return { updatedNodes, updatedLinks };
};
