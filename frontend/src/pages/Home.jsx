import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import { analyzeStory, validateStory } from "../services/api";

const Home = () => {
  const [story, setStory] = useState("");
  const [title, setTitle] = useState("");
  const [episodes, setEpisodes] = useState(5);
  const [snowflakes, setSnowflakes] = useState([]);
  const [isSnowEnabled, setIsSnowEnabled] = useState(true);
  const [validationMessage, setValidationMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { isDark } = useTheme();

  const emotionEmojis = [
    "😊",
    "😢",
    "😠",
    "😨",
    "😲",
    "🥰",
    "🤔",
    "😌",
    "🥺",
    "😤",
    "🤯",
    "🥳",
  ];

  // Snow effect
  useEffect(() => {
    if (!isSnowEnabled) return;

    const createSnowflake = () => {
      const useEmoji = Math.random() < 0.15;
      const randomEmoji =
        emotionEmojis[Math.floor(Math.random() * emotionEmojis.length)];

      const snowflake = {
        id: Math.random(),
        left: Math.random() * 100,
        animationDuration: 5 + Math.random() * 8,
        opacity: useEmoji
          ? 0.7 + Math.random() * 0.3
          : 0.1 + Math.random() * 0.2,
        size: useEmoji ? 14 + Math.random() * 10 : 2 + Math.random() * 4,
        isEmoji: useEmoji,
        emojiChar: randomEmoji,
      };

      setSnowflakes((prev) => [...prev, snowflake]);

      setTimeout(() => {
        setSnowflakes((prev) => prev.filter((s) => s.id !== snowflake.id));
      }, snowflake.animationDuration * 1000);
    };

    for (let i = 0; i < 30; i++) {
      setTimeout(createSnowflake, i * 50);
    }

    const interval = setInterval(createSnowflake, 300);
    return () => clearInterval(interval);
  }, [isSnowEnabled, isDark]);

  const handleAnalyze = async (e) => {
    e.preventDefault();

    if (!story.trim()) {
      alert("Please enter a story");
      return;
    }

    setLoading(true);
    setError("");
    setValidationMessage("");

    try {
      const data = await analyzeStory(story, title, episodes);

      if (data && data.success) {
        navigate("/results", {
          state: {
            story,
            storyTitle: title || "Untitled Story",
            analysisData: data.data,
          },
        });
      } else {
        setError(data?.error || "Analysis failed");
        setLoading(false);
      }
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleValidate = async () => {
    if (!story.trim()) {
      alert("Please enter a story");
      return;
    }

    setLoading(true);
    setError("");
    setValidationMessage("");

    try {
      const data = await validateStory(story);
      if (data && data.success) {
        const { valid, length, estimated_episodes } = data.data;
        setValidationMessage(
          valid
            ? `✅ Valid story! ${length} chars, estimated ${estimated_episodes} episodes`
            : `❌ Story too short (min 50 chars)`,
        );
      } else {
        setValidationMessage(`❌ ${data?.error || "Validation failed"}`);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300 relative overflow-hidden">
      {/* Snowfall Toggle Button */}
      <button
        onClick={() => setIsSnowEnabled(!isSnowEnabled)}
        className="fixed top-20 right-4 z-50 p-3 bg-white dark:bg-gray-800 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-110"
        title={isSnowEnabled ? "Turn off effects" : "Turn on effects"}
      >
        {isSnowEnabled ? (isDark ? "❄️" : "😊") : "☀️"}
      </button>

      {/* Floating Emojis/Snow Effect */}
      {isSnowEnabled && (
        <div className="fixed inset-0 pointer-events-none z-10">
          {snowflakes.map((flake) => (
            <div
              key={flake.id}
              className="absolute animate-snowfall"
              style={{
                left: `${flake.left}%`,
                top: "-10%",
                fontSize: flake.isEmoji ? `${flake.size}px` : "0",
                width: !flake.isEmoji ? `${flake.size}px` : "auto",
                height: !flake.isEmoji ? `${flake.size}px` : "auto",
                opacity: flake.opacity,
                animationDuration: `${flake.animationDuration}s`,
                backgroundColor: !flake.isEmoji
                  ? isDark
                    ? "#e5e7eb"
                    : "#ffffff"
                  : "transparent",
                borderRadius: !flake.isEmoji ? "50%" : "0",
              }}
            >
              {flake.isEmoji && (isDark ? "❄️" : flake.emojiChar)}
            </div>
          ))}
        </div>
      )}

      {/* Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-black/50 dark:bg-black/70 z-50 flex items-center justify-center">
          <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-2xl max-w-md w-full mx-4">
            <div className="flex flex-col items-center text-center">
              <div className="w-20 h-20 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-6"></div>
              <h3 className="text-2xl font-bold text-gray-800 dark:text-white mb-2">
                Analyzing Your Story
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                This may take a few moments...
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-500">
                Processing emotions and cliffhangers
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="relative z-20 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero Section */}
        <div className="text-center mb-12 animate-fade-in">
          <div className="flex justify-center space-x-4 text-6xl mb-6">
            {["📚", "✨", "🎭", "✍️"].map((emoji, i) => (
              <span
                key={i}
                className="transform hover:scale-110 transition-transform duration-300 animate-bounce-slow"
                style={{ animationDelay: `${i * 0.2}s` }}
              >
                {emoji}
              </span>
            ))}
          </div>

          <h1 className="text-5xl sm:text-6xl md:text-7xl font-black mb-4">
            <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 dark:from-blue-400 dark:via-purple-400 dark:to-pink-400 text-transparent bg-clip-text bg-300% animate-gradient">
              Story Analyzer
            </span>
          </h1>

          <p className="text-lg sm:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto leading-relaxed">
            Paste your story and get AI-powered insights about{" "}
            <span className="text-blue-600 dark:text-blue-400 font-semibold px-2 py-1 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
              emotions
            </span>{" "}
            and{" "}
            <span className="text-purple-600 dark:text-purple-400 font-semibold px-2 py-1 bg-purple-50 dark:bg-purple-900/30 rounded-lg">
              cliffhangers
            </span>
          </p>
        </div>

        {/* Feature Cards - REMOVED Smart Suggestions */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-12">
          {[
            {
              emoji: "📊",
              title: "Emotion Analysis",
              desc: "Track emotions throughout your story",
              color: "from-blue-400 to-blue-600",
            },
            {
              emoji: "⚡",
              title: "Cliffhanger Score",
              desc: "Measure suspense and engagement",
              color: "from-purple-400 to-purple-600",
            },
            {
              emoji: "🎭",
              title: "Plot Twists",
              desc: "Get AI-powered twist suggestions",
              color: "from-indigo-400 to-indigo-600",
            },
          ].map((card, i) => (
            <div
              key={i}
              className="group relative animate-slide-up h-full"
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              <div
                className={`absolute inset-0 bg-gradient-to-r ${card.color} opacity-0 group-hover:opacity-10 dark:group-hover:opacity-20 rounded-2xl transition-opacity duration-500`}
              />
              <div className="relative bg-white dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-2xl p-6 transform transition-all duration-300 hover:-translate-y-2 border border-gray-100 dark:border-gray-700 h-full flex flex-col">
                <div className="text-5xl mb-4 group-hover:scale-110 group-hover:rotate-12 transition-transform duration-300">
                  {card.emoji}
                </div>
                <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-2">
                  {card.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 flex-grow">
                  {card.desc}
                </p>
                <div
                  className={`absolute bottom-0 left-0 h-1 w-0 group-hover:w-full bg-gradient-to-r ${card.color} transition-all duration-500 rounded-b-2xl`}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Story Input Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 sm:p-8 mb-12 border border-gray-100 dark:border-gray-700">
          <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-4 flex items-center">
            <span className="bg-blue-100 dark:bg-blue-900/50 p-2 rounded-lg mr-3 animate-pulse-slow">
              📝
            </span>
            Your Story
          </h2>

          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Story Title (optional)"
            className="w-full mb-4 p-3 border-2 border-gray-200 dark:border-gray-700 rounded-lg 
                     focus:border-blue-500 dark:focus:border-blue-400 focus:ring-4 focus:ring-blue-100 dark:focus:ring-blue-900/30 
                     outline-none transition-all bg-gray-50 dark:bg-gray-900 text-gray-700 dark:text-gray-300"
          />

          <textarea
            className="w-full h-48 sm:h-64 p-4 border-2 border-gray-200 dark:border-gray-700 rounded-xl 
                     focus:border-blue-500 dark:focus:border-blue-400 focus:ring-4 focus:ring-blue-100 dark:focus:ring-blue-900/30 
                     outline-none transition-all resize-none text-gray-700 dark:text-gray-300
                     placeholder-gray-400 dark:placeholder-gray-500 bg-gray-50 dark:bg-gray-900"
            placeholder="Once upon a time..."
            value={story}
            onChange={(e) => setStory(e.target.value)}
          />

          {/* Episodes Slider */}
          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Number of Episodes:{" "}
              <span className="text-blue-600 font-bold">{episodes}</span>
            </label>
            <input
              type="range"
              min="3"
              max="10"
              value={episodes}
              onChange={(e) => setEpisodes(parseInt(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
            />
            <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
              <span>3 episodes</span>
              <span>10 episodes</span>
            </div>
          </div>

          {/* Character and Word Counter */}
          <div className="flex space-x-4 text-sm mt-4">
            <span className="bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full text-gray-600 dark:text-gray-300">
              📝 {story.length} characters
            </span>
            <span className="bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full text-gray-600 dark:text-gray-300">
              📊 {story.split(" ").filter((w) => w).length} words
            </span>
          </div>

          {/* Validation Message */}
          {validationMessage && (
            <div
              className={`mt-4 p-3 rounded-lg ${
                validationMessage.includes("✅")
                  ? "bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-300"
                  : "bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300"
              }`}
            >
              {validationMessage}
            </div>
          )}

          {/* Error Message */}
          {error && !loading && (
            <div className="mt-4 p-3 bg-red-50 dark:bg-red-900/20 rounded-lg text-red-800 dark:text-red-300">
              Error: {error}
            </div>
          )}

          {/* Buttons */}
          <div className="flex flex-wrap gap-4 justify-center mt-6">
            <button
              onClick={handleAnalyze}
              disabled={loading || !story.trim()}
              className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold text-lg hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {loading ? (
                <>
                  <span className="animate-spin">⏳</span>
                  Analyzing...
                </>
              ) : (
                <>
                  <span>✨</span>
                  Analyze Story
                </>
              )}
            </button>

            <button
              onClick={handleValidate}
              disabled={loading || !story.trim()}
              className="px-6 py-4 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-xl font-semibold text-lg hover:bg-gray-300 dark:hover:bg-gray-600 transform hover:scale-105 transition-all duration-300 disabled:opacity-50"
            >
              Quick Validate
            </button>

            {story && (
              <button
                onClick={() => {
                  setStory("");
                  setTitle("");
                  setEpisodes(5);
                  setValidationMessage("");
                  setError("");
                }}
                className="px-6 py-4 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-xl font-semibold text-lg hover:bg-gray-300 dark:hover:bg-gray-600 transform hover:scale-105 transition-all duration-300"
              >
                Reset
              </button>
            )}
          </div>
        </div>

        {/* Example Stories Section */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6 text-center">
            Try Example Stories
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              {
                emoji: "🌄",
                title: "Mystery Story",
                desc: "Secrets and revelations",
                story:
                  "In a small village nestled between misty mountains, an old clock tower held secrets that no one dared to uncover. Until one stormy night, when lightning struck and everything changed...",
              },
              {
                emoji: "❤️",
                title: "Love Story",
                desc: "Heartwarming romance",
                story:
                  "Sarah never believed in love at first sight until she walked into the old bookstore and saw him reading her favorite novel. Their eyes met, and time stood still as they discovered their shared love for stories.",
              },
              {
                emoji: "🚀",
                title: "Sci-Fi",
                desc: "Intergalactic adventure",
                story:
                  "Captain Ray's ship was caught in a cosmic storm when an alien vessel emerged from the vortex. First contact was about to begin, and humanity wasn't ready for what the stars had brought.",
              },
            ].map((example, i) => (
              <button
                key={i}
                onClick={() => {
                  setStory(example.story);
                  setTitle(example.title);
                }}
                className="group bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md hover:shadow-2xl transition-all duration-300 text-left border border-gray-100 dark:border-gray-700 transform hover:-translate-y-2"
              >
                <span className="text-4xl block mb-3 group-hover:scale-110 group-hover:rotate-12 transition-transform duration-300">
                  {example.emoji}
                </span>
                <h3 className="font-semibold text-gray-800 dark:text-white mb-1">
                  {example.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                  {example.desc}
                </p>
                <span className="text-blue-600 dark:text-blue-400 text-sm font-medium group-hover:underline">
                  Click to use →
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Snowfall animation */}
      <style>{`
        @keyframes snowfall {
          0% { transform: translateY(0) rotate(0deg); }
          100% { transform: translateY(100vh) rotate(360deg); }
        }
        .animate-snowfall {
          animation: snowfall linear forwards;
        }
      `}</style>
    </div>
  );
};

export default Home;
