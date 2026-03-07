import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import ScoreMeter from "../components/analysis/ScoreMeter";
import EmotionChart from "../components/analysis/EmotionChart";

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [analysisData, setAnalysisData] = useState(null);
  const [storySaved, setStorySaved] = useState(false);
  const [sparkles, setSparkles] = useState([]);

  // Sparkle effect
  useEffect(() => {
    const sparkleArray = [];
    for (let i = 0; i < 20; i++) {
      sparkleArray.push({
        id: i,
        left: Math.random() * 100,
        top: Math.random() * 100,
        size: 4 + Math.random() * 8,
        delay: Math.random() * 3,
        duration: 2 + Math.random() * 3,
      });
    }
    setSparkles(sparkleArray);
  }, []);

  const story = location.state?.story || "";
  const storyTitle = location.state?.storyTitle || "Untitled Story";
  const passedAnalysisData = location.state?.analysisData || null;

  useEffect(() => {
    if (passedAnalysisData) {
      setAnalysisData(passedAnalysisData);
    } else if (!story) {
      navigate("/");
    }
  }, [passedAnalysisData, story, navigate]);

  useEffect(() => {
    if (analysisData && story && !storySaved) {
      saveStoryToDashboard();
    }
  }, [analysisData, story, storySaved]);

  const saveStoryToDashboard = () => {
    try {
      const savedStories = JSON.parse(localStorage.getItem("stories") || "[]");
      const cliffhangerScore =
        analysisData.overall_scores?.cliffhanger_quality || 0;
      const retentionScore =
        analysisData.overall_scores?.retention_prediction || 0;
      const avgScore = Math.round(cliffhangerScore * 50 + retentionScore * 50);

      const newStory = {
        id: Date.now(),
        title: storyTitle,
        date: new Date().toLocaleDateString("en-CA"),
        score: avgScore,
        preview: story.substring(0, 100) + "...",
        fullStory: story,
        analysisData: analysisData,
        cliffhangerScore: Math.round(cliffhangerScore * 100),
        retentionScore: Math.round(retentionScore * 100),
      };

      const updatedStories = [newStory, ...savedStories];
      localStorage.setItem("stories", JSON.stringify(updatedStories));
      setStorySaved(true);
    } catch (error) {
      console.error("Error saving story:", error);
    }
  };

  const prepareEmotionData = () => {
    if (!analysisData?.episodes?.length) return null;
    const emotions = {
      joy: [],
      sadness: [],
      anger: [],
      fear: [],
      surprise: [],
    };

    try {
      for (const episode of analysisData.episodes) {
        const arc = episode.emotional_arc;
        if (!arc) continue;

        if (Array.isArray(arc) && arc.length > 0) {
          const epEmotions = {
            joy: 0,
            sadness: 0,
            anger: 0,
            fear: 0,
            surprise: 0,
          };
          let count = 0;

          for (const point of arc) {
            if (point?.all_emotions) {
              epEmotions.joy += point.all_emotions.joy || 0;
              epEmotions.sadness += point.all_emotions.sadness || 0;
              epEmotions.anger += point.all_emotions.anger || 0;
              epEmotions.fear += point.all_emotions.fear || 0;
              epEmotions.surprise += point.all_emotions.surprise || 0;
              count++;
            }
          }

          if (count > 0) {
            emotions.joy.push(Math.round((epEmotions.joy / count) * 100));
            emotions.sadness.push(
              Math.round((epEmotions.sadness / count) * 100),
            );
            emotions.anger.push(Math.round((epEmotions.anger / count) * 100));
            emotions.fear.push(Math.round((epEmotions.fear / count) * 100));
            emotions.surprise.push(
              Math.round((epEmotions.surprise / count) * 100),
            );
          }
        }
      }
    } catch (err) {
      console.error("Error processing emotion data:", err);
      return null;
    }

    return emotions.joy.length ? emotions : null;
  };

  const emotionData = prepareEmotionData();
  const cliffhangerDisplay = analysisData?.overall_scores?.cliffhanger_quality
    ? Math.round(analysisData.overall_scores.cliffhanger_quality * 100)
    : 0;
  const retentionDisplay = analysisData?.overall_scores?.retention_prediction
    ? Math.round(analysisData.overall_scores.retention_prediction * 100)
    : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-indigo-950 dark:to-purple-950 transition-colors duration-300 relative overflow-hidden">
      {/* Sparkle Animation Background */}
      <div className="fixed inset-0 pointer-events-none z-0">
        {sparkles.map((sparkle) => (
          <div
            key={sparkle.id}
            className="absolute bg-yellow-300 dark:bg-purple-300 rounded-full"
            style={{
              left: `${sparkle.left}%`,
              top: `${sparkle.top}%`,
              width: `${sparkle.size}px`,
              height: `${sparkle.size}px`,
              opacity: 0.3,
              animation: `sparkle ${sparkle.duration}s ease-in-out infinite`,
              animationDelay: `${sparkle.delay}s`,
            }}
          />
        ))}
      </div>

      {/* Floating Orbs */}
      <div className="fixed inset-0 pointer-events-none z-0">
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="absolute rounded-full bg-gradient-to-r from-purple-300/20 to-pink-300/20 dark:from-purple-600/10 dark:to-pink-600/10"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              width: `${100 + Math.random() * 200}px`,
              height: `${100 + Math.random() * 200}px`,
              animation: `floatOrb ${20 + i * 5}s linear infinite`,
              filter: "blur(40px)",
            }}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 max-w-6xl mx-auto py-8 px-4">
        {/* Header with animation */}
        <div className="flex items-center mb-8 animate-slide-in-left">
          <button
            onClick={() => navigate("/")}
            className="px-6 py-2 bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm text-gray-800 dark:text-gray-200 rounded-lg font-semibold hover:bg-white hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl flex items-center gap-2 group"
          >
            <span className="group-hover:-translate-x-1 transition-transform duration-300">
              ←
            </span>
            Back
          </button>
          <h1 className="text-3xl font-bold ml-4 bg-gradient-to-r from-purple-600 to-pink-600 dark:from-purple-400 dark:to-pink-400 text-transparent bg-clip-text animate-pulse-slow">
            Analysis Results
          </h1>
        </div>

        {analysisData ? (
          <>
            {/* Story Preview Card with glow effect */}
            <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl shadow-2xl p-6 mb-8 border border-purple-200 dark:border-purple-800 animate-scale-in group hover:shadow-purple-200/50 dark:hover:shadow-purple-900/50 transition-shadow duration-500">
              <h2 className="text-xl font-semibold mb-2 flex items-center gap-2">
                <span className="text-2xl animate-wiggle">📖</span>
                Your Story
              </h2>
              <p className="text-gray-600 dark:text-gray-300 line-clamp-3">
                {story.substring(0, 200)}...
              </p>
              <div className="mt-2 text-sm text-gray-500 dark:text-gray-400 flex items-center gap-4">
                <span className="flex items-center gap-1">
                  <span className="animate-pulse">🌐</span>{" "}
                  {analysisData.language || "en"}
                </span>
                <span className="flex items-center gap-1">
                  <span className="animate-pulse">📺</span>{" "}
                  {analysisData.total_episodes} episodes
                </span>
                {storySaved && (
                  <span className="ml-4 text-green-600 flex items-center gap-1 animate-bounce-subtle">
                    ✓ Saved to library
                  </span>
                )}
              </div>
            </div>

            {/* Scores Grid with animations */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div
                className="animate-slide-up"
                style={{ animationDelay: "0.2s" }}
              >
                <ScoreMeter
                  label="Cliffhanger Score"
                  score={cliffhangerDisplay}
                  color="blue"
                />
              </div>
              <div
                className="animate-slide-up"
                style={{ animationDelay: "0.4s" }}
              >
                <ScoreMeter
                  label="Retention Score"
                  score={retentionDisplay}
                  color="green"
                />
              </div>
            </div>

            {/* Emotion Chart with fade in */}
            {emotionData && (
              <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl shadow-2xl p-6 mb-8 border border-purple-200 dark:border-purple-800 animate-fade-in">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <span className="text-2xl animate-float">📊</span>
                  Emotion Journey
                </h2>
                <EmotionChart data={emotionData} />
              </div>
            )}

            {/* Retention Curve with animated bars */}
            {analysisData.retention_curve && (
              <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl shadow-2xl p-6 mb-8 border border-purple-200 dark:border-purple-800 animate-scale-in">
                <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                  <span className="text-2xl animate-pulse">📈</span>
                  Retention Forecast
                </h2>
                <div className="flex items-end h-40 gap-2">
                  {analysisData.retention_curve.map((value, idx) => (
                    <div
                      key={idx}
                      className="flex-1 flex flex-col items-center group"
                    >
                      <div
                        className="w-full bg-gradient-to-t from-green-500 to-green-400 rounded-t-lg transform transition-all duration-700 hover:scale-y-110 hover:shadow-lg"
                        style={{
                          height: `${value * 100}%`,
                          minHeight: "4px",
                          animation: `barGrow 0.5s ease-out ${idx * 0.1}s both`,
                        }}
                      />
                      <span className="text-xs mt-2">Ep {idx + 1}</span>
                      <span className="text-xs font-semibold">
                        {Math.round(value * 100)}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* View Episodes Button with pulse effect */}
            <div className="flex justify-center mt-8 animate-bounce-in">
              <button
                onClick={() => navigate("/episodes", { state: location.state })}
                className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold text-lg hover:from-purple-700 hover:to-pink-700 transform hover:scale-105 transition-all duration-300 shadow-2xl hover:shadow-purple-500/50 flex items-center gap-2 group relative overflow-hidden"
              >
                <span className="relative z-10 flex items-center gap-2">
                  <span className="text-2xl group-hover:rotate-12 transition-transform duration-300">
                    📺
                  </span>
                  View Episodes
                  <span className="text-2xl group-hover:translate-x-2 transition-transform duration-300">
                    ✨
                  </span>
                </span>
                <div className="absolute inset-0 bg-white/20 transform -skew-x-12 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>
              </button>
            </div>
          </>
        ) : (
          <div className="text-center py-20 animate-fade-in">
            <div className="text-8xl mb-4 animate-float">📊</div>
            <p className="text-gray-500 dark:text-gray-400 text-xl mb-4">
              No analysis data available.
            </p>
            <button
              onClick={() => navigate("/")}
              className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold hover:from-purple-700 hover:to-pink-700 transform hover:scale-105 transition-all duration-300 shadow-xl"
            >
              Analyze a Story ✨
            </button>
          </div>
        )}
      </div>

      {/* Animation Keyframes */}
      <style>{`
        @keyframes sparkle {
          0%, 100% { opacity: 0.2; transform: scale(1); }
          50% { opacity: 0.6; transform: scale(1.5); }
        }

        @keyframes floatOrb {
          0% { transform: translate(0, 0) scale(1); }
          25% { transform: translate(50px, -30px) scale(1.1); }
          50% { transform: translate(100px, 0) scale(1); }
          75% { transform: translate(50px, 30px) scale(0.9); }
          100% { transform: translate(0, 0) scale(1); }
        }

        @keyframes slide-in-left {
          from { transform: translateX(-50px); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }

        @keyframes scale-in {
          from { transform: scale(0.9); opacity: 0; }
          to { transform: scale(1); opacity: 1; }
        }

        @keyframes fade-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }

        @keyframes barGrow {
          from { height: 0; }
          to { height: attr(data-height); }
        }

        @keyframes bounce-in {
          0% { transform: scale(0.3); opacity: 0; }
          50% { transform: scale(1.05); }
          70% { transform: scale(0.9); }
          100% { transform: scale(1); opacity: 1; }
        }

        .animate-slide-in-left {
          animation: slide-in-left 0.6s ease-out forwards;
        }

        .animate-scale-in {
          animation: scale-in 0.5s ease-out forwards;
        }

        .animate-fade-in {
          animation: fade-in 1s ease-out forwards;
        }

        .animate-bounce-in {
          animation: bounce-in 0.8s ease-out forwards;
        }

        .animate-float {
          animation: floatOrb 6s ease-in-out infinite;
        }

        .animate-wiggle {
          animation: wiggle 2s ease-in-out infinite;
        }

        @keyframes wiggle {
          0%, 100% { transform: rotate(0deg); }
          25% { transform: rotate(-5deg); }
          75% { transform: rotate(5deg); }
        }
      `}</style>
    </div>
  );
};

export default Results;
