import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { useParams } from 'react-router-dom';

const DOC_FILES: Record<string, string> = {
  readme: '/README.md',
  'getting-started': '/GETTING_STARTED.md',
  development: '/DEVELOPMENT.md',
  deployment: '/DEPLOYMENT.md',
  'cli-commands': '/CLI_COMMANDS.md',
  a2a: '/A2A_GUIDE.md',
  'be-integration': '/BE_INTEGRATION_GUIDE.md',
  story: '/AGENT_OPS_STORY.md',
};

export const DocPage: React.FC = () => {
  const { docId } = useParams<{ docId: string }>();
  const [content, setContent] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDoc = async () => {
      setLoading(true);
      try {
        const file = DOC_FILES[docId || 'readme'] || DOC_FILES.readme;
        const response = await fetch(file);
        if (!response.ok) throw new Error('File not found');
        const text = await response.text();
        setContent(text);
      } catch (err) {
        setContent('# Error\nDocument not found.');
      } finally {
        setLoading(false);
      }
    };

    fetchDoc();
  }, [docId]);

  if (loading) {
    return <div className="doc-loading">Loading documentation...</div>;
  }

  return (
    <article className="markdown-body">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {content}
      </ReactMarkdown>
    </article>
  );
};
