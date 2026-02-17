import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import type { A2UIComponent } from '../types';

/**
 * A sample Lit-based A2UI component.
 * This demonstrates how A2UI can be rendered using standard Web Components.
 */
@customElement('a2-lit-renderer')
export class A2LitRenderer extends LitElement {
  @property({ type: Object }) component?: A2UIComponent;

  static styles = css`
    :host {
      display: block;
      font-family: var(--font-family, 'Inter', sans-serif);
    }
    .a2-lit-card {
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 1rem;
      margin-bottom: 1rem;
    }
    .a2-lit-text {
      color: #f3f4f6;
    }
  `;

  render() {
    if (!this.component) return html`<div>No component data</div>`;

    return html`
      <div class="a2-lit-card">
        ${this.component.type === 'Text' 
          ? html`<p class="a2-lit-text">${this.component.props?.text}</p>`
          : html`<div>Unknown: ${this.component.type}</div>`
        }
        <div class="children">
          ${this.component.children?.map(child => html`
            <a2-lit-renderer .component=${child}></a2-lit-renderer>
          `)}
        </div>
      </div>
    `;
  }
}
