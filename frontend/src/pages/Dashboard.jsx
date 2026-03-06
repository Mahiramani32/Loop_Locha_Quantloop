import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState("");
  const [stories, setStories] = useState([]);

  // Load stories from localStorage
  useEffect(() => {
    loadStories();
  }, []);

  const loadStories = () => {
    const savedStories = JSON.parse(localStorage.getItem("stories") || "[]");
    setStories(
      savedStories.length
        ? savedStories
        : [
            {
              id: 1,
              title: "Echoes from the Nebula",
              date: "2024-03-15",
              score: 95,
              preview: "In the depths of space, a mysterious signal...",
              fullStory:
                "In the depths of space, a mysterious signal was detected...",
            },
            {
              id: 2,
              title: "The Last Lighthouse",
              date: "2024-03-14",
              score: 82,
              preview: "On a rocky shore, the old lighthouse keeper...",
              fullStory:
                "On a rocky shore, the old lighthouse keeper spent his days watching the waves...",
            },
            {
              id: 3,
              title: "Whispers in the Wind",
              date: "2024-03-13",
              score: 78,
              preview: "The wind carried secrets through the valley...",
              fullStory:
                "The wind carried secrets through the valley, whispering tales of old...",
            },
            {
              id: 4,
              title: "Digital Dreams",
              date: "2024-03-12",
              score: 88,
              preview: "In a world of virtual reality, one programmer...",
              fullStory:
                "In a world of virtual reality, one programmer discovered something unexpected...",
            },
            {
              id: 5,
              title: "The Forgotten Temple",
              date: "2024-03-11",
              score: 91,
              preview: "Deep in the jungle, an ancient temple held...",
              fullStory:
                "Deep in the jungle, an ancient temple held secrets that could change history...",
            },
            {
              id: 6,
              title: "Midnight Melody",
              date: "2024-03-10",
              score: 85,
              preview: "Every night at midnight, a mysterious piano...",
              fullStory:
                "Every night at midnight, a mysterious piano played music that haunted the town...",
            },
          ],
    );
  };

  // Delete story function
  const handleDeleteStory = (e, storyId) => {
    e.stopPropagation(); // Prevent clicking on the story card

    if (window.confirm("Are you sure you want to delete this story?")) {
      const savedStories = JSON.parse(localStorage.getItem("stories") || "[]");
      const updatedStories = savedStories.filter((s) => s.id !== storyId);
      localStorage.setItem("stories", JSON.stringify(updatedStories));
      loadStories(); // Reload stories after deletion
    }
  };

  // Handle story click - Navigate to Episodes page
  const handleStoryClick = (story) => {
    navigate("/episodes", {
      state: {
        story: story.fullStory || story.preview,
        storyTitle: story.title,
        storyId: story.id,
      },
    });
  };

  const getScoreColor = (score) => {
    if (score >= 90)
      return "text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/30";
    if (score >= 70)
      return "text-yellow-600 dark:text-yellow-400 bg-yellow-100 dark:bg-yellow-900/30";
    return "text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30";
  };

  const filteredStories = stories.filter((story) =>
    story.title.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  // Calculate stats
  const totalStories = stories.length;
  const avgScore =
    Math.round(stories.reduce((acc, s) => acc + s.score, 0) / stories.length) ||
    0;
  const bestStory = stories.reduce(
    (best, current) => (current.score > (best?.score || 0) ? current : best),
    null,
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300">
      {/* Floating Emojis Background */}
      <div className="fixed inset-0 pointer-events-none opacity-10 dark:opacity-20">
        {["📊", "📈", "📉", "🎯", "💡"].map((emoji, i) => (
          <span
            key={i}
            className="absolute text-8xl animate-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${i * 0.5}s`,
            }}
          >
            {emoji}
          </span>
        ))}
      </div>

      {/* Main Content */}
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-center mb-8 animate-fade-in">
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-800 dark:text-white mb-4 sm:mb-0">
            Your Story Dashboard 📊
          </h1>

          {/* New Story Button */}
          <button
            onClick={() => navigate("/")}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl flex items-center gap-2"
          >
            <span>➕</span>
            New Story
          </button>
        </div>

        {/* Search Bar */}
        <div className="mb-8 animate-slide-up">
          <div className="relative">
            <span className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400">
              🔍
            </span>
            <input
              type="text"
              placeholder="Search your stories..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-3 rounded-xl border-2 border-gray-200 dark:border-gray-700 
                       bg-white dark:bg-gray-800 text-gray-800 dark:text-white
                       focus:border-blue-500 dark:focus:border-blue-400 focus:ring-4 focus:ring-blue-100 dark:focus:ring-blue-900/30 
                       outline-none transition-all"
            />
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 transform transition-all duration-300 hover:scale-105 hover:shadow-2xl border border-gray-100 dark:border-gray-700">
            <div className="text-4xl mb-3 animate-bounce-slow">📚</div>
            <h3 className="text-gray-600 dark:text-gray-400 text-sm">
              Total Stories
            </h3>
            <p className="text-3xl font-bold text-gray-800 dark:text-white">
              {totalStories}
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 transform transition-all duration-300 hover:scale-105 hover:shadow-2xl border border-gray-100 dark:border-gray-700">
            <div className="text-4xl mb-3 animate-bounce-slow animation-delay-200">
              📊
            </div>
            <h3 className="text-gray-600 dark:text-gray-400 text-sm">
              Average Score
            </h3>
            <p className="text-3xl font-bold text-green-600 dark:text-green-400">
              {avgScore}%
            </p>
          </div>
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 transform transition-all duration-300 hover:scale-105 hover:shadow-2xl border border-gray-100 dark:border-gray-700">
            <div className="text-4xl mb-3 animate-bounce-slow animation-delay-400">
              🏆
            </div>
            <h3 className="text-gray-600 dark:text-gray-400 text-sm">
              Best Story
            </h3>
            <p className="text-lg font-bold text-purple-600 dark:text-purple-400">
              {bestStory?.title || "N/A"}
            </p>
            {bestStory && (
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                {bestStory.score}% score
              </p>
            )}
          </div>
        </div>

        {/* Recent Stories - Click to go to Episodes */}
        <div>
          <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">
            Recent Stories
          </h2>
          <div className="space-y-4">
            {filteredStories.map((story, index) => (
              <div
                key={story.id}
                onClick={() => handleStoryClick(story)}
                className="group bg-white dark:bg-gray-800 rounded-xl shadow-md hover:shadow-2xl p-6 
                         cursor-pointer transform transition-all duration-300 hover:-translate-y-1 
                         border border-gray-100 dark:border-gray-700 animate-slide-up relative"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                      {story.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-2">
                      {story.preview}
                    </p>
                    <p className="text-gray-400 dark:text-gray-500 text-xs">
                      {story.date}
                    </p>
                  </div>
                  <div className="flex items-center space-x-4">
                    <span
                      className={`px-4 py-2 rounded-full text-sm font-semibold ${getScoreColor(story.score)}`}
                    >
                      {story.score}%
                    </span>

                    {/* Delete Button */}
                    <button
                      onClick={(e) => handleDeleteStory(e, story.id)}
                      className="p-2 bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-200 dark:hover:bg-red-900/50 transition-all duration-300 transform hover:scale-110"
                      title="Delete story"
                    >
                      🗑️
                    </button>

                    {/* Episode indicator */}
                    <span className="text-purple-600 dark:text-purple-400 text-sm font-medium flex items-center gap-1">
                      <span>📺</span>
                      View Episodes
                    </span>

                    <span className="text-gray-400 group-hover:translate-x-2 transition-transform duration-300">
                      →
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
