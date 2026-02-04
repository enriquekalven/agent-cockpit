import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { useParams } from 'react-router-dom';

const DOC_FILES: Record<string, string> = {
  readme: '/README.md',
  'getting-started': '/GETTING_STARTED.md',
  deployment: '/DEPLOYMENT.md',
  story: '/AGENT_OPS_STORY.md',
  'production-checklist': '/PRODUCTION_CHECKLIST.md',
  'cockpit-guide': '/COCKPIT_GUIDE.md',
  'arch-review': '/TECHNICAL_ARCH_REVIEW.md',
  'quality-guide': '/TECHNICAL_QUALITY_GUIDE.md',
  'redteam-guide': '/TECHNICAL_REDTEAM_GUIDE.md',
  'finops-guide': '/TECHNICAL_FINOPS_GUIDE.md',
  'ux-guide': '/TECHNICAL_UX_GUIDE.md',
  'infra-guide': '/TECHNICAL_INFRA_GUIDE.md',
  'a2a-guide': '/TECHNICAL_A2A_GUIDE.md',
  'audit-guide': '/TECHNICAL_AUDIT_GUIDE.md',
  'commands-master': '/TECHNICAL_COMMANDS_MASTER.md',
  'uvx-master': '/TECHNICAL_UVX_MASTER.md',
  'roadmap': '/ROADMAP_V13.md',
  'google-architecture': '/GOOGLE_ARCHITECTURE.md',
  'audit-scenarios': '/AUDIT_SCENARIOS.md',
  'prd': '/PRD.md',
  'gemini': '/GEMINI.md',
};

export const DocPage: React.FC = () => {
  const { docId } = useParams<{ docId: string }>();
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDoc = async () => {
      setLoading(true);
      try {
        const file = DOC_FILES[docId || 'getting-started'] || DOC_FILES['getting-started'];
        const response = await fetch(file);
        if (!response.ok) throw new Error('File not found');
        const text = await response.text();
        setContent(text);
      } catch (err) {
        setContent('# Error\nDocument not found. Please check the documentation path.');
      } finally {
        // Add a slight delay for better transition feel
        setTimeout(() => setLoading(false), 300);
      }
    };

    fetchDoc();
  }, [docId]);

  if (loading) {
    return (
      <div className="doc-loading-container">
        <div className="skeleton-title" />
        <div className="skeleton-line" style={{ width: '100%' }} />
        <div className="skeleton-line" style={{ width: '90%' }} />
        <div className="skeleton-line" style={{ width: '95%' }} />
        <div className="skeleton-line" style={{ width: '85%' }} />
        <div className="skeleton-line" style={{ width: '40%', marginTop: '2rem' }} />
      </div>
    );
  }

  return (
    <article className="markdown-body">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {content}
      </ReactMarkdown>
    </article>
  );
};
