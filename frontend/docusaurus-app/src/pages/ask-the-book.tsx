import React, { useState } from 'react';
import Layout from '@theme/Layout';

function AskTheBook(): JSX.Element {
  const [question, setQuestion] = useState('');

  const handleAsk = () => {
    // In a real application, this would trigger the RAG system
    console.log('Asked question:', question);
    alert(`You asked: ${question}`);
  };

  return (
    <Layout
      title="Ask the Book"
      description="Ask questions about the textbook using an interactive RAG system"
    >
      <main className="container margin-vert--lg">
        <h1 className="hero__title text--center">Ask the Book</h1>
        <p className="text--center">This is an interactive RAG system. Ask a question about the textbook.</p>
        <div style={{ maxWidth: '600px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '10px', alignItems: 'center' }}>
          <p className="hero__subtitle text--center">e.g., What is Physical AI?</p>
          <input
            type="text"
            placeholder="Type your question here..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            style={{ width: '100%', padding: '10px', fontSize: '1rem', borderRadius: '5px', border: '1px solid #ccc' }}
          />
          <button
            onClick={handleAsk}
            style={{ padding: '10px 20px', fontSize: '1rem', borderRadius: '5px', border: 'none', backgroundColor: '#007bff', color: 'white', cursor: 'pointer' }}
          >
            Ask
          </button>
        </div>
      </main>
    </Layout>
  );
}

export default AskTheBook;

