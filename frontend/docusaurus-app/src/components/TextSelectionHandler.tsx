import React, { useState, useEffect, useRef } from 'react';

const TextSelectionHandler: React.FC = () => {
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const [buttonPosition, setButtonPosition] = useState<{ x: number; y: number } | null>(null);
  const [explanation, setExplanation] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const buttonRef = useRef<HTMLButtonElement>(null);

  const handleMouseUp = () => {
    const selection = window.getSelection();
    if (selection && selection.toString().length > 0) {
      const text = selection.toString().trim(); // Trim to avoid empty selections with whitespace
      if (text.length > 0) {
        setSelectedText(text);

        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        // Position the button slightly above and centered on the selected text
        setButtonPosition({
          x: rect.left + window.scrollX + rect.width / 2,
          y: rect.top + window.scrollY - 40, // 40px above selection
        });
      } else {
        setSelectedText(null);
        setButtonPosition(null);
      }
    } else {
      setSelectedText(null);
      setButtonPosition(null);
    }
  };

  const handleAskAIClick = async () => {
    if (selectedText) {
      setIsLoading(true);
      setExplanation(null); // Clear previous explanation

      try {
        const response = await fetch('http://localhost:8000/explain_text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text_selection: selectedText }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.explanation) {
          setExplanation(data.explanation);
        } else if (data.error) {
          setExplanation(`Error: ${data.error}`);
        } else {
          setExplanation('No explanation received.');
        }
      } catch (error) {
        console.error('Error fetching explanation:', error);
        setExplanation('Failed to fetch explanation. Please ensure the API is running and try again.');
      } finally {
        setIsLoading(false);
        // Clear selection but keep button position for now to allow closing the popup
        // window.getSelection()?.removeAllRanges(); // Don't remove range yet, as user might still want to interact with selection
      }
    }
  };

  const closeExplanationPopup = () => {
    setExplanation(null);
    setSelectedText(null);
    setButtonPosition(null);
    window.getSelection()?.removeAllRanges(); // Clear selection when popup is closed
  };

  useEffect(() => {
    document.addEventListener('mouseup', handleMouseUp);
    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, []);

  return (
    <>
      {selectedText && buttonPosition && (
        <button
          ref={buttonRef}
          className="ask-ai-button"
          style={{
            position: 'absolute',
            left: buttonPosition.x,
            top: buttonPosition.y,
            transform: 'translateX(-50%)', // Center the button horizontally
            zIndex: 1000, // Ensure it's above other content
          }}
          onClick={handleAskAIClick}
          disabled={isLoading}>
          {isLoading ? 'Asking AI...' : 'Ask AI'}
        </button>
      )}

      {explanation && (
        <div className="explanation-popup-overlay">
          <div className="explanation-popup-content">
            <button className="close-button" onClick={closeExplanationPopup}>
              &times;
            </button>
            <h3>Simplified Explanation</h3>
            {isLoading ? (
              <p>Loading explanation...</p>
            ) : (
              <p>{explanation}</p>
            )}
            <p><strong>Original Text:</strong> {selectedText}</p>
          </div>
        </div>
      )}
    </>
  );
};

export default TextSelectionHandler;
