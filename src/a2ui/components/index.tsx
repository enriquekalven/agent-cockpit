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

export const Image: React.FC<{ src: string; alt?: string; caption?: string }> = ({ src, alt, caption }) => {
  return (
    <div className="a2-image-container">
      <img src={src} alt={alt} className="a2-image" />
      {caption && <p className="a2-caption">{caption}</p>}
    </div>
  );
};

export const List: React.FC<{ items: string[]; title?: string }> = ({ items, title }) => {
  return (
    <div className="a2-list-container">
      {title && <h4 className="a2-list-title">{title}</h4>}
      <ul className="a2-list">
        {items.map((item, i) => (
          <li key={i} className="a2-list-item">{item}</li>
        ))}
      </ul>
    </div>
  );
};

export const StatBar: React.FC<{ label: string; value: number; color?: string }> = ({ label, value, color = '#3b82f6' }) => {
  return (
    <div className="a2-stat-bar-container">
      <div className="a2-stat-bar-label">
        <span>{label}</span>
        <span>{value}%</span>
      </div>
      <div className="a2-stat-bar-track">
        <div 
          className="a2-stat-bar-fill" 
          style={{ width: `${value}%`, backgroundColor: color }}
        />
      </div>
    </div>
  );
};
