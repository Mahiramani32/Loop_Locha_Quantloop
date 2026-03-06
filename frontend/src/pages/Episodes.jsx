import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useStory } from "../hooks/useStory";

const Episodes = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [episodes, setEpisodes] = useState([]);
  const [genre, setGenre] = useState("Thriller");
  const [tone, setTone] = useState("Suspenseful");
  const [selectedEpisode, setSelectedEpisode] = useState(null);
  const [loading, setLoading] = useState(false);

  // Get story data from location
  const story = location.state?.story || "";
  const storyTitle = location.state?.storyTitle || "Your Story";
  const storyId = location.state?.storyId || null;
  const analysisData = location.state?.analysisData || null;

  // Use analysis data if available
  useEffect(() => {
    const loadEpisodes = async () => {
      setLoading(true);
      try {
        // If we have analysis data from Results page, use it
        if (analysisData && analysisData.episodes) {
          console.log("Raw episode data from backend:", analysisData.episodes);

          // Extract per-episode suggestions from the structured suggestions object
          const allSuggestions = [];
          if (analysisData.suggestions) {
            const sug = analysisData.suggestions;
            if (sug.critical || sug.improvement || sug.tips) {
              ["critical", "improvement", "tips"].forEach((cat) => {
                if (Array.isArray(sug[cat])) {
                  sug[cat].forEach((s) => {
                    if (s.text) allSuggestions.push({ ...s, category: cat });
                  });
                }
              });
            }
          }

          const formattedEpisodes = analysisData.episodes.map((ep, index) => {
            const epNum = ep.episode_number || index + 1;

            // Get the best available description - PRIORITIZE description field
            let description = "";
            if (ep.description && ep.description.trim() !== "") {
              description = ep.description;
              console.log(`Episode ${epNum}: Using description`);
            } else if (ep.summary && ep.summary.trim() !== "") {
              description = ep.summary;
              console.log(`Episode ${epNum}: Using summary`);
            } else if (ep.content && ep.content.trim() !== "") {
              description = ep.content;
              console.log(`Episode ${epNum}: Using content`);
            } else {
              description =
                "No description available for this episode. Generate a new story to see more detailed episode plots.";
            }

            // Find suggestions for this episode
            const episodeSuggestions = allSuggestions.filter(
              (s) => s.episode === epNum,
            );

            return {
              id: epNum,
              number: epNum,
              title: ep.title || `Episode ${epNum}`,
              description: description,
              summary: ep.summary || "",
              cliffhanger: ep.cliffhanger || "To be continued...",
              emotional_arc: ep.emotional_arc || [],
              cliffhanger_score: ep.cliffhanger_score || 0,
              retention_score: ep.retention_score || 0,
              genre: ep.genre || "general",
              twist_suggestions:
                analysisData.twists?.find((t) => t.episode === epNum)?.twists ||
                [],
              suggestions: episodeSuggestions,
            };
          });

          console.log("Formatted episodes:", formattedEpisodes);
          setEpisodes(formattedEpisodes);
          setSelectedEpisode(formattedEpisodes[0]);
        }
        // Otherwise fetch from backend using story ID (future implementation)
        else if (storyId) {
          console.log("Fetch episodes by ID:", storyId);
        }
      } catch (error) {
        console.error("Error loading episodes:", error);
      } finally {
        setLoading(false);
      }
    };

    loadEpisodes();
  }, [analysisData, storyId]);

  const genres = [
    "Thriller",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Fantasy",
    "Horror",
    "Drama",
    "Comedy",
  ];
  const tones = [
    "Suspenseful",
    "Dark",
    "Light-hearted",
    "Mysterious",
    "Action-packed",
    "Emotional",
    "Humorous",
    "Serious",
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300 relative overflow-hidden">
      {/* Floating Emojis Background */}
      <div className="fixed inset-0 pointer-events-none opacity-10 dark:opacity-20">
        {["📺", "🎬", "📽️", "🎭", "📝", "✨"].map((emoji, i) => (
          <span
            key={i}
            className="absolute text-8xl animate-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${i * 0.5}s`,
              animationDuration: `${3 + i}s`,
            }}
          >
            {emoji}
          </span>
        ))}
      </div>

      {/* Main Content */}
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header with Back Button */}
        <div className="flex items-center mb-6 animate-fade-in">
          <button
            onClick={() => navigate(-1)}
            className="px-6 py-2 bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-lg font-semibold hover:bg-gray-300 dark:hover:bg-gray-600 transform hover:scale-105 transition-all duration-300"
          >
            ← Back
          </button>
          <h1 className="text-3xl font-bold text-gray-800 dark:text-white ml-4">
            Story Episodes
          </h1>
        </div>

        {/* Story Title */}
        <div className="mb-4 text-gray-600 dark:text-gray-400 animate-slide-up">
          <span className="font-medium">Story:</span> {storyTitle}
        </div>

        {/* Story Preview Card */}
        {story && (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 mb-6 border border-gray-100 dark:border-gray-700 animate-slide-up">
            <p className="text-gray-600 dark:text-gray-300 text-sm line-clamp-2">
              <span className="text-blue-600 dark:text-blue-400 mr-2">📖</span>
              {typeof story === "string"
                ? story.substring(0, 150) + "..."
                : "Your story"}
            </p>
          </div>
        )}

        {/* Controls Row */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 mb-8 border border-gray-100 dark:border-gray-700 transform transition-all duration-300 hover:shadow-2xl animate-slide-up">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            {/* Genre Dropdown */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Genre
              </label>
              <select
                value={genre}
                onChange={(e) => setGenre(e.target.value)}
                className="w-full p-3 rounded-lg border-2 border-gray-200 dark:border-gray-700 
                         bg-white dark:bg-gray-900 text-gray-800 dark:text-white
                         focus:border-blue-500 dark:focus:border-blue-400 focus:ring-4 focus:ring-blue-100 dark:focus:ring-blue-900/30 
                         outline-none transition-all"
              >
                {genres.map((g) => (
                  <option key={g} value={g}>
                    {g}
                  </option>
                ))}
              </select>
            </div>

            {/* Episodes Info - DYNAMIC COUNT */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Episodes
              </label>
              <div className="p-3 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800 rounded-lg text-gray-800 dark:text-white font-semibold border-2 border-gray-200 dark:border-gray-700">
                {loading ? "Loading..." : `${episodes.length} Episodes`}
              </div>
            </div>

            {/* Tone Dropdown */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Tone
              </label>
              <select
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                className="w-full p-3 rounded-lg border-2 border-gray-200 dark:border-gray-700 
                         bg-white dark:bg-gray-900 text-gray-800 dark:text-white
                         focus:border-blue-500 dark:focus:border-blue-400 focus:ring-4 focus:ring-blue-100 dark:focus:ring-blue-900/30 
                         outline-none transition-all"
              >
                {tones.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>

            {/* Generate Button */}
            <div>
              <button
                onClick={() => {
                  alert(
                    "Regenerate feature coming soon! This will use the backend to create new episodes with different genre/tone.",
                  );
                }}
                className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                Regenerate Arc <span className="ml-2">✨</span>
              </button>
            </div>
          </div>
        </div>

        {/* Loading State */}
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
          </div>
        ) : (
          /* Two Column Layout - Episodes List + Selected Episode Detail */
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Episodes List - Left Column */}
            <div className="lg:col-span-1">
              <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-4 border border-gray-100 dark:border-gray-700">
                <h2 className="text-lg font-semibold text-gray-800 dark:text-white mb-4 px-2">
                  Episodes ({episodes.length})
                </h2>
                <div className="space-y-2 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                  {episodes.map((ep, index) => (
                    <button
                      key={ep.id}
                      onClick={() => setSelectedEpisode(ep)}
                      className={`w-full text-left p-4 rounded-xl transition-all duration-300 transform hover:scale-102
                                ${
                                  selectedEpisode?.id === ep.id
                                    ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg"
                                    : "bg-gray-50 dark:bg-gray-700/50 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 hover:shadow-md"
                                }`}
                    >
                      <div className="font-medium flex items-center text-lg mb-1">
                        <span className="mr-2">📺</span>
                        Episode {ep.number || index + 1}:{" "}
                        {ep.title.replace(/^Episode \d+:\s*/, "")}
                      </div>
                      <div
                        className={`text-sm text-left mt-2 ${selectedEpisode?.id === ep.id ? "text-blue-100" : "text-gray-600 dark:text-gray-300"} ${selectedEpisode?.id !== ep.id && "line-clamp-2"}`}
                      >
                        <span className="font-semibold">Summary:</span>{" "}
                        {ep.summary || ep.description}
                      </div>
                      {ep.cliffhanger && (
                        <div
                          className={`text-sm text-left mt-1 line-clamp-2 ${selectedEpisode?.id === ep.id ? "text-yellow-100" : "text-gray-600 dark:text-gray-300"}`}
                        >
                          <span
                            className={`font-semibold ${selectedEpisode?.id === ep.id ? "text-yellow-200" : "text-amber-600 dark:text-amber-400"}`}
                          >
                            Cliffhanger:
                          </span>{" "}
                          {ep.cliffhanger}
                        </div>
                      )}
                      <div className="flex items-center gap-2 mt-3 flex-wrap">
                        {ep.cliffhanger_score > 0 && (
                          <span className="text-xs px-2 py-1 bg-blue-100 dark:bg-blue-900/30 rounded-full">
                            ⚡ Cliff: {(ep.cliffhanger_score * 100).toFixed(0)}%
                          </span>
                        )}
                        {ep.retention_score > 0 && (
                          <span className="text-xs px-2 py-1 bg-green-100 dark:bg-green-900/30 rounded-full">
                            📈 Ret: {(ep.retention_score * 100).toFixed(0)}%
                          </span>
                        )}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Selected Episode Detail - Right Column */}
            <div className="lg:col-span-2">
              {selectedEpisode && (
                <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700 transform transition-all duration-300 hover:shadow-2xl">
                  {/* Episode Header */}
                  <div className="flex flex-col sm:flex-row justify-between items-start gap-4 mb-6">
                    <div>
                      <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-2">
                        {selectedEpisode.title}
                      </h2>
                      <p className="text-gray-600 dark:text-gray-400 flex items-center">
                        <span className="mr-2">📺</span>
                        Episode{" "}
                        {selectedEpisode.number ||
                          episodes.findIndex(
                            (e) => e.id === selectedEpisode.id,
                          ) + 1}{" "}
                        of {episodes.length}
                      </p>
                      {selectedEpisode.cliffhanger_score > 0 && (
                        <div className="flex gap-4 mt-2">
                          <span className="text-sm px-3 py-1 bg-blue-100 dark:bg-blue-900/30 rounded-full">
                            Cliffhanger:{" "}
                            {(selectedEpisode.cliffhanger_score * 100).toFixed(
                              0,
                            )}
                            %
                          </span>
                          <span className="text-sm px-3 py-1 bg-green-100 dark:bg-green-900/30 rounded-full">
                            Retention:{" "}
                            {(selectedEpisode.retention_score * 100).toFixed(0)}
                            %
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Action Buttons */}
                    <div className="flex flex-wrap gap-2">
                      <button
                        onClick={() =>
                          alert("Regenerate episode feature coming soon!")
                        }
                        className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-all duration-300 transform hover:scale-105 text-sm font-medium"
                      >
                        🔄 Regenerate
                      </button>
                      <button
                        onClick={() =>
                          alert("Improve cliffhanger feature coming soon!")
                        }
                        className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-all duration-300 transform hover:scale-105 text-sm font-medium"
                      >
                        ⚡ Improve Cliffhanger
                      </button>
                      <button
                        onClick={() => {
                          // Export episode as text
                          const element = document.createElement("a");
                          const file = new Blob(
                            [
                              `${selectedEpisode.title}\n\n${selectedEpisode.description}`,
                              selectedEpisode.cliffhanger
                                ? `\n\nCliffhanger: ${selectedEpisode.cliffhanger}`
                                : "",
                            ],
                            { type: "text/plain" },
                          );
                          element.href = URL.createObjectURL(file);
                          element.download = `episode-${selectedEpisode.number || 1}.txt`;
                          document.body.appendChild(element);
                          element.click();
                        }}
                        className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 text-sm font-medium shadow-md"
                      >
                        📤 Export
                      </button>
                    </div>
                  </div>

                  {/* Episode Content - Full Description */}
                  <div className="prose dark:prose-invert max-w-none bg-gray-50 dark:bg-gray-700/30 p-4 rounded-xl border border-gray-100 dark:border-gray-700">
                    <p className="text-gray-700 dark:text-gray-300 leading-relaxed max-w-none text-base">
                      <span className="font-semibold block mb-2 text-gray-900 dark:text-white">
                        Full Description:
                      </span>
                      {selectedEpisode.description}
                    </p>
                  </div>

                  {/* Twist Suggestions from backend */}
                  {selectedEpisode.twist_suggestions &&
                    selectedEpisode.twist_suggestions.length > 0 && (
                      <div className="mt-6 p-4 bg-gradient-to-r from-purple-50 to-indigo-50 dark:from-purple-900/20 dark:to-indigo-900/20 rounded-xl border border-purple-200 dark:border-purple-800">
                        <h3 className="text-sm font-semibold text-purple-800 dark:text-purple-300 mb-2 flex items-center">
                          <span className="mr-2">🎭</span>
                          Plot Twists
                        </h3>
                        <ul className="space-y-2">
                          {selectedEpisode.twist_suggestions.map(
                            (twist, idx) => (
                              <li key={idx} className="flex items-start gap-2">
                                <span className="text-purple-600 mt-1">✨</span>
                                <span className="text-purple-700 dark:text-purple-400 text-sm">
                                  {twist.text || twist}
                                </span>
                              </li>
                            ),
                          )}
                        </ul>
                      </div>
                    )}

                  {/* AI Suggestions for this episode */}
                  {selectedEpisode.suggestions &&
                    selectedEpisode.suggestions.length > 0 && (
                      <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 rounded-xl border border-blue-200 dark:border-blue-800">
                        <h3 className="text-sm font-semibold text-blue-800 dark:text-blue-300 mb-2 flex items-center">
                          <span className="mr-2">💡</span>
                          Suggestions
                        </h3>
                        <ul className="space-y-2">
                          {selectedEpisode.suggestions.map((sug, idx) => (
                            <li key={idx} className="flex items-start gap-2">
                              <span
                                className={`mt-1 ${
                                  sug.category === "critical"
                                    ? "text-red-500"
                                    : sug.category === "improvement"
                                      ? "text-yellow-500"
                                      : "text-blue-500"
                                }`}
                              >
                                •
                              </span>
                              <span className="text-blue-700 dark:text-blue-400 text-sm">
                                {sug.text || sug}
                              </span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                  {/* Cliffhanger Preview */}
                  {selectedEpisode.cliffhanger && (
                    <div className="mt-6 p-4 bg-gradient-to-r from-yellow-50 to-amber-50 dark:from-yellow-900/20 dark:to-amber-900/20 rounded-xl border border-yellow-200 dark:border-yellow-800">
                      <h3 className="text-sm font-semibold text-yellow-800 dark:text-yellow-300 mb-2 flex items-center">
                        <span className="mr-2">⚡</span>
                        Cliffhanger Ending
                      </h3>
                      <p className="text-yellow-700 dark:text-yellow-400 text-sm">
                        {selectedEpisode.cliffhanger}
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Custom scrollbar styles */}
      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #f1f1f1;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #cbd5e0;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #94a3b8;
        }
        .dark .custom-scrollbar::-webkit-scrollbar-track {
          background: #2d3748;
        }
        .dark .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #4a5568;
        }
        .dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #718096;
        }
      `}</style>
    </div>
  );
};

export default Episodes;
