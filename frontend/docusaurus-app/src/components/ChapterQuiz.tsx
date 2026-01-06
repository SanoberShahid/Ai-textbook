import React, { useState } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Quiz from './Quiz'; // The presentational component
import styles from './ChapterQuiz.module.css';

interface QuizQuestion {
  question: string;
  options: string[];
  correctAnswer: string;
}

interface ChapterQuizProps {
  chapter: string;
}

const ChapterQuiz: React.FC<ChapterQuizProps> = ({ chapter }) => {
  const { siteConfig } = useDocusaurusContext();
  const backendUrl = siteConfig.customFields.backendUrl as string;

  const [quizData, setQuizData] = useState<QuizQuestion[] | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchQuiz = async () => {
    setIsLoading(true);
    setError(null);
    setQuizData(null);

    try {
      const response = await fetch(`${backendUrl}/generate_quiz`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ chapter_id: chapter }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || `HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      if (data.quiz && data.quiz.length > 0) {
        setQuizData(data.quiz);
      } else {
        setError('No quiz could be generated for this chapter.');
      }
    } catch (e: any) {
      console.error('Failed to fetch quiz:', e);
      setError(e.message || 'An unexpected error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.chapterQuizContainer}>
      { !quizData && (
        <div className={styles.startScreen}>
          <h3>Test Your Knowledge!</h3>
          <p>Ready to see what you've learned from {chapter}?</p>
          <button
            className={styles.startButton}
            onClick={fetchQuiz}
            disabled={isLoading}
          >
            {isLoading ? 'Generating Quiz...' : 'Start the Quiz'}
          </button>
          {error && <p className={styles.error}>{error}</p>}
        </div>
      )}

      {isLoading && !error && <div className={styles.loading}>Loading Quiz...</div>}

      {quizData && <Quiz data={quizData} />}
    </div>
  );
};

export default ChapterQuiz;
