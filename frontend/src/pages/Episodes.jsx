import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const Episodes = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [episodes, setEpisodes] = useState([]);
  const [selectedEpisode, setSelectedEpisode] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filmStrip, setFilmStrip] = useState([]);

  // Film strip effect
  useEffect(() => {
    const strips = [];
    for (let i = 0; i < 20; i++) {
      strips.push({
        id: i,
        top: Math.random() * 100,
        speed: 10 + Math.random() * 20,
        delay: Math.random() * 5,
      });
    }
    setFilmStrip(strips);
  }, []);

  const story = location.state?.story || "";
  const storyTitle = location.state?.storyTitle || "Your Story";
  const analysisData = location.state?.analysisData || null;

  useEffect(() => {
    const loadEpisodes = async () => {
      setLoading(true);
      try {
        if (analysisData && analysisData.episodes) {
          const formattedEpisodes = analysisData.episodes.map((ep, index) => {
            const epNum = ep.episode_number || index + 1;
            const description =
              ep.description ||
              ep.summary ||
              ep.content ||
              "No description available.";

            return {
              id: epNum,
              number: epNum,
              title: ep.title || `Episode ${epNum}`,
              description: description,
              summary: ep.summary || "",
              cliffhanger: ep.cliffhanger || "",
              cliffhanger_score: ep.cliffhanger_score || 0,
              retention_score: ep.retention_score || 0,
              twist_suggestions:
                analysisData.twists?.find((t) => t.episode === epNum)?.twists ||
                [],
            };
          });

          setEpisodes(formattedEpisodes);
          setSelectedEpisode(formattedEpisodes[0]);
        }
      } catch (error) {
        console.error("Error loading episodes:", error);
      } finally {
        setLoading(false);
      }
    };

    loadEpisodes();
  }, [analysisData]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 dark:from-black dark:via-purple-950 dark:to-black transition-colors duration-300 relative overflow-hidden">
      {/* Film Strip Background Animation */}
      <div className="fixed inset-0 pointer-events-none z-0">
        {filmStrip.map((strip) => (
          <div
            key={strip.id}
            className="absolute w-full h-0.5 bg-gradient-to-r from-transparent via-purple-500/20 to-transparent"
            style={{
              top: `${strip.top}%`,
              animation: `filmStrip ${strip.speed}s linear infinite`,
              animationDelay: `${strip.delay}s`,
            }}
          />
        ))}
      </div>

      {/* Floating Film Reels */}
      <div className="fixed inset-0 pointer-events-none z-0">
        {[...Array(6)].map((_, i) => (
          <div
            key={i}
            className="absolute text-8xl opacity-5 animate-float-reel"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${i * 2}s`,
              animationDuration: `${15 + i * 5}s`,
            }}
          >
            🎞️
          </div>
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header with film clapper animation */}
        <div className="flex items-center mb-6 animate-clapper">
          <button
            onClick={() => navigate(-1)}
            className="px-6 py-2 bg-white/10 backdrop-blur-md text-white rounded-lg font-semibold hover:bg-white/20 transform hover:scale-105 transition-all duration-300 border border-purple-500/30 hover:border-purple-500/50 flex items-center gap-2 group"
          >
            <span className="group-hover:-translate-x-1 transition-transform">
              ←
            </span>
            Back to Results
          </button>
          <h1 className="text-3xl font-bold ml-4 text-white flex items-center gap-3">
            <span className="text-4xl animate-spin-slow">🎬</span>
            Episode Guide
          </h1>
        </div>

        {/* Story Title with reel effect */}
        <div className="mb-6 text-purple-300 animate-reveal flex items-center gap-2">
          <span className="text-2xl">📽️</span>
          <span className="font-medium">Now Playing:</span> {storyTitle}
        </div>

        {/* Loading State with film reel spinner */}
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="relative">
              <div className="w-20 h-20 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-3xl animate-pulse">🎬</span>
              </div>
            </div>
          </div>
        ) : (
          <>
            {/* Episode count banner */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 mb-8 border border-purple-500/30 animate-slide-down">
              <div className="text-center">
                <span className="text-2xl font-bold text-white flex items-center justify-center gap-4">
                  <span className="text-3xl animate-bounce">🎬</span>
                  {episodes.length} Episodes in This Season
                  <span className="text-3xl animate-bounce animation-delay-200">
                    🎬
                  </span>
                </span>
              </div>
            </div>

            {/* Two Column Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column - Episode List */}
              <div className="lg:col-span-1">
                <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-purple-500/30 animate-slide-right">
                  <h2 className="text-xl font-bold text-white mb-4 px-2 flex items-center gap-2">
                    <span className="text-2xl">📋</span>
                    Episode List
                  </h2>
                  <div className="space-y-2 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                    {episodes.map((ep, index) => (
                      <button
                        key={ep.id}
                        onClick={() => setSelectedEpisode(ep)}
                        className={`w-full text-left p-4 rounded-xl transition-all duration-500 transform hover:scale-102
                                  ${
                                    selectedEpisode?.id === ep.id
                                      ? "bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-2xl scale-105 border-2 border-white"
                                      : "bg-white/5 text-gray-300 hover:bg-white/10 hover:scale-102 border border-purple-500/20"
                                  } animate-slide-up`}
                        style={{ animationDelay: `${index * 0.1}s` }}
                      >
                        <div className="font-bold flex items-center text-lg mb-1">
                          <span className="mr-2 text-2xl">▶️</span>
                          Episode {ep.number}
                        </div>
                        <div className="text-sm text-left mt-2 line-clamp-2 text-gray-400">
                          {ep.summary ||
                            ep.description.substring(0, 80) + "..."}
                        </div>
                        <div className="flex items-center gap-2 mt-3">
                          <span
                            className={`text-xs px-2 py-1 rounded-full ${
                              selectedEpisode?.id === ep.id
                                ? "bg-white/20 text-white"
                                : "bg-purple-900/30 text-purple-300"
                            }`}
                          >
                            ⚡ Cliffhanger:{" "}
                            {(ep.cliffhanger_score * 100).toFixed(0)}%
                          </span>
                          <span
                            className={`text-xs px-2 py-1 rounded-full ${
                              selectedEpisode?.id === ep.id
                                ? "bg-white/20 text-white"
                                : "bg-pink-900/30 text-pink-300"
                            }`}
                          >
                            📈 Retention:{" "}
                            {(ep.retention_score * 100).toFixed(0)}%
                          </span>
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Right Column - Selected Episode */}
              <div className="lg:col-span-2">
                {selectedEpisode && (
                  <div className="bg-white/10 backdrop-blur-md rounded-2xl p-6 border border-purple-500/30 animate-slide-left">
                    {/* Episode Header with film strip effect */}
                    <div className="relative overflow-hidden rounded-xl mb-6">
                      <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-pink-600/20 animate-pulse"></div>
                      <div className="relative p-6">
                        <h2 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
                          <span className="text-4xl">🎬</span>
                          {selectedEpisode.title}
                        </h2>
                        <p className="text-purple-300 flex items-center gap-2">
                          <span>Episode {selectedEpisode.number}</span>
                          <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                          <span>Season 1</span>
                        </p>
                      </div>
                    </div>

                    {/* Score Cards */}
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      <div className="bg-white/5 rounded-xl p-4 border border-purple-500/30 transform hover:scale-105 transition-transform duration-300">
                        <div className="text-2xl mb-2">⚡</div>
                        <div className="text-sm text-gray-400">
                          Cliffhanger Intensity
                        </div>
                        <div className="text-2xl font-bold text-purple-400">
                          {(selectedEpisode.cliffhanger_score * 100).toFixed(0)}
                          %
                        </div>
                      </div>
                      <div className="bg-white/5 rounded-xl p-4 border border-pink-500/30 transform hover:scale-105 transition-transform duration-300">
                        <div className="text-2xl mb-2">📈</div>
                        <div className="text-sm text-gray-400">
                          Retention Rate
                        </div>
                        <div className="text-2xl font-bold text-pink-400">
                          {(selectedEpisode.retention_score * 100).toFixed(0)}%
                        </div>
                      </div>
                    </div>

                    {/* Full Description with typewriter effect */}
                    <div className="bg-black/30 rounded-xl p-6 mb-6 border border-purple-500/30 animate-glow">
                      <h3 className="text-purple-400 font-semibold mb-3 flex items-center gap-2">
                        <span className="text-xl">📝</span>
                        Scene Details
                      </h3>
                      <p className="text-gray-300 leading-relaxed animate-typewriter">
                        {selectedEpisode.description}
                      </p>
                    </div>

                    {/* Cliffhanger with neon effect */}
                    {selectedEpisode.cliffhanger && (
                      <div className="bg-gradient-to-r from-purple-900/50 to-pink-900/50 rounded-xl p-6 mb-6 border-2 border-purple-500/50 animate-neon">
                        <h3 className="text-xl font-bold text-white mb-3 flex items-center gap-2">
                          <span className="text-2xl">⚡</span>
                          Cliffhanger Ending
                        </h3>
                        <p className="text-purple-200 text-lg italic">
                          "{selectedEpisode.cliffhanger}"
                        </p>
                      </div>
                    )}

                    {/* Plot Twists with star effect */}
                    {selectedEpisode.twist_suggestions?.length > 0 && (
                      <div className="bg-black/30 rounded-xl p-6 border border-yellow-500/30">
                        <h3 className="text-xl font-bold text-yellow-400 mb-4 flex items-center gap-2">
                          <span className="text-2xl animate-pulse">⭐</span>
                          Plot Twists
                        </h3>
                        <div className="space-y-3">
                          {selectedEpisode.twist_suggestions.map(
                            (twist, idx) => (
                              <div
                                key={idx}
                                className="p-4 bg-yellow-500/10 rounded-lg border border-yellow-500/20 transform hover:scale-105 hover:border-yellow-500/50 transition-all duration-300 animate-twist"
                                style={{ animationDelay: `${idx * 0.2}s` }}
                              >
                                <p className="text-yellow-300">
                                  {twist.text || twist}
                                </p>
                              </div>
                            ),
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </>
        )}
      </div>

      {/* Animation Keyframes */}
      <style>{`
        @keyframes filmStrip {
          0% { transform: translateX(-100%); opacity: 0; }
          10% { opacity: 0.5; }
          90% { opacity: 0.5; }
          100% { transform: translateX(100%); opacity: 0; }
        }

        @keyframes float-reel {
          0% { transform: translate(0, 0) rotate(0deg); opacity: 0.05; }
          25% { transform: translate(50px, -30px) rotate(90deg); opacity: 0.1; }
          50% { transform: translate(100px, 0) rotate(180deg); opacity: 0.05; }
          75% { transform: translate(50px, 30px) rotate(270deg); opacity: 0.1; }
          100% { transform: translate(0, 0) rotate(360deg); opacity: 0.05; }
        }

        @keyframes clapper {
          0% { transform: rotate(-5deg) scale(0.95); opacity: 0; }
          50% { transform: rotate(5deg) scale(1.05); }
          100% { transform: rotate(0) scale(1); opacity: 1; }
        }

        @keyframes reveal {
          from { clip-path: inset(0 100% 0 0); }
          to { clip-path: inset(0 0 0 0); }
        }

        @keyframes glow {
          0%, 100% { box-shadow: 0 0 20px rgba(168, 85, 247, 0.3); }
          50% { box-shadow: 0 0 40px rgba(168, 85, 247, 0.6); }
        }

        @keyframes neon {
          0%, 100% { border-color: rgba(168, 85, 247, 0.5); box-shadow: 0 0 20px rgba(168, 85, 247, 0.3); }
          50% { border-color: rgba(236, 72, 153, 0.8); box-shadow: 0 0 40px rgba(236, 72, 153, 0.6); }
        }

        @keyframes twist {
          0% { transform: scale(0.95); opacity: 0; }
          50% { transform: scale(1.05); }
          100% { transform: scale(1); opacity: 1; }
        }

        @keyframes slide-right {
          from { transform: translateX(-50px); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }

        @keyframes slide-left {
          from { transform: translateX(50px); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }

        .animate-float-reel {
          animation: float-reel linear infinite;
        }

        .animate-clapper {
          animation: clapper 0.8s ease-out forwards;
        }

        .animate-reveal {
          animation: reveal 1s ease-out forwards;
        }

        .animate-glow {
          animation: glow 3s ease-in-out infinite;
        }

        .animate-neon {
          animation: neon 2s ease-in-out infinite;
        }

        .animate-twist {
          animation: twist 0.5s ease-out forwards;
        }

        .animate-slide-right {
          animation: slide-right 0.6s ease-out forwards;
        }

        .animate-slide-left {
          animation: slide-left 0.6s ease-out forwards;
        }

        .animate-slide-down {
          animation: slide-down 0.6s ease-out forwards;
        }

        @keyframes slide-down {
          from { transform: translateY(-30px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }

        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(255,255,255,0.1);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(168, 85, 247, 0.5);
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(168, 85, 247, 0.8);
        }
      `}</style>
    </div>
  );
};

export default Episodes;
