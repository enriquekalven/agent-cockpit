import React, { useEffect, useRef } from 'react';

/**
 * Improvement #2: Automated A2UI Surface Discovery
 * 
 * An HOC that automatically injects data-surface-id based on the component name
 * or a provided ID. This reduces manual instrumentation effort.
 */
export function withSurfaceDiscovery<P extends object>(
  Component: React.ComponentType<P>,
  surfaceId?: string
) {
  return function SurfaceManager(props: P) {
    const id = surfaceId || Component.displayName || Component.name || 'anonymous-surface';
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => {
      if (ref.current) {
        ref.current.setAttribute('data-surface-id', id);
        ref.current.setAttribute('data-a2ui-discovered', 'true');
        console.debug(`[A2UI] Surface discovered: ${id}`);
      }
    }, [id]);

    return (
      <div ref={ref} className="a2ui-surface-wrapper" style={{ display: 'contents' }}>
        <Component {...props} />
      </div>
    );
  };
}

/**
 * AutoSurface component for declarative surface marking.
 */
export const AutoSurface: React.FC<{ id?: string; children: React.ReactNode }> = ({ id, children }) => {
  const ref = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (ref.current && id) {
      ref.current.setAttribute('data-surface-id', id);
    }
  }, [id]);

  return (
    <div ref={ref} className="a2ui-auto-surface" style={{ display: 'contents' }}>
      {children}
    </div>
  );
};
