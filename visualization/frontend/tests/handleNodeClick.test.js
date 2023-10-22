// handleNodeClick.test.js
// Description: This file contains the functions that are called when a node is clicked.

import React from "react";
import { expandNode } from "../src/components/data/handleNodeClick";
import Department from "../src/components/assets/Department.png";

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
});

// Exceptiona C