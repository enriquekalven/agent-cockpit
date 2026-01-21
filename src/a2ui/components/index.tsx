import React from 'react';

export const Text: React.FC<{ text: string; variant?: 'h1' | 'h2' | 'body' }> = ({ text, variant = 'body' }) => {
  if (variant === 'h1') return <h1 className="a2-h1">{text}</h1>;
  if (variant === 'h2') return <h2 className="a2-h2">{text}</h2>;
  return <p className="a2-body">{text}</p>;
};

export const Button: React.FC<{ label: string; onClick?: () => void; variant?: 'primary' | 'secondary' }> = ({ label, onClick, variant = 'primary' }) => {
  return (
    <button className={`a2-button ${variant}`} onClick={onClick}>
      {label}
    </button>
  );
};

export const Card: React.FC<{ children: React.ReactNode; title?: string }> = ({ children, title }) => {
  return (
    <div className="a2-card">
      {title && <h3 className="a2-card-title">{title}</h3>}
      <div className="a2-card-content">{children}</div>
    </div>
  );
};
