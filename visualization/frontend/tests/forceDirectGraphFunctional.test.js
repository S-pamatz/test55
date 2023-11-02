import { render, screen, waitFor } from '@testing-library/react';
import ForceDirectGraph from '../src/components/graphComponents/ForceDirectGraph';
import React from 'react';
import { GraphContext, GraphContextProvider } from '../src/components/data/GraphContext';
screen.debug();

jest.mock('d3');

const MockGraphProvider = ({ children }) => {
    screen.debug();
    const mockContextValue = {
        nodes: [
            {
                id: 0,
                Name: 'Universities',
                icon: 'University',
                expanded: false,
                depth: 0,
                fx: 500,
                fy: 400,
            },
        ],
        links: [],
        selectedNode: null,
        onNodeClick: jest.fn(),
        onSearchClick: jest.fn(),
        updateNode: jest.fn(),
        setStartingNode: jest.fn(),
    };
    return (
      <GraphContextProvider value={mockContextValue}>
        {children}
      </GraphContextProvider>
    );
};


test('renders ForceDirectGraph with provided context', () => {
    render(
      <MockGraphProvider>
        <ForceDirectGraph />
      </MockGraphProvider>
    );
  
    const forceGraph = screen.getByTestId('force-graph');
    expect(forceGraph).toBeInTheDocument();
  });

  test('should have an initial node(root)', async () => {
    const {container} = render(
      <MockGraphProvider>
        <ForceDirectGraph />
      </MockGraphProvider>
    );
    await waitFor(() => {
        const nodeGroup = container.querySelector("[data-testid='node-0']");
        // expect(nodeGroup.classList.toString()).toContain('nodeGroup');
    });
    

  });
  





