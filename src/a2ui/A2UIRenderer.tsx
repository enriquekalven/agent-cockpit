import React from 'react';
import { A2UIComponent } from './types';
import { Text, Button, Card, Image, List, StatBar } from './components';

const Registry: Record<string, React.FC<any>> = {
  Text,
  Button,
  Card,
  Image,
  List,
  StatBar,
  Container: Card, // Alias for common A2UI convention
};

export const A2UIRenderer: React.FC<{ component: A2UIComponent }> = ({ component }) => {
  const Component = Registry[component.type] || (() => <div className="unknown">Unknown: {component.type}</div>);

  const children = component.children?.map((child, i) => (
    <A2UIRenderer key={child.id || i} component={child} />
  )) || null;

  return (
    <Component {...component.props}>
      {children}
    </Component>
  );
};

export const A2UISurfaceRenderer: React.FC<{ surface: any }> = ({ surface }) => {
  return (
    <div className="a2-surface" id={surface.surfaceId}>
      {surface.content.map((comp: A2UIComponent, i: number) => (
        <A2UIRenderer key={comp.id || i} component={comp} />
      ))}
    </div>
  );
};
