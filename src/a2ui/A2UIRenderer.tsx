import React from 'react';
import { A2UIComponent } from './types';
import { Text, Button, Card, Image, List, StatBar, Grid, Metric, Visual } from './components';

const Registry: Record<string, React.FC<any>> = {
  Text,
  Button,
  Card,
  Image,
  List,
  StatBar,
  Container: Card, // Alias for common A2UI convention
  Grid,
  Metric,
  Visual,
};

export const A2UIRenderer: React.FC<{ component: A2UIComponent }> = React.memo(({ component }) => {
  const Component = Registry[component.type] || (() => <div className="unknown">Unknown: {component.type}</div>);

  // v1.0 Autonomous Accessibility Injection
  const autoProps = { ...component.props };
  if (component.type === 'Text' && !autoProps.role) {
    autoProps.role = 'status';
    autoProps['aria-live'] = 'polite';
  }

  const children = component.children?.map((child, i) => (
    <A2UIRenderer key={child.id || i} component={child} />
  )) || null;

  return (
    <Component {...autoProps}>
      {children}
    </Component>
  );
}, (prev, next) => {
  // Deep comparison of component structure to prevent unnecessary re-renders
  return prev.component.id === next.component.id &&
    JSON.stringify(prev.component.props) === JSON.stringify(next.component.props) &&
    prev.component.children?.length === next.component.children?.length;
});

export const A2UISurfaceRenderer: React.FC<{ surface: any }> = ({ surface }) => {
  return (
    <div className="a2-surface" id={surface.surfaceId} role="main" aria-label="Agent Reasoning Surface">
      {surface.content.map((comp: A2UIComponent, i: number) => (
        <A2UIRenderer key={comp.id || i} component={comp} />
      ))}
    </div>
  );
};
