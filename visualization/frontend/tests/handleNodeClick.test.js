// handleNodeClick.test.js
// Description: This file contains the functions that are called when a node is clicked.

import React from "react";
import { expandNode, collapseNode } from "../src/components/data/handleNodeClick";
import Department from "../src/assets/DepartmentW.png";

describe("expandNode function", () => {
  // Normal case
  test("should expand the clicked node and add children", () => {
    // Given
    const nodes = [{ id: 1, depth: 0, expanded: false }];
    const links = [];
    const clickedNode = { id: 1, depth: 0, expanded: false };
    const nodesLibrary = [
      { id: 1, depth: 0, expanded: false },
      { id: 2, parent: 1, Name: "Child 1" },
      { id: 3, parent: 1, Name: "Child 2" },
    ];
    // When
    const { updatedNodes, updatedLinks } = expandNode(
      nodes,
      links,
      clickedNode,
      nodesLibrary
    );
    // Then
    expect(updatedNodes).toEqual([
      { id: 1, depth: 0, expanded: true },
      { id: 2, parent: 1, Name: "Child 1", depth: 1, icon: Department },
      { id: 3, parent: 1, Name: "Child 2", depth: 1, icon: Department },
    ]);
    expect(updatedLinks).toEqual([
      { source: 2, target: 1 },
      { source: 3, target: 1 },
    ]);
  });
  // Boundary Case
  // Clicked node is not in the nodes data.
  test(" should not expand the clicked node and add children", () => {
    const nodes = [{ id: 1, depth: 0, expanded: false }];
    const links = [];
    const clickedNode = { id: 2, depth: 0, expanded: false };
    const nodesLibrary = [
      { id: 1, depth: 0, expanded: false },
      { id: 2, parent: 1, Name: "Child 1" },
      { id: 3, parent: 1, Name: "Child 2" },
    ];
    const { updatedNodes, updatedLinks } = expandNode(
      nodes,
      links,
      clickedNode,
      nodesLibrary
    );
    expect(updatedNodes).toEqual([{ id: 1, depth: 0, expanded: false }]);
    expect(updatedLinks).toEqual([]);
  });
  // Exception case: Clicked node is already expanded
  test("should not add children if clicked node is already expanded", () => {
    // Given
    const nodes = [
      { id: 1, depth: 0, expanded: true },
      { id: 2, parent: 1, Name: "Child 1", depth: 1 },
      { id: 3, parent: 1, Name: "Child 2", depth: 1 },
    ];
    const links = [
      { source: 2, target: 1 },
      { source: 3, target: 1 },
    ];
    const clickedNode = { id: 1, depth: 0, expanded: true };
    const nodesLibrary = [
      { id: 1, depth: 0, expanded: true },
      { id: 2, parent: 1, Name: "Child 1", depth: 1 },
      { id: 3, parent: 1, Name: "Child 2", depth: 1 },
      { id: 4, parent: 1, Name: "Child 3" }, // Additional child to test if it gets added or not
    ];
    // When
    const { updatedNodes, updatedLinks } = expandNode(
      nodes,
      links,
      clickedNode,
      nodesLibrary
    );
    // Then
    expect(updatedNodes).toEqual([
      { id: 1, depth: 0, expanded: true },
      { id: 2, parent: 1, Name: "Child 1", depth: 1 },
      { id: 3, parent: 1, Name: "Child 2", depth: 1 },
    ]);
    expect(updatedLinks).toEqual([
      { source: 2, target: 1 },
      { source: 3, target: 1 },
    ]);
  });
});

// testing CollapseNode function
describe("collapseNode function", () => {
  // Normal case
  // Clicked node has descendants
  test("should collapse the clicked node and remove all its descendants", () => {
    // Given
    const nodes = [
      { id: 1, depth: 0, expanded: true },
      { id: 2, parent: 1, depth: 1 },
      { id: 3, parent: 1, depth: 1 },
      { id: 4, parent: 2, depth: 2 }
    ];
    const links = [
      { source: { id: 1 }, target: { id: 2 } },
      { source: { id: 1 }, target: { id: 3 } },
      { source: { id: 2 }, target: { id: 4 } }
    ];
    const clickedNode = { id: 1, depth: 0, expanded: true };
  
    // When
    const { updatedNodes, updatedLinks } = collapseNode(nodes, links, clickedNode);
  
    // Then
    expect(updatedNodes).toEqual([{ ...clickedNode, expanded: false }]);
    expect(updatedLinks).toEqual([]);
  });
  // Boundary case
  // Clicked node has no descendants
  test("should handle collapse when there are no descendants", () => {
    // Given
    const nodes = [
      { id: 1, depth: 0, expanded: false },
      { id: 2, parent: 1, depth: 1, expanded: false },
      { id: 3, parent: 1, depth: 1, expanded: false }
    ];
    const links = [
      { source: { id: 1 }, target: { id: 2 } },
      { source: { id: 1 }, target: { id: 3 } },
    ];
    const clickedNode = { id: 1, depth: 0, expanded: false };
  
    // When
    const { updatedNodes, updatedLinks } = collapseNode(nodes, links, clickedNode);
  
    // Then
    expect(updatedNodes).toEqual(nodes);
    expect(updatedLinks).toEqual(links);
  });
  // Exception case
  // Clicked node is not in the nodes data
  test("should handle the scenario when clicked node is not found", () => {
    // Given
    const nodes = [
      { id: 1, depth: 0, expanded: true },
      { id: 2, parent: 1, depth: 1 }
    ];
    const links = [      { source: { id: 1 }, target: { id: 2 } }];
    const clickedNode = { id: 3, depth: 0, expanded: true };
  
    // When
    const { updatedNodes, updatedLinks } = collapseNode(nodes, links, clickedNode);
  
    // Then
    expect(updatedNodes).toEqual(nodes);
    expect(updatedLinks).toEqual(links);
  });
});
  
  
