import { useState, useEffect } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import ScoreMeter from "../components/analysis/ScoreMeter";
import EmotionChart from "../components/analysis/EmotionChart";
import { useStory } from "../hooks/useStory";

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { id } = useParams();
  const { result, loading, error, analyze } = useStory();
  const [analysisData, setAnalysisData] = useState(null);
  const [localLoading, setLocalLoading] = useState(false);
  const [localError, setLocalError] = useState(null);

  // Get story from location state or use ID
  const story = location.state?.story || "";
  const storyTitle = location.state?.storyTitle || "Your Story";
  const passedAnalysisData = location.state?.analysisData || null;

  // Check if we have data, if not redirect
  useEffect(() => {
    console.log("Results page loaded with state:", location.state);

    if (!passedAnalysisData && !story && !id) {
      console.log("No data found, redirecting to home");
      navigate("/");
    }

    if (passedAnalysisData) {
      console.log("Using passed analysis data:", passedAnalysisData);
      setAnalysisData(passedAnalysisData);
    }
  }, [location, navigate, passedAnalysisData, story, id]);

  // Load analysis results if we have story but no data
  useEffect(() => {
    const loadAnalysis = async () => {
      if (story && !analysisData && !passedAnalysisData) {
        setLocalLoading(true);
        setLocalError(null);
        try {
          await analyze(story, storyTitle, 5);
        } catch (err) {
          setLocalError(err.message);
        } finally {
          setLocalLoading(false);
        }
      }
    };

    loadAnalysis();
  }, [story, storyTitle, analyze, analysisData, passedAnalysisData]);

  // Update analysisData when result changes
  useEffect(() => {
    if (result && !analysisData) {
      setAnalysisData(result);
    }
  }, [result, analysisData]);

  // Prepare emotion chart data - aggregates across ALL episodes
  const prepareEmotionData = () => {
    if (
      !analysisData ||
      !analysisData.episodes ||
      analysisData.episodes.length === 0
    ) {
      console.log("No episode data available");
      return null;
    }

    const emotions = {
      joy: [],
      sadness: [],
      anger: [],
      fear: [],
      surprise: [],
    };

    try {
      // Iterate through ALL episodes to build a cross-episode emotion journey
      for (const episode of analysisData.episodes) {
        const arc = episode.emotional_arc;
        if (!arc) continue;

        if (Array.isArray(arc) && arc.length > 0) {
          // Backend returns array of {time, emotion, intensity, all_emotions}
          // Average the emotion scores across all segments of this episode
          const epEmotions = { joy: 0, sadness: 0, anger: 0, fear: 0, surprise: 0 };
          let count = 0;

          for (const point of arc) {
            if (point && point.all_emotions) {
              epEmotions.joy += (point.all_emotions.joy || 0);
              epEmotions.sadness += (point.all_emotions.sadness || 0);
              epEmotions.anger += (point.all_emotions.anger || 0);
              epEmotions.fear += (point.all_emotions.fear || 0);
              epEmotions.surprise += (point.all_emotions.surprise || 0);
              count++;
            } else if (point && point.emotion && point.intensity) {
              // Fallback: distribute intensity to the dominant emotion
              const intensity = point.intensity;
              const emotionKey = point.emotion;
              if (epEmotions.hasOwnProperty(emotionKey)) {
                epEmotions[emotionKey] += intensity;
              }
              // Give small values to others
              const others = Object.keys(epEmotions).filter(e => e !== emotionKey);
              const share = (1 - intensity) / others.length;
              others.forEach(e => { epEmotions[e] += share; });
              count++;
            }
          }

          if (count > 0) {
            emotions.joy.push(Math.round((epEmotions.joy / count) * 100));
            emotions.sadness.push(Math.round((epEmotions.sadness / count) * 100));
            emotions.anger.push(Math.round((epEmotions.anger / count) * 100));
            emotions.fear.push(Math.round((epEmotions.fear / count) * 100));
            emotions.surprise.push(Math.round((epEmotions.surprise / count) * 100));
          }
        } else if (typeof arc === "object" && !Array.isArray(arc)) {
          // Plain object with emotion scores
          emotions.joy.push(Math.round((arc.joy || 0) * 100));
          emotions.sadness.push(Math.round((arc.sadness || 0) * 100));
          emotions.anger.push(Math.round((arc.anger || 0) * 100));
          emotions.fear.push(Math.round((arc.fear || 0) * 100));
          emotions.surprise.push(Math.round((arc.surprise || 0) * 100));
        }
      }
    } catch (err) {
      console.error("Error processing emotion data:", err);
      return null;
    }

    // Ensure we have at least some data
    if (emotions.joy.length === 0) {
      console.log("No emotion data points found, using fallback");
      return null;
    }

    console.log("Processed emotion data across episodes:", emotions);
    return emotions;
  };

  // Get suggestions from analysis — handles {critical, improvement, tips} format
  const getSuggestions = () => {
    if (!analysisData) return [];

    const suggestions = [];

    // Handle structured suggestions from backend: {critical: [...], improvement: [...], tips: [...]}
    if (analysisData.suggestions) {
      const sug = analysisData.suggestions;

      // Extract from structured format
      if (sug.critical || sug.improvement || sug.tips) {
        // Critical suggestions first
        if (Array.isArray(sug.critical)) {
          sug.critical.forEach((s) => {
            if (s.text) suggestions.push(`🔴 ${s.text}`);
          });
        }
        // Improvement suggestions
        if (Array.isArray(sug.improvement)) {
          sug.improvement.forEach((s) => {
            if (s.text) suggestions.push(`🟡 ${s.text}`);
          });
        }
        // Tips
        if (Array.isArray(sug.tips)) {
          sug.tips.forEach((s) => {
            if (s.text) suggestions.push(`🔵 ${s.text}`);
          });
        }
      }
      // Fallback: flat array format
      else if (Array.isArray(sug)) {
        sug.forEach((s) => {
          if (s.suggestion) suggestions.push(s.suggestion);
          else if (s.text) suggestions.push(s.text);
          else if (typeof s === "string") suggestions.push(s);
        });
      }
    }

    // Add cliffhanger detail recommendations
    if (analysisData.cliffhanger_details) {
      analysisData.cliffhanger_details.forEach((detail, idx) => {
        if (detail.recommendations && detail.recommendations.length > 0) {
          suggestions.push(`Episode ${idx + 1}: ${detail.recommendations[0]}`);
        }
      });
    }

    return suggestions.length > 0
      ? suggestions
      : [
          "Add more suspense at the end to increase cliffhanger score",
          "Describe the main character's feelings more deeply",
          "Consider adding an unexpected plot twist in the middle",
          "The beginning could use more emotional impact",
        ];
  };

  const emotionData = prepareEmotionData();
  const suggestions = getSuggestions();

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      {/* Header with back button */}
      <div className="flex items-center mb-8">
        <button
          onClick={() => navigate("/")}
          className="px-6 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-lg font-semibold hover:bg-gray-300 dark:hover:bg-gray-600 transform hover:scale-105 transition-all duration-300"
        >
          ← Back
        </button>
        <h1 className="text-3xl font-bold ml-4">Analysis Results</h1>
      </div>

      {/* Loading State */}
      {(loading || localLoading) && (
        <div className="flex justify-center items-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
          <span className="ml-4 text-gray-600 dark:text-gray-400">
            Analyzing your story...
          </span>
        </div>
      )}

      {/* Error State */}
      {(error || localError) && (
        <div className="bg-red-100 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-xl p-6 mb-8">
          <h3 className="text-lg font-semibold text-red-800 dark:text-red-300 mb-2">
            Error
          </h3>
          <p className="text-red-700 dark:text-red-400">
            {error || localError}
          </p>
        </div>
      )}

      {/* Results */}
      {analysisData && !loading && !localLoading && (
        <>
          {/* Story Preview */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-8">
            <h2 className="text-xl font-semibold mb-2">Your Story</h2>
            <p className="text-gray-600 dark:text-gray-300 line-clamp-3">
              {story.substring(0, 200)}...
            </p>
            <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Language: {analysisData.language || "en"} | Episodes:{" "}
              {analysisData.total_episodes}
            </div>
          </div>

          {/* Scores Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <ScoreMeter
              label="Cliffhanger Score"
              score={Math.round(
                (analysisData.overall_scores?.cliffhanger_quality || 0.5) * 100,
              )}
              color="blue"
            />
            <ScoreMeter
              label="Retention Score"
              score={Math.round(
                (analysisData.overall_scores?.retention_prediction || 0.5) *
                  100,
              )}
              color="green"
            />
          </div>

          {/* Emotion Chart */}
          {emotionData && (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-8">
              <h2 className="text-xl font-semibold mb-4">Emotion Journey</h2>
              <EmotionChart data={emotionData} />
            </div>
          )}

          {/* Retention Curve */}
          {analysisData.retention_curve && (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-8">
              <h2 className="text-xl font-semibold mb-4">
                📈 Retention Forecast
              </h2>
              <div className="flex items-end h-40 gap-2">
                {analysisData.retention_curve.map((value, idx) => {
                  const pct = Math.round(value * 100);
                  return (
                    <div key={idx} className="flex-1 flex flex-col items-center">
                      <div
                        className="w-full bg-gradient-to-t from-green-500 to-green-400 rounded-t-lg transition-all duration-500"
                        style={{ height: `${pct}%`, minHeight: "4px" }}
                      ></div>
                      <span className="text-xs mt-2 text-gray-600 dark:text-gray-400">
                        Ep {idx + 1}
                      </span>
                      <span className="text-xs font-semibold">
                        {pct}%
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Twists Section */}
          {analysisData.twists && analysisData.twists.length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-8">
              <h2 className="text-xl font-semibold mb-4">🎭 Plot Twists</h2>
              <div className="space-y-4">
                {analysisData.twists.map((episode, idx) => (
                  <div key={idx} className="border-l-4 border-purple-500 pl-4">
                    <h3 className="font-medium text-purple-600 dark:text-purple-400">
                      Episode {episode.episode}: {episode.genre || "General"}
                    </h3>
                    <div className="mt-2 space-y-2">
                      {episode.twists &&
                        episode.twists.map((twist, tidx) => (
                          <div key={tidx} className="flex items-start gap-2">
                            <span className="text-purple-500 mt-1">✨</span>
                            <span className="text-gray-700 dark:text-gray-300">
                              {twist.text || twist}
                            </span>
                          </div>
                        ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Suggestions */}
          {suggestions.length > 0 && (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-8">
              <h2 className="text-xl font-semibold mb-4">
                💡 Suggestions to Improve
              </h2>
              <ul className="space-y-3">
                {suggestions.slice(0, 5).map((suggestion, index) => (
                  <li key={index} className="flex items-start gap-2">
                    <span className="text-blue-600 mt-1">•</span>
                    <span className="text-gray-700 dark:text-gray-300">
                      {suggestion}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Generate Story Arc Button */}
          <div className="flex justify-center mt-8">
            <button
              onClick={() => {
                navigate("/episodes", {
                  state: {
                    story,
                    storyTitle,
                    storyId: analysisData.story_id,
                    analysisData,
                  },
                });
              }}
              className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold text-lg hover:from-purple-700 hover:to-pink-700 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl flex items-center gap-2"
            >
              <span>📺</span>
              View Episodes
              <span>✨</span>
            </button>
          </div>
        </>
      )}

      {/* No Data State */}
      {!analysisData && !loading && !localLoading && !error && !localError && (
        <div className="text-center py-20">
          <p className="text-gray-500 dark:text-gray-400">
            No analysis data available.
          </p>
          <button
            onClick={() => navigate("/")}
            className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Go Home
          </button>
        </div>
      )}
    </div>
  );
};

export default Results;
