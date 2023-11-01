import { render, screen, waitFor } from '@testing-library/react';
import ForceDirectGraph from '../src/components/graphComponents/ForceDirectGraph';
import React from 'react';
import { GraphContext, GraphContextProvider } from '../src/components/data/GraphContext';
screen.debug();

jest.mock('d3');

const MockGraphProvider = ({ children }) => {
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
        expect(nodeGroup.classList.toString()).toContain('nodeGroup');
    });
    

  });
  





// import React from 'react';
// import { render, screen, waitFor, within } from '@testing-library/react';
// import ForceDirectGraph from '../src/components/graphComponents/ForceDirectGraph';
// import GraphContext from '../src/components/data/GraphContext';

// jest.mock('d3');

// test('should have an initial node(root)',async () => {
//     // Mock the context value that your component expects
//     const mockContextValue = {
//         nodes: [
//             {
//                 id: 0,
//                 Name: 'Universities',
//                 icon: 'University',
//                 expanded: false,
//                 depth: 0,
//                 fx: 500,
//                 fy: 400,
//             },
//         ],
//         links: [],
//     };

//     // Wrap your component with the context provider and provide the mock value
//     render(
//         <GraphContext.Provider value={mockContextValue}>
//             <ForceDirectGraph />
//         </GraphContext.Provider>
//     );
    
//     const nodeGroup = screen.getByTestId('nodeGroup');
//     expect(nodeGroup).toBeInTheDocument();
    
//     // Additionally, you can check other attributes or content
//     const circle = within(nodeGroup).getByRole('img'); // Assuming the <circle> represents the node
//     expect(circle).toHaveAttribute('r', '40'); // Check if the radius is correct
  
//     const text = within(nodeGroup).getByText('UNI');
//     expect(text).toBeInTheDocument();
//   });
