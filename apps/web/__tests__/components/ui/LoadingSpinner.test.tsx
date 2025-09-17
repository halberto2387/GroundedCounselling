import { render, screen } from '@testing-library/react';
import { LoadingSpinner } from '../../../components/ui/LoadingSpinner';

describe('LoadingSpinner', () => {
  it('renders with default props', () => {
    render(<LoadingSpinner />);
    
    const spinner = screen.getByRole('status');
    expect(spinner).toBeInTheDocument();
    expect(spinner).toHaveAttribute('aria-label', 'Loading');
    
    const srText = screen.getByText('Loading...');
    expect(srText).toBeInTheDocument();
    expect(srText).toHaveClass('sr-only');
  });

  it('applies correct size classes', () => {
    const { rerender } = render(<LoadingSpinner size="small" />);
    let spinner = screen.getByRole('status');
    expect(spinner).toHaveClass('h-4', 'w-4');

    rerender(<LoadingSpinner size="medium" />);
    spinner = screen.getByRole('status');
    expect(spinner).toHaveClass('h-8', 'w-8');

    rerender(<LoadingSpinner size="large" />);
    spinner = screen.getByRole('status');
    expect(spinner).toHaveClass('h-12', 'w-12');
  });

  it('applies custom className', () => {
    render(<LoadingSpinner className="custom-class" />);
    
    const spinner = screen.getByRole('status');
    expect(spinner).toHaveClass('custom-class');
  });

  it('has correct animation and styling classes', () => {
    render(<LoadingSpinner />);
    
    const spinner = screen.getByRole('status');
    expect(spinner).toHaveClass('animate-spin');
    expect(spinner).toHaveClass('rounded-full');
    expect(spinner).toHaveClass('border-2');
    expect(spinner).toHaveClass('border-primary-200');
    expect(spinner).toHaveClass('border-t-primary-600');
  });
});