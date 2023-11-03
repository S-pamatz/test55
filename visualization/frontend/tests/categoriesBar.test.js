import { render, screen, fireEvent } from '@testing-library/react';
import CategoriesBar from '../src/components/layouts/graphLayout/CategoriesBar';
import React from 'react';

test('checks if button with content "Universities" is present', () => {
    render(<CategoriesBar />);
  
    // Query for the button
    const universityButton = screen.getByRole('button', { name: /Universities/i });
  
    // Assert that the button is in the document
    expect(universityButton).toBeInTheDocument();
  });