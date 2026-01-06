import React, { useState } from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './RagChatbot.module.css';

interface Message {
  text: string;
  isUser: boolean;
}

interface ChatRequest {
  messages: { role: string; content: string }[];
}

interface ChatResponse {
  answer: string;
}

const RagChatbot = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const { siteConfig } = useDocusaurusContext();
  const backendUrl = siteConfig.customFields.backendUrl as string;

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { text: input, isUser: true };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      // Prepare the messages for the API request
      const apiMessages = messages.map(msg => ({
        role: msg.isUser ? 'user' : 'assistant',
        content: msg.text
      }));

      // Add the current user input
      apiMessages.push({
        role: 'user',
        content: input
      });

      const requestBody: ChatRequest = {
        messages: apiMessages
      };

      const response = await fetch(`${backendUrl}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || `HTTP error! Status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();

      const botMessage: Message = {
        text: data.answer,
        isUser: false,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err: any) {
      console.error('Error sending message:', err);
      setError(err.message || 'Failed to send message. Please ensure the API is running and try again.');

      // Add error message to chat as well
      const errorMessage: Message = {
        text: `Error: ${err.message || 'Failed to get response from the AI. Please try again.'}`,
        isUser: false,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout title="RAG Chatbot" description="Chat with the AI Textbook">
      <div className={styles.chatContainer}>
        <div className={styles.messageList}>
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`${styles.message} ${
                msg.isUser ? styles.userMessage : styles.botMessage
              }`}
            >
              {msg.text}
            </div>
          ))}
          {isLoading && (
            <div className={`${styles.message} ${styles.botMessage}`}>
              <span className={styles.loadingDots}></span>
            </div>
          )}
          {error && <div className={styles.errorMessage}>{error}</div>}
        </div>
        <div className={styles.inputArea}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask a question about the AI textbook..."
            className={styles.inputBox}
            disabled={isLoading}
          />
          <button onClick={handleSend} className={styles.sendButton} disabled={isLoading}>
            Send
          </button>
        </div>
      </div>
    </Layout>
  );
};

export default RagChatbot;
