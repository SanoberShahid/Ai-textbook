import React, { useState, useEffect, useRef, useCallback } from 'react';
import ReactDOM from 'react-dom';

interface ExplanationPopupProps {
  explanation: string;
  onClose: () => void;
}

const ExplanationPopup: React.FC<ExplanationPopupProps> = ({ explanation, onClose }) => {
  return (
    <div className="explanation-popup-overlay" onClick={onClose}>
      <div className="explanation-popup-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-button" onClick={onClose}>&times;</button>
        <h3>Simplified Explanation</h3>
        <p>{explanation}</p>
      </div>
    </div>
  );
};

const TextSelectionHighlighter: React.FC = () => {
  const [selectedText, setSelectedText] = useState<string>('');
  const [buttonPosition, setButtonPosition] = useState<{ x: number; y: number } | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [explanation, setExplanation] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const buttonRef = useRef<HTMLButtonElement>(null);

  const getSelectionDetails = useCallback(() => {
    const selection = window.getSelection();
    if (selection && selection.toString().length > 0) {
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      // Position the button above the selected text
      setButtonPosition({
        x: rect.left + window.scrollX + rect.width / 2,
        y: rect.top + window.scrollY - 40, // 40px above selection
      });
      setSelectedText(selection.toString());
    } else {
      setSelectedText('');
      setButtonPosition(null);
      setExplanation(null);
      setError(null);
    }
  }, []);

  useEffect(() => {
    document.addEventListener('mouseup', getSelectionDetails);
    document.addEventListener('selectionchange', getSelectionDetails); // For immediate feedback

    return () => {
      document.removeEventListener('mouseup', getSelectionDetails);
      document.removeEventListener('selectionchange', getSelectionDetails);
    };
  }, [getSelectionDetails]);

  const handleAskAI = async () => {
    if (!selectedText.trim()) return;

    setIsLoading(true);
    setExplanation(null);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/explain_text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text_selection: selectedText }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`HTTP error! status: ${response.status} - ${errorData.error || response.statusText}`);
      }

      const data = await response.json();
      if (data.explanation) {
        setExplanation(data.explanation);
      } else {
        setError(data.error || 'Could not get an explanation.');
      }
    } catch (e: any) {
      console.error("Error asking AI for explanation:", e);
      setError(`Failed to get explanation: ${e.message || 'Please check backend server.'}`);
    } finally {
      setIsLoading(false);
      // After showing explanation, clear selection and hide button
      window.getSelection()?.removeAllRanges();
      setSelectedText('');
      setButtonPosition(null);
    }
  };

  const closeExplanationPopup = () => {
    setExplanation(null);
    setError(null);
  };

  return (
    <>
      {buttonPosition && selectedText && (
        <button
          ref={buttonRef}
          className="ask-ai-button"
          style={{ left: buttonPosition.x, top: buttonPosition.y }}
          onClick={handleAskAI}
          disabled={isLoading}
        >
          {isLoading ? 'Asking AI...' : 'Ask AI'}
        </button>
      )}

      {explanation && ReactDOM.createPortal(
        <ExplanationPopup explanation={explanation} onClose={closeExplanationPopup} />,
        document.body
      )}

      {error && ReactDOM.createPortal(
        <ExplanationPopup explanation={error} onClose={closeExplanationPopup} />,
        document.body
      )}
    </>
  );
};

export default TextSelectionHighlighter;