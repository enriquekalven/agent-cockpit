export interface A2UIComponent {
  type: string;
  id?: string;
  props?: Record<string, any>;
  children?: A2UIComponent[];
}

export interface A2UISurface {
  surfaceId: string;
  content: A2UIComponent[];
  data?: Record<string, any>;
}

export interface A2UIMessage {
  surfaces: A2UISurface[];
}
