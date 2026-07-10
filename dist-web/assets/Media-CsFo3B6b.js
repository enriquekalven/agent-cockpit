import{c as r,d as o,j as e}from"./index-CIXdYeLf.js";import{C as n}from"./chevron-left-BXuc3H9K.js";import{E as s}from"./external-link-ZXYTl_Pi.js";/**
 * @license lucide-react v0.562.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const d=[["path",{d:"M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z",key:"10ikf1"}]],l=r("play",d),p=()=>{const t=o(),a=[{title:"AgentOps Cockpit Getting Started",url:"https://youtu.be/-H-7iJMi-A0",id:"-H-7iJMi-A0",desc:"Learn the basics of AgentOps Cockpit and how to get started."},{title:"Ladder of Autonomy",url:"https://youtu.be/_qithDKlZSA",id:"_qithDKlZSA",desc:"Understand the levels of autonomy in AI agents."},{title:"Why you need Evolve",url:"https://youtu.be/oJtb-0idIDI",id:"oJtb-0idIDI",desc:"Discover why the Evolve module is critical for agent evolution."},{title:"Why you need Certify",url:"https://youtu.be/bTrmyXqkprg",id:"bTrmyXqkprg",desc:"Learn about the certification process for production readiness."},{title:"Why you need Upgrade",url:"https://youtu.be/b6Xk3tnvsmI",id:"b6Xk3tnvsmI",desc:"Understand how to upgrade your agents safely."},{title:"Evolve Deep Dive",url:"https://youtu.be/0fMEQZTrwHI",id:"0fMEQZTrwHI",desc:"A deep dive into the Evolve capabilities."}];return e.jsxs("div",{className:"media-view",children:[e.jsx("div",{className:"media-glow"}),e.jsxs("header",{className:"media-header",children:[e.jsxs("button",{className:"back-btn",onClick:()=>t("/"),children:[e.jsx(n,{size:18}),"Back to Home"]}),e.jsxs("div",{className:"media-title-group",children:[e.jsxs("h1",{children:["AgentOps ",e.jsx("span",{className:"gradient-text",children:"Media Hub"})]}),e.jsx("p",{children:"Watch tutorials and deep dives on autonomous governance."})]})]}),e.jsx("main",{className:"media-container",children:e.jsx("div",{className:"video-grid",children:a.map(i=>e.jsxs("div",{className:"video-card",children:[e.jsxs("div",{className:"video-thumbnail-container",children:[e.jsx("img",{src:`https://img.youtube.com/vi/${i.id}/maxresdefault.jpg`,alt:i.title,className:"video-thumbnail"}),e.jsx("div",{className:"play-overlay",children:e.jsx("div",{className:"play-button",children:e.jsx(l,{size:24,fill:"currentColor"})})})]}),e.jsxs("div",{className:"video-info",children:[e.jsx("h3",{children:i.title}),e.jsx("p",{children:i.desc}),e.jsxs("a",{href:i.url,target:"_blank",rel:"noopener noreferrer",className:"watch-link",children:["Watch on YouTube ",e.jsx(s,{size:14})]})]})]},i.id))})}),e.jsx("style",{children:`
        .media-view {
          min-height: 100vh;
          background: #0f172a;
          color: white;
          padding: 2rem;
          position: relative;
          overflow-x: hidden;
        }

        .media-glow {
          position: absolute;
          top: 0;
          right: 0;
          width: 50vw;
          height: 50vh;
          background: radial-gradient(circle, rgba(59, 130, 246, 0.1), transparent 70%);
          pointer-events: none;
        }

        .media-header {
          max-width: 1200px;
          margin: 0 auto 3rem;
        }

        .back-btn {
          background: transparent;
          border: 1px solid rgba(255,255,255,0.1);
          color: rgba(255,255,255,0.7);
          padding: 0.5rem 1rem;
          border-radius: 8px;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.85rem;
          cursor: pointer;
          margin-bottom: 2rem;
          transition: all 0.2s;
        }
        .back-btn:hover {
          background: rgba(255,255,255,0.05);
          color: white;
        }

        .media-title-group h1 {
          font-size: 2.5rem;
          font-weight: 800;
          margin-bottom: 0.5rem;
          letter-spacing: -0.02em;
        }

        .media-title-group p {
          color: #94a3b8;
          font-size: 1.1rem;
        }

        .media-container {
          max-width: 1200px;
          margin: 0 auto;
        }

        .video-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 2rem;
        }

        .video-card {
          background: #1e293b;
          border-radius: 16px;
          border: 1px solid rgba(255,255,255,0.05);
          overflow: hidden;
          transition: all 0.3s ease;
          display: flex;
          flex-direction: column;
        }

        .video-card:hover {
          transform: translateY(-5px);
          border-color: rgba(59, 130, 246, 0.3);
          box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }

        .video-thumbnail-container {
          position: relative;
          aspect-ratio: 16/9;
          overflow: hidden;
        }

        .video-thumbnail {
          width: 100%;
          height: 100%;
          object-fit: cover;
          transition: transform 0.3s ease;
        }

        .video-card:hover .video-thumbnail {
          transform: scale(1.05);
        }

        .play-overlay {
          position: absolute;
          inset: 0;
          background: rgba(0,0,0,0.4);
          display: flex;
          align-items: center;
          justify-content: center;
          opacity: 0.8;
          transition: opacity 0.3s ease;
        }

        .video-card:hover .play-overlay {
          opacity: 1;
          background: rgba(0,0,0,0.2);
        }

        .play-button {
          width: 48px;
          height: 48px;
          border-radius: 50%;
          background: rgba(59, 130, 246, 0.8);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          transition: transform 0.2s ease;
        }

        .video-card:hover .play-button {
          transform: scale(1.1);
          background: #3b82f6;
        }

        .video-info {
          padding: 1.5rem;
          flex: 1;
          display: flex;
          flex-direction: column;
        }

        .video-info h3 {
          font-size: 1.1rem;
          font-weight: 700;
          margin-bottom: 0.5rem;
          color: white;
        }

        .video-info p {
          font-size: 0.85rem;
          color: #94a3b8;
          line-height: 1.5;
          margin-bottom: 1.5rem;
          flex: 1;
        }

        .watch-link {
          color: #3b82f6;
          text-decoration: none;
          font-size: 0.85rem;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          transition: color 0.2s;
          margin-top: auto;
        }

        .watch-link:hover {
          color: #60a5fa;
        }

        @media (max-width: 768px) {
          .media-view { padding: 1rem; }
          .media-title-group h1 { font-size: 2rem; }
          .video-grid { grid-template-columns: 1fr; }
        }
      `})]})};export{p as Media};
