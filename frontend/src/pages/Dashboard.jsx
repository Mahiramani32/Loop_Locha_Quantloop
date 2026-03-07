import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [floatingBooks, setFloatingBooks] = useState([]);

  // Load stories from localStorage
  useEffect(() => {
    loadStories();
    createFloatingBooks();
  }, []);

  const createFloatingBooks = () => {
    const books = [];
    const bookEmojis = ["📚", "📖", "📕", "📗", "📘", "📙", "📓", "📔"];
    for (let i = 0; i < 15; i++) {
      books.push({
        id: i,
        emoji: bookEmojis[Math.floor(Math.random() * bookEmojis.length)],
        left: Math.random() * 100,
        top: Math.random() * 100,
        size: 20 + Math.random() * 40,
        duration: 15 + Math.random() * 20,
        delay: Math.random() * 5,
        rotate: Math.random() * 360,
      });
    }
    setFloatingBooks(books);
  };

  const loadStories = () => {
    setLoading(true);
    try {
      const savedStories = JSON.parse(localStorage.getItem("stories") || "[]");
      setStories(savedStories);
    } catch (error) {
      console.error("Error loading stories:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteStory = (e, storyId) => {
    e.stopPropagation();
    if (window.confirm("Are you sure you want to delete this story?")) {
      const savedStories = JSON.parse(localStorage.getItem("stories") || "[]");
      const updatedStories = savedStories.filter((s) => s.id !== storyId);
      localStorage.setItem("stories", JSON.stringify(updatedStories));
      loadStories();
    }
  };

  const handleStoryClick = (story) => {
    navigate("/episodes", {
      state: {
        story: story.fullStory,
        storyTitle: story.title,
        storyId: story.id,
        analysisData: story.analysisData,
      },
    });
  };

  const getScoreColor = (score) => {
    if (score >= 90) return "text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30";
    if (score >= 70) return "text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/30";
    return "text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30";
  };

  const filteredStories = stories.filter((story) =>
    story.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const totalStories = stories.length;
  const avgScore = totalStories > 0
    ? Math.round(stories.reduce((acc, s) => acc + s.score, 0) / totalStories)
    : 0;
  const bestStory = stories.reduce(
    (best, current) => (current.score > (best?.score || 0) ? current : best),
    null
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 dark:from-gray-900 dark:via-indigo-950 dark:to-purple-950 transition-colors duration-300 relative overflow-hidden">
      {/* Floating Books Animation */}
      <div className="fixed inset-0 pointer-events-none z-0">
        {floatingBooks.map((book) => (
          <div
            key={book.id}
            className="absolute animate-float-book"
            style={{
              left: `${book.left}%`,
              top: `${book.top}%`,
              fontSize: `${book.size}px`,
              opacity: 0.15,
              transform: `rotate(${book.rotate}deg)`,
              animation: `floatBook ${book.duration}s linear infinite`,
              animationDelay: `${book.delay}s`,
            }}
          >
            {book.emoji}
          </div>
        ))}
      </div>

      {/* Floating Particles Effect */}
      <div className="fixed inset-0 pointer-events-none z-0">
        {[...Array(30)].map((_, i) => (
          <div
            key={i}
            className="absolute rounded-full bg-amber-400 dark:bg-purple-400"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              width: `${2 + Math.random() * 4}px`,
              height: `${2 + Math.random() * 4}px`,
              opacity: 0.2,
              animation: `floatParticle ${10 + Math.random() * 20}s linear infinite`,
              animationDelay: `${Math.random() * 5}s`,
            }}
          />
        ))}
      </div>

      {/* Main Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header with animation */}
        <div className="flex flex-col sm:flex-row justify-between items-center mb-8 animate-slide-down">
          <h1 className="text-4xl sm:text-5xl font-bold mb-4 sm:mb-0 bg-gradient-to-r from-amber-600 to-orange-600 dark:from-purple-400 dark:to-pink-400 text-transparent bg-clip-text animate-pulse-slow">
            Your Story Library 📚
          </h1>

          <button
            onClick={() => navigate("/")}
            className="px-6 py-3 bg-gradient-to-r from-amber-500 to-orange-500 dark:from-purple-600 dark:to-pink-600 text-white rounded-xl font-semibold hover:from-amber-600 hover:to-orange-600 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl flex items-center gap-2 animate-bounce-subtle"
          >
            <span className="text-xl">➕</span>
            Write New Story
          </button>
        </div>

        {/* Search Bar with glow effect */}
        <div className="mb-8 animate-slide-up">
          <div className="relative group">
            <span className="absolute left-4 top-1/2 transform -translate-y-1/2 text-amber-500 dark:text-purple-400 text-xl group-hover:scale-110 transition-transform duration-300">
              🔍
            </span>
            <input
              type="text"
              placeholder="Search your stories..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-14 pr-4 py-4 rounded-2xl border-2 border-amber-200 dark:border-purple-800 
                       bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm text-gray-800 dark:text-white
                       focus:border-amber-500 dark:focus:border-purple-400 focus:ring-4 focus:ring-amber-200 dark:focus:ring-purple-900/30 
                       outline-none transition-all shadow-lg group-hover:shadow-2xl"
            />
          </div>
        </div>

        {/* Stats Cards with animations */}
        {!loading && totalStories > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl shadow-xl p-6 transform transition-all duration-500 hover:scale-105 hover:rotate-1 hover:shadow-2xl border border-amber-200 dark:border-purple-800 animate-float-card">
              <div className="text-5xl mb-3 animate-bounce-slow text-amber-600 dark:text-purple-400">📚</div>
              <h3 className="text-amber-700 dark:text-purple-300 text-sm font-semibold">Total Stories</h3>
              <p className="text-4xl font-bold text-gray-800 dark:text-white">{totalStories}</p>
            </div>
            
            <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl shadow-xl p-6 transform transition-all duration-500 hover:scale-105 hover:rotate-1 hover:shadow-2xl border border-amber-200 dark:border-purple-800 animate-float-card" style={{ animationDelay: "0.2s" }}>
              <div className="text-5xl mb-3 animate-bounce-slow text-amber-600 dark:text-purple-400">📊</div>
              <h3 className="text-amber-700 dark:text-purple-300 text-sm font-semibold">Average Score</h3>
              <p className="text-4xl font-bold text-green-600 dark:text-green-400">{avgScore}%</p>
            </div>
            
            <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl shadow-xl p-6 transform transition-all duration-500 hover:scale-105 hover:rotate-1 hover:shadow-2xl border border-amber-200 dark:border-purple-800 animate-float-card" style={{ animationDelay: "0.4s" }}>
              <div className="text-5xl mb-3 animate-bounce-slow text-amber-600 dark:text-purple-400">🏆</div>
              <h3 className="text-amber-700 dark:text-purple-300 text-sm font-semibold">Best Story</h3>
              <p className="text-lg font-bold text-purple-600 dark:text-purple-400">{bestStory?.title || "N/A"}</p>
              {bestStory && <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{bestStory.score}% score</p>}
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-20">
            <div className="relative">
              <div className="w-16 h-16 border-4 border-amber-300 dark:border-purple-300 border-t-amber-600 dark:border-t-purple-600 rounded-full animate-spin"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-2xl animate-pulse">📖</span>
              </div>
            </div>
          </div>
        )}

        {/* Stories Grid */}
        {!loading && (
          <div>
            <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6 flex items-center gap-2">
              <span className="text-3xl animate-wiggle">📖</span>
              Your Stories
            </h2>
            
            {filteredStories.length === 0 ? (
              <div className="text-center py-20 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-2xl shadow-xl border border-amber-200 dark:border-purple-800">
                <div className="text-7xl mb-4 animate-float">📚</div>
                <p className="text-gray-600 dark:text-gray-400 text-xl mb-4">No stories yet...</p>
                <button
                  onClick={() => navigate("/")}
                  className="px-8 py-4 bg-gradient-to-r from-amber-500 to-orange-500 dark:from-purple-600 dark:to-pink-600 text-white rounded-xl font-semibold hover:from-amber-600 hover:to-orange-600 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
                >
                  Write Your First Story ✨
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredStories.map((story, index) => (
                  <div
                    key={story.id}
                    onClick={() => handleStoryClick(story)}
                    className="group bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl shadow-xl p-6 
                             cursor-pointer transform transition-all duration-500 hover:-translate-y-2 hover:shadow-2xl 
                             border border-amber-200 dark:border-purple-800 animate-card-pop"
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    <div className="flex justify-between items-start mb-4">
                      <span className="text-4xl group-hover:scale-110 group-hover:rotate-12 transition-transform duration-300">
                        {index % 3 === 0 ? "📕" : index % 3 === 1 ? "📗" : "📙"}
                      </span>
                      <button
                        onClick={(e) => handleDeleteStory(e, story.id)}
                        className="p-2 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-200 dark:hover:bg-red-900/50 transition-all duration-300 transform hover:scale-110 hover:rotate-90"
                      >
                        🗑️
                      </button>
                    </div>

                    <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-2 group-hover:text-amber-600 dark:group-hover:text-purple-400 transition-colors">
                      {story.title}
                    </h3>
                    
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-2">
                      {story.preview}
                    </p>

                    <div className="flex justify-between items-center">
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getScoreColor(story.score)}`}>
                        {story.score}% Score
                      </span>
                      
                      <span className="text-amber-600 dark:text-purple-400 text-sm font-medium flex items-center gap-1 group-hover:translate-x-2 transition-transform duration-300">
                        Read More
                        <span className="text-lg">→</span>
                      </span>
                    </div>

                    <div className="mt-3 text-xs text-gray-400 dark:text-gray-500">
                      {story.date}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Animation Keyframes */}
      <style>{`
        @keyframes floatBook {
          0% { transform: translateY(0) rotate(0deg); opacity: 0.1; }
          25% { transform: translateY(-20px) rotate(5deg); opacity: 0.2; }
          50% { transform: translateY(0) rotate(0deg); opacity: 0.1; }
          75% { transform: translateY(20px) rotate(-5deg); opacity: 0.2; }
          100% { transform: translateY(0) rotate(0deg); opacity: 0.1; }
        }

        @keyframes floatParticle {
          0% { transform: translateY(0) translateX(0); opacity: 0.2; }
          25% { transform: translateY(-30px) translateX(15px); opacity: 0.3; }
          50% { transform: translateY(0) translateX(30px); opacity: 0.2; }
          75% { transform: translateY(30px) translateX(15px); opacity: 0.3; }
          100% { transform: translateY(0) translateX(0); opacity: 0.2; }
        }

        @keyframes slide-down {
          from { transform: translateY(-50px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }

        @keyframes slide-up {
          from { transform: translateY(50px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }

        @keyframes card-pop {
          0% { transform: scale(0.9); opacity: 0; }
          50% { transform: scale(1.02); }
          100% { transform: scale(1); opacity: 1; }
        }

        @keyframes wiggle {
          0%, 100% { transform: rotate(0deg); }
          25% { transform: rotate(-10deg); }
          75% { transform: rotate(10deg); }
        }

        .animate-slide-down {
          animation: slide-down 0.8s ease-out forwards;
        }

        .animate-slide-up {
          animation: slide-up 0.8s ease-out forwards;
        }

        .animate-card-pop {
          animation: card-pop 0.5s ease-out forwards;
        }

        .animate-wiggle {
          animation: wiggle 1s ease-in-out infinite;
        }

        .animate-float-card {
          animation: floatBook 6s ease-in-out infinite;
        }

        .animate-bounce-subtle {
          animation: bounce 2s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
};

export default Dashboard;