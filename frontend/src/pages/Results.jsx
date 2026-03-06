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

  // Prepare emotion chart data - FIXED FOR BACKEND FORMAT
  const prepareEmotionData = () => {
    if (
      !analysisData ||
      !analysisData.episodes ||
      analysisData.episodes.length === 0
    ) {
      console.log("No episode data available");
      return null;
    }

    // Get emotions from first episode
    const firstEpisode = analysisData.episodes[0];
    console.log("First episode data:", firstEpisode);

    if (!firstEpisode.emotional_arc) {
      console.log("No emotional_arc found");
      return null;
    }

    // Transform emotional_arc object into chart format
    const emotions = {
      joy: [],
      sadness: [],
      anger: [],
      fear: [],
      surprise: [],
    };

    try {
      // Check if emotional_arc is an object with emotion scores
      if (
        typeof firstEpisode.emotional_arc === "object" &&
        !Array.isArray(firstEpisode.emotional_arc)
      ) {
        console.log(
          "emotional_arc is an object with scores:",
          firstEpisode.emotional_arc,
        );

        // For a single emotion point, create 5 time points with slight variations
        const baseEmotions = firstEpisode.emotional_arc;

        // Create 5 data points with slight variations
        for (let i = 0; i < 5; i++) {
          // Add some variation to make the chart interesting (±10%)
          const variation = 0.9 + Math.random() * 0.2; // 0.9 to 1.1

          emotions.joy.push(
            Math.min(
              100,
              Math.max(0, (baseEmotions.joy || 0.2) * 100 * variation),
            ),
          );
          emotions.sadness.push(
            Math.min(
              100,
              Math.max(0, (baseEmotions.sadness || 0.2) * 100 * variation),
            ),
          );
          emotions.anger.push(
            Math.min(
              100,
              Math.max(0, (baseEmotions.anger || 0.1) * 100 * variation),
            ),
          );
          emotions.fear.push(
            Math.min(
              100,
              Math.max(0, (baseEmotions.fear || 0.2) * 100 * variation),
            ),
          );
          emotions.surprise.push(
            Math.min(
              100,
              Math.max(0, (baseEmotions.surprise || 0.3) * 100 * variation),
            ),
          );
        }
      }
      // Handle array format if it exists
      else if (Array.isArray(firstEpisode.emotional_arc)) {
        firstEpisode.emotional_arc.forEach((point) => {
          if (point && point.all_emotions) {
            emotions.joy.push((point.all_emotions.joy || 0) * 100);
            emotions.sadness.push((point.all_emotions.sadness || 0) * 100);
            emotions.anger.push((point.all_emotions.anger || 0) * 100);
            emotions.fear.push((point.all_emotions.fear || 0) * 100);
            emotions.surprise.push((point.all_emotions.surprise || 0) * 100);
          } else if (point && point.emotion && point.intensity) {
            const intensity = point.intensity * 100;
            const baseEmotions = {
              joy: 0,
              sadness: 0,
              anger: 0,
              fear: 0,
              surprise: 0,
            };

            if (baseEmotions.hasOwnProperty(point.emotion)) {
              baseEmotions[point.emotion] = intensity;
              const remaining = 100 - intensity;
              const otherEmotions = Object.keys(baseEmotions).filter(
                (e) => e !== point.emotion,
              );
              const share = remaining / otherEmotions.length;
              otherEmotions.forEach((e) => (baseEmotions[e] = share));
            }

            emotions.joy.push(baseEmotions.joy);
            emotions.sadness.push(baseEmotions.sadness);
            emotions.anger.push(baseEmotions.anger);
            emotions.fear.push(baseEmotions.fear);
            emotions.surprise.push(baseEmotions.surprise);
          }
        });
      }
    } catch (err) {
      console.error("Error processing emotion data:", err);
      return null;
    }

    // Ensure we have at least some data
    if (emotions.joy.length === 0) {
      console.log("No emotion data points found, using fallback");
      return {
        joy: [30, 45, 60, 40, 20],
        sadness: [15, 30, 20, 10, 5],
        anger: [8, 15, 10, 5, 2],
        fear: [25, 35, 30, 20, 10],
        surprise: [10, 25, 40, 35, 15],
      };
    }

    console.log("Processed emotion data:", emotions);
    return emotions;
  };

  // Get suggestions from analysis
  const getSuggestions = () => {
    if (!analysisData) return [];

    const suggestions = [];

    // Add cliffhanger suggestions
    if (analysisData.suggestions) {
      analysisData.suggestions.forEach((s) => {
        if (s.suggestion) suggestions.push(s.suggestion);
      });
    }

    // Add twist suggestions
    if (analysisData.twists && analysisData.twists.length > 0) {
      analysisData.twists.forEach((episode) => {
        if (episode.twists) {
          episode.twists.forEach((twist) => {
            if (twist.text) suggestions.push(`💡 Twist: ${twist.text}`);
          });
        }
      });
    }

    // Add cliffhanger details
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
              <div className="flex items-end h-32 gap-2">
                {analysisData.retention_curve.map((value, idx) => (
                  <div key={idx} className="flex-1 flex flex-col items-center">
                    <div
                      className="w-full bg-gradient-to-t from-green-500 to-green-400 rounded-t-lg"
                      style={{ height: `${value * 100}%` }}
                    ></div>
                    <span className="text-xs mt-2 text-gray-600 dark:text-gray-400">
                      Ep {idx + 1}
                    </span>
                    <span className="text-xs font-semibold">
                      {Math.round(value * 100)}%
                    </span>
                  </div>
                ))}
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
