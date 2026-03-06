/**
 * API Service for connecting to backend
 * Base URL: http://localhost:5000/api
 */

// For development with backend on port 5000
const API_BASE_URL = "http://localhost:5000/api";

/**
 * Analyze a story
 * @param {string} story - The story text
 * @param {string} title - Story title
 * @param {number} episodes - Number of episodes
 * @returns {Promise} - API response
 */
export const analyzeStory = async (story, title, episodes = 5) => {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ story, title, episodes }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

/**
 * Validate a story (quick check)
 * @param {string} story - The story text
 * @returns {Promise} - API response
 */
export const validateStory = async (story) => {
  try {
    const response = await fetch(`${API_BASE_URL}/validate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ story }),
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

/**
 * Check API health
 * @returns {Promise} - API response
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

export default {
  analyzeStory,
  validateStory,
  checkHealth,
};
