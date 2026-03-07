import { useState } from "react";
import { analyzeStory, validateStory } from "../services/api";

/**
 * Custom hook for story analysis
 */
export const useStory = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [validation, setValidation] = useState(null);

  /**
   * Analyze a story
   */
  const analyze = async (story, title, episodes = 5) => {
    setLoading(true);
    setError(null);

    try {
      const data = await analyzeStory(story, title, episodes);
      if (data.success) {
        setResult(data.data);
        return data.data;
      } else {
        setError(data.error);
        return null;
      }
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Quick validate a story
   */
  const validate = async (story) => {
    setLoading(true);
    setError(null);

    try {
      const data = await validateStory(story);
      setValidation(data);
      return data;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Reset state
   */
  const reset = () => {
    setResult(null);
    setValidation(null);
    setError(null);
  };

  return {
    loading,
    error,
    result,
    validation,
    analyze,
    validate,
    reset,
  };
};

export default useStory;
