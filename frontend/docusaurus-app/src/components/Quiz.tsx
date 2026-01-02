import React, { useState } from 'react';
import clsx from 'clsx';
import styles from './Quiz.module.css';

interface QuizQuestion {
  question: string;
  options: string[];
  correctAnswer: string;
}

interface QuizProps {
  data: QuizQuestion[];
}

const Quiz: React.FC<QuizProps> = ({ data }) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  const currentQuestion = data[currentQuestionIndex];

  const handleOptionClick = (option: string) => {
    if (!isSubmitted) {
      setSelectedAnswer(option);
    }
  };

  const handleSubmit = () => {
    if (selectedAnswer) {
      setIsSubmitted(true);
      if (selectedAnswer === currentQuestion.correctAnswer) {
        setScore(score + 1);
      }
    }
  };

  const handleNext = () => {
    setSelectedAnswer(null);
    setIsSubmitted(false);
    if (currentQuestionIndex < data.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      // End of quiz, could show final score or reset
      alert(`Quiz Finished! Your score: ${score}/${data.length}`);
      setCurrentQuestionIndex(0); // Reset for replay
      setScore(0);
    }
  };

  const getOptionClassName = (option: string) => {
    if (!isSubmitted) {
      return clsx(styles.option, {
        [styles.selected]: selectedAnswer === option,
      });
    }

    // After submission
    if (option === currentQuestion.correctAnswer) {
      return clsx(styles.option, styles.correct);
    }
    if (option === selectedAnswer && option !== currentQuestion.correctAnswer) {
      return clsx(styles.option, styles.incorrect);
    }
    return styles.option;
  };

  if (!currentQuestion) {
    return <div className={styles.quizContainer}>No quiz data available.</div>;
  }

  return (
    <div className={styles.quizContainer}>
      <h2>Quiz Time!</h2>
      <p className={styles.questionNumber}>Question {currentQuestionIndex + 1} of {data.length}</p>
      <p className={styles.questionText}>{currentQuestion.question}</p>
      <div className={styles.optionsContainer}>
        {currentQuestion.options.map((option, index) => (
          <button
            key={index}
            className={getOptionClassName(option)}
            onClick={() => handleOptionClick(option)}
            disabled={isSubmitted}
          >
            {option}
          </button>
        ))}
      </div>
      <div className={styles.actions}>
        {!isSubmitted && (
          <button
            className={styles.submitButton}
            onClick={handleSubmit}
            disabled={!selectedAnswer}
          >
            Submit Answer
          </button>
        )}
        {isSubmitted && (
          <button
            className={styles.nextButton}
            onClick={handleNext}
          >
            {currentQuestionIndex < data.length - 1 ? 'Next Question' : 'Restart Quiz'}
          </button>
        )}
      </div>
      {isSubmitted && (
        <div className={styles.feedback}>
          {selectedAnswer === currentQuestion.correctAnswer ? (
            <p className={styles.correctFeedback}>Correct!</p>
          ) : (
            <p className={styles.incorrectFeedback}>Incorrect. The correct answer was: {currentQuestion.correctAnswer}</p>
          )}
        </div>
      )}
    </div>
  );
};

export default Quiz;
