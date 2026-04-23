import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Play, ExternalLink } from 'lucide-react';

export const Media: React.FC = () => {
  const navigate = useNavigate();

  const videos = [
    {
      title: 'AgentOps Cockpit Getting Started',
      url: 'https://youtu.be/-H-7iJMi-A0',
      id: '-H-7iJMi-A0',
      desc: 'Learn the basics of AgentOps Cockpit and how to get started.'
    },
    {
      title: 'Ladder of Autonomy',
      url: 'https://youtu.be/_qithDKlZSA',
      id: '_qithDKlZSA',
      desc: 'Understand the levels of autonomy in AI agents.'
    },
    {
      title: 'Why you need Evolve',
      url: 'https://youtu.be/oJtb-0idIDI',
      id: 'oJtb-0idIDI',
      desc: 'Discover why the Evolve module is critical for agent evolution.'
    },
    {
      title: 'Why you need Certify',
      url: 'https://youtu.be/bTrmyXqkprg',
      id: 'bTrmyXqkprg',
      desc: 'Learn about the certification process for production readiness.'
    },
    {
      title: 'Why you need Upgrade',
      url: 'https://youtu.be/b6Xk3tnvsmI',
      id: 'b6Xk3tnvsmI',
      desc: 'Understand how to upgrade your agents safely.'
    },
    {
      title: 'Evolve Deep Dive',
      url: 'https://youtu.be/0fMEQZTrwHI',
      id: '0fMEQZTrwHI',
      desc: 'A deep dive into the Evolve capabilities.'
    }
  ];

  return (
    <div className="media-view">
      <div className="media-glow"></div>
      
      <header className="media-header">
        <button className="back-btn" onClick={() => navigate('/')}>
          <ChevronLeft size={18} />
          Back to Home
        </button>
        <div className="media-title-group">
          <h1>AgentOps <span className="gradient-text">Media Hub</span></h1>
          <p>Watch tutorials and deep dives on autonomous governance.</p>
        </div>
      </header>

      <main className="media-container">
        <div className="video-grid">
          {videos.map((video) => (
            <div key={video.id} className="video-card">
              <div className="video-thumbnail-container">
                <img 
                  src={`https://img.youtube.com/vi/${video.id}/maxresdefault.jpg`} 
                  alt={video.title}
                  className="video-thumbnail"
                />
                <div className="play-overlay">
                  <div className="play-button">
                    <Play size={24} fill="currentColor" />
                  </div>
                </div>
              </div>
              <div className="video-info">
                <h3>{video.title}</h3>
                <p>{video.desc}</p>
                <a 
                  href={video.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="watch-link"
                >
                  Watch on YouTube <ExternalLink size={14} />
                </a>
              </div>
            </div>
          ))}
        </div>
      </main>

      <style>{`
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
      `}</style>
    </div>
  );
};
