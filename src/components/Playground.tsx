import React, { useState, useRef, useEffect } from 'react';
import { Send, ArrowLeft, Bot, User, Sparkles, Shield, Zap } from 'lucide-react';
import { Link } from 'react-router-dom';
import { A2UISurfaceRenderer } from '../a2ui/A2UIRenderer';

interface Message {
  role: 'user' | 'assistant';
  content: string | any;
}

export const Playground: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Hello! I am your Optimized Agent. How can I assist you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      // Calling the local FastAPI Agent Engine
      const response = await fetch(`http://localhost:8000/agent/query?q=${encodeURIComponent(userMessage)}`);
      const data = await response.json();
      
      setMessages(prev => [...prev, { role: 'assistant', content: data }]);
    } catch (err) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: {
          surfaceId: 'error',
          content: [{
            type: 'Text',
            props: { text: 'Engine Offline. Please ensure the backend is running with "make dev".', variant: 'body' }
          }]
        } 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="playground-container">
      <header className="playground-header">
        <Link to="/" className="back-link">
          <ArrowLeft size={20} />
          <span>Exit Playground</span>
        </Link>
        <div className="flex items-center gap-3">
          <Sparkles className="text-secondary-color" size={24} />
          <h1 className="text-xl font-bold">Agent Engine Preview</h1>
        </div>
        <div className="engine-status">
          <span className="dot"></span>
          Agent Stack v2.1
        </div>
      </header>

      <div className="chat-viewport">
        <div className="messages-list">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message-wrapper ${msg.role}`}>
              <div className="avatar">
                {msg.role === 'assistant' ? <Bot size={20} /> : <User size={20} />}
              </div>
              <div className="message-content">
                {typeof msg.content === 'string' ? (
                  <p>{msg.content}</p>
                ) : (
                  <A2UISurfaceRenderer surface={msg.content} />
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message-wrapper assistant">
              <div className="avatar pulsing">
                <Bot size={20} />
              </div>
              <div className="loading-indicator">
                <span></span><span></span><span></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="input-area">
        <div className="input-container glass-panel">
          <input 
            type="text" 
            placeholder="Type a query (e.g., 'Search for cloud policies')..." 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button className="send-btn" onClick={handleSend} disabled={isLoading}>
            <Send size={20} />
          </button>
        </div>
        <p className="input-hint text-xs opacity-50 text-center mt-3">
          <Shield size={12} className="inline mr-1" /> All queries are audited for PII and cost-optimized by the Cockpit.
        </p>
      </div>

      <style>{`
        .playground-container {
          height: 100vh;
          display: flex;
          flex-direction: column;
          background: var(--bg-color);
          color: var(--text-color);
        }
        .playground-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 1rem 2rem;
          border-bottom: 1px solid var(--border-color);
          background: rgba(var(--bg-color-rgb), 0.8);
          backdrop-filter: blur(10px);
          z-index: 10;
        }
        .engine-status {
          font-size: 0.75rem;
          font-weight: 800;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          background: rgba(var(--secondary-color-rgb), 0.1);
          color: var(--secondary-color);
          padding: 0.4rem 0.8rem;
          border-radius: 2rem;
        }
        .dot {
          width: 6px;
          height: 6px;
          background: var(--secondary-color);
          border-radius: 50%;
        }
        .chat-viewport {
          flex: 1;
          overflow-y: auto;
          padding: 2rem;
        }
        .messages-list {
          max-width: 900px;
          margin: 0 auto;
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }
        .message-wrapper {
          display: flex;
          gap: 1.5rem;
          max-width: 80%;
        }
        .message-wrapper.user {
          flex-direction: row-reverse;
          align-self: flex-end;
        }
        .avatar {
          width: 40px;
          height: 40px;
          border-radius: 12px;
          background: var(--surface-color);
          border: 1px solid var(--border-color);
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
          color: var(--primary-color);
        }
        .message-wrapper.user .avatar {
          background: var(--primary-color);
          color: white;
          border: none;
        }
        .message-content {
          background: var(--surface-color);
          padding: 1.25rem;
          border-radius: 20px;
          border: 1px solid var(--border-color);
          font-size: 0.95rem;
          line-height: 1.6;
        }
        .message-wrapper.user .message-content {
          background: var(--primary-color);
          color: white;
          border: none;
        }
        .input-area {
          padding: 2rem;
          background: linear-gradient(to top, var(--bg-color), transparent);
        }
        .input-container {
          max-width: 900px;
          margin: 0 auto;
          display: flex;
          gap: 1rem;
          padding: 0.75rem 1.5rem;
          background: rgba(255, 255, 255, 0.03);
          border-radius: 100px;
          border: 1px solid var(--border-color);
        }
        .input-container input {
          flex: 1;
          background: transparent;
          border: none;
          color: white;
          font-size: 1rem;
          outline: none;
        }
        .send-btn {
          background: var(--primary-color);
          color: white;
          border: none;
          width: 40px;
          height: 40px;
          border-radius: 50%;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: transform 0.2s;
        }
        .send-btn:hover {
          transform: scale(1.1);
        }
        .loading-indicator {
          display: flex;
          gap: 4px;
          padding: 10px;
        }
        .loading-indicator span {
          width: 6px;
          height: 6px;
          background: var(--text-color);
          border-radius: 50%;
          opacity: 0.3;
          animation: dot-loading 1.4s infinite;
        }
        .loading-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .loading-indicator span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes dot-loading {
          0%, 100% { transform: translateY(0); opacity: 0.3; }
          50% { transform: translateY(-4px); opacity: 1; }
        }
      `}</style>
    </div>
  );
};
