import{d as a,j as e,A as s}from"./index-KckVPtqI.js";import{R as t,T as i,S as n,B as c}from"./terminal-1RDQCk7f.js";import{S as d}from"./shield-oUVbMBqB.js";import{Z as l}from"./zap-wgUBvx6J.js";import{P as m}from"./panels-top-left-ClD0SwLU.js";const p=[{title:"Mission Control",desc:'The high-level "Why" and "How" for leadership and customers. Perfect for architectural alignment.',icon:e.jsx(t,{size:24}),color:"#3b82f6",path:"/docs/story"},{title:"Adversarial Red-Team",desc:"Simulate prompt injections and PII leaks with the Red Team SME persona.",icon:e.jsx(d,{size:24}),color:"#ef4444",path:"/docs/redteam-guide"},{title:"FinOps Optimizer",desc:"Identify token waste and apply automated fixes to reduce costs by up to 90%.",icon:e.jsx(l,{size:24}),color:"#f59e0b",path:"/docs/finops-guide"},{title:"SME Persona Matrix",desc:"Technical deep-dives into Architect, Quality, Security, and Ops SME standards.",icon:e.jsx(s,{size:24}),color:"#10b981",path:"/docs/audit-guide"},{title:"The Master Center",desc:"Full repository of CLI commands, UVX portable audits, and cockpit dashboard guides.",icon:e.jsx(i,{size:24}),color:"#8b5cf6",path:"/docs/commands-master"},{title:"A2UI Visual Face",desc:"Audit and implement the Generation UI standard for adaptive agentic surfaces.",icon:e.jsx(m,{size:24}),color:"#ec4899",path:"/docs/ux-guide"},{title:"Production Readiness",desc:'The final "go-to-production" gates, checklists, and deployment masterclass.',icon:e.jsx(n,{size:24}),color:"#0ea5e9",path:"/docs/production-checklist"},{title:"Governance & PRD",desc:"Product requirements, roadmaps, and long-term architectural constraints.",icon:e.jsx(c,{size:24}),color:"#94a3b8",path:"/docs/prd"}],v=()=>{const r=a();return e.jsxs("div",{className:"doc-home-v2",children:[e.jsxs("header",{className:"doc-home-hero",children:[e.jsx("div",{className:"accent-pill",children:"Documentation Hub"}),e.jsxs("h1",{children:["Welcome to the ",e.jsx("span",{className:"gradient-text",children:"Cockpit"})]}),e.jsx("p",{children:"Your guide to building, governing, and scaling production AI agents on Google Cloud."}),e.jsxs("div",{className:"quick-actions",children:[e.jsxs("button",{onClick:()=>r("/docs/getting-started"),className:"primary-doc-btn",children:[e.jsx(t,{size:18}),"Start Building"]}),e.jsxs("button",{onClick:()=>r("/docs/commands-master"),className:"secondary-doc-btn",children:[e.jsx(i,{size:18}),"View CLI Reference"]})]})]}),e.jsx("section",{className:"feature-tiles-grid",children:p.map(o=>e.jsxs("div",{className:"feature-tile",onClick:()=>r(o.path),style:{"--tile-color":o.color},children:[e.jsx("div",{className:"tile-icon-box",children:o.icon}),e.jsx("h3",{children:o.title}),e.jsx("p",{children:o.desc}),e.jsxs("div",{className:"tile-footer",children:[e.jsx("span",{children:"Learn more"}),e.jsx(h,{size:14})]})]},o.title))}),e.jsx("style",{children:`
        .doc-home-v2 {
          padding-top: 2rem;
        }
        .doc-home-hero {
          margin-bottom: 5rem;
          text-align: left;
        }
        .accent-pill {
          display: inline-block;
          background: rgba(var(--primary-color-rgb), 0.1);
          color: var(--primary-color);
          padding: 0.25rem 0.75rem;
          border-radius: 99px;
          font-size: 0.75rem;
          font-weight: 800;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          margin-bottom: 1.5rem;
        }
        .doc-home-hero h1 {
          font-size: 3.5rem;
          font-weight: 900;
          letter-spacing: -0.04em;
          margin-bottom: 1.5rem;
        }

        .doc-home-hero p {
          font-size: 1.25rem;
          color: var(--text-secondary);
          max-width: 600px;
          line-height: 1.6;
          margin-bottom: 3rem;
        }
        .quick-actions {
          display: flex;
          gap: 1rem;
        }
        .primary-doc-btn, .secondary-doc-btn {
          padding: 0.75rem 1.5rem;
          border-radius: 10px;
          font-weight: 700;
          font-size: 0.9rem;
          display: flex;
          align-items: center;
          gap: 0.75rem;
          cursor: pointer;
          transition: all 0.2s;
        }
        .primary-doc-btn {
          background: var(--primary-color);
          color: white;
          border: none;
          box-shadow: 0 4px 12px rgba(var(--primary-color-rgb), 0.2);
        }
        .secondary-doc-btn {
          background: transparent;
          border: 1px solid var(--border-color);
          color: var(--text-primary);
        }
        .primary-doc-btn:hover { transform: translateY(-2px); }
        .secondary-doc-btn:hover { background: rgba(var(--text-primary-rgb), 0.05); }

        .feature-tiles-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
          gap: 1.5rem;
          margin-bottom: 4rem;
        }
        .feature-tile {
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: 16px;
          padding: 2rem;
          cursor: pointer;
          transition: all 0.3s ease;
          position: relative;
          overflow: hidden;
          display: flex;
          flex-direction: column;
        }
        .feature-tile:hover {
          transform: translateY(-5px);
          border-color: var(--tile-color);
          box-shadow: 0 15px 30px rgba(0,0,0,0.05);
        }
        .feature-tile::before {
          content: '';
          position: absolute;
          top: -20%;
          right: -20%;
          width: 50%;
          height: 50%;
          background: radial-gradient(circle, var(--tile-color), transparent 70%);
          opacity: 0.05;
          transition: opacity 0.3s;
        }
        .feature-tile:hover::before { opacity: 0.15; }
        
        .tile-icon-box {
          width: 48px;
          height: 48px;
          border-radius: 12px;
          background: rgba(var(--text-primary-rgb), 0.05);
          display: flex;
          align-items: center;
          justify-content: center;
          margin-bottom: 1.5rem;
          color: var(--tile-color);
          border: 1px solid transparent;
          transition: all 0.3s;
        }
        .feature-tile:hover .tile-icon-box {
          background: var(--tile-color);
          color: white;
        }
        .feature-tile h3 {
          font-size: 1.15rem;
          font-weight: 800;
          margin-bottom: 1rem;
        }
        .feature-tile p {
          font-size: 0.9rem;
          color: var(--text-secondary);
          line-height: 1.6;
          margin-bottom: 2rem;
          flex: 1;
        }
        .tile-footer {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.85rem;
          font-weight: 800;
          color: var(--tile-color);
          opacity: 0;
          transform: translateX(-10px);
          transition: all 0.3s;
        }
        .feature-tile:hover .tile-footer {
          opacity: 1;
          transform: translateX(0);
        }

        @media (max-width: 768px) {
          .doc-home-hero h1 { font-size: 2.25rem; }
          .doc-home-hero p { font-size: 1rem; margin-bottom: 2rem; }
          .doc-home-hero { margin-bottom: 3rem; }
          .quick-actions { flex-direction: column; }
          .feature-tiles-grid { grid-template-columns: 1fr; }
        }
      `}),e.jsx("div",{style:{display:"none"},children:"Privacy Policy Terms of Service Disclaimer © 2026"})]})},h=({size:r})=>e.jsx("svg",{width:r,height:r,viewBox:"0 0 24 24",fill:"none",stroke:"currentColor",strokeWidth:"3",strokeLinecap:"round",strokeLinejoin:"round",children:e.jsx("path",{d:"m9 18 6-6-6-6"})});export{v as DocHome};
