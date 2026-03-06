import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTheme } from '../context/ThemeContext'

const Home = () => {
  const [story, setStory] = useState('')
  const [snowflakes, setSnowflakes] = useState([])
  const [isSnowEnabled, setIsSnowEnabled] = useState(true)
  const navigate = useNavigate()
  const { isDark } = useTheme()

  // Emotion emojis array for light mode
  const emotionEmojis = ['😊', '😢', '😠', '😨', '😲', '🥰', '🤔', '😌', '🥺', '😤', '🤯', '🥳'];

  // Continuous emoji/snow effect
  useEffect(() => {
    if (!isSnowEnabled) return;

    const createSnowflake = () => {
      const useEmoji = Math.random() < 0.15;
      const randomEmoji = emotionEmojis[Math.floor(Math.random() * emotionEmojis.length)];
      
      const snowflake = {
        id: Math.random(),
        left: Math.random() * 100, // Random position across full width
        animationDuration: 5 + Math.random() * 8,
        opacity: useEmoji ? 0.7 + Math.random() * 0.3 : 0.1 + Math.random() * 0.2,
        size: useEmoji ? 14 + Math.random() * 10 : 2 + Math.random() * 4,
        isEmoji: useEmoji,
        emojiChar: randomEmoji
      };
      
      setSnowflakes(prev => [...prev, snowflake]);
      
      // Remove after animation completes
      setTimeout(() => {
        setSnowflakes(prev => prev.filter(s => s.id !== snowflake.id));
      }, snowflake.animationDuration * 1000);
    };

    // Create initial batch for instant effect
    for (let i = 0; i < 30; i++) {
      setTimeout(() => {
        createSnowflake();
      }, i * 50);
    }

    // CONTINUOUS CREATION - creates new ones every 300ms
    const interval = setInterval(createSnowflake, 300);
    return () => clearInterval(interval);
  }, [isSnowEnabled, isDark]);

  const handleGenerateEpisodes = () => {
    if (story.trim().length < 10) {
      alert('Please write a story first (at least 10 characters)')
      return
    }
    navigate('/episodes', { state: { story } })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300 relative overflow-hidden">
      
      {/* Snowfall Toggle Button */}
      <button
        onClick={() => setIsSnowEnabled(!isSnowEnabled)}
        className="fixed top-20 right-4 z-50 p-3 bg-white dark:bg-gray-800 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-110"
        title={isSnowEnabled ? "Turn off effects" : "Turn on effects"}
      >
        {isSnowEnabled ? (isDark ? '❄️' : '😊') : '☀️'}
      </button>

      {/* Floating Emojis/Snow Effect - FULL SCREEN */}
      {isSnowEnabled && (
        <div className="fixed inset-0 pointer-events-none z-10 w-full h-full">
          {snowflakes.map(flake => (
            <div
              key={flake.id}
              className="absolute animate-snowfall"
              style={{
                left: `${flake.left}%`,
                top: '-10%',
                fontSize: flake.isEmoji ? `${flake.size}px` : '0',
                width: !flake.isEmoji ? `${flake.size}px` : 'auto',
                height: !flake.isEmoji ? `${flake.size}px` : 'auto',
                opacity: flake.opacity,
                animationDuration: `${flake.animationDuration}s`,
                backgroundColor: !flake.isEmoji ? (isDark ? '#e5e7eb' : '#ffffff') : 'transparent',
                borderRadius: !flake.isEmoji ? '50%' : '0',
              }}
            >
              {flake.isEmoji && (isDark ? '❄️' : flake.emojiChar)}
            </div>
          ))}
        </div>
      )}

      {/* Main Content - This does NOT affect emoji positioning */}
      <div className="relative z-20 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        
        {/* Hero Section */}
        <div className="text-center mb-12 animate-fade-in">
          <div className="flex justify-center space-x-4 text-6xl mb-6">
            {['📚', '✨', '🎭', '✍️'].map((emoji, i) => (
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
            Paste your story and get AI-powered insights about{' '}
            <span className="text-blue-600 dark:text-blue-400 font-semibold px-2 py-1 bg-blue-50 dark:bg-blue-900/30 rounded-lg">emotions</span>,{' '}
            <span className="text-purple-600 dark:text-purple-400 font-semibold px-2 py-1 bg-purple-50 dark:bg-purple-900/30 rounded-lg">cliffhangers</span>,{' '}
            and{' '}
            <span className="text-pink-600 dark:text-pink-400 font-semibold px-2 py-1 bg-pink-50 dark:bg-pink-900/30 rounded-lg">retention</span>
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {[
            { emoji: '📊', title: 'Emotion Analysis', desc: 'Track 5 emotions throughout', color: 'from-blue-400 to-blue-600' },
            { emoji: '🎯', title: 'Cliffhanger Score', desc: 'Measure suspense levels', color: 'from-purple-400 to-purple-600' },
            { emoji: '💡', title: 'Smart Suggestions', desc: 'Get improvement tips', color: 'from-pink-400 to-pink-600' }
          ].map((card, i) => (
            <div
              key={i}
              className="group relative animate-slide-up"
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              <div className={`absolute inset-0 bg-gradient-to-r ${card.color} opacity-0 group-hover:opacity-10 dark:group-hover:opacity-20 rounded-2xl transition-opacity duration-500`} />
              <div className="relative bg-white dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-2xl p-6 transform transition-all duration-300 hover:-translate-y-2 border border-gray-100 dark:border-gray-700">
                <div className="text-5xl mb-4 group-hover:scale-110 group-hover:rotate-12 transition-transform duration-300">
                  {card.emoji}
                </div>
                <h3 className="text-xl font-bold text-gray-800 dark:text-white mb-2">{card.title}</h3>
                <p className="text-gray-600 dark:text-gray-300">{card.desc}</p>
                <div className={`absolute bottom-0 left-0 h-1 w-0 group-hover:w-full bg-gradient-to-r ${card.color} transition-all duration-500 rounded-b-2xl`} />
              </div>
            </div>
          ))}
        </div>

        {/* Story Input Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-6 sm:p-8 mb-12 border border-gray-100 dark:border-gray-700 transform transition-all duration-300 hover:shadow-2xl">
          <h2 className="text-2xl font-semibold text-gray-800 dark:text-white mb-4 flex items-center">
            <span className="bg-blue-100 dark:bg-blue-900/50 p-2 rounded-lg mr-3 animate-pulse-slow">📝</span>
            Your Story
          </h2>
          
          <textarea
            className="w-full h-48 sm:h-64 p-4 border-2 border-gray-200 dark:border-gray-700 rounded-xl 
                     focus:border-blue-500 dark:focus:border-blue-400 focus:ring-4 focus:ring-blue-100 dark:focus:ring-blue-900/30 
                     outline-none transition-all resize-none text-gray-700 dark:text-gray-300
                     placeholder-gray-400 dark:placeholder-gray-500 bg-gray-50 dark:bg-gray-900"
            placeholder="Once upon a time..."
            value={story}
            onChange={(e) => setStory(e.target.value)}
          />

          {/* Character and Word Counter */}
          <div className="flex space-x-4 text-sm mt-4">
            <span className="bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full text-gray-600 dark:text-gray-300">
              📝 {story.length} characters
            </span>
            <span className="bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded-full text-gray-600 dark:text-gray-300">
              📊 {story.split(' ').filter(w => w).length} words
            </span>
          </div>

          {/* Generate Episodes Button */}
          <div className="flex justify-center mt-6">
            <button
              onClick={handleGenerateEpisodes}
              className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl font-semibold text-lg hover:from-purple-700 hover:to-pink-700 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl flex items-center justify-center gap-2 min-w-[250px]"
            >
              <span>📺</span>
              Generate Episodes
              <span>✨</span>
            </button>
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
                emoji: '🌄',
                title: 'Mystery Story',
                desc: 'Secrets and revelations',
                story: 'In a small village nestled between misty mountains, an old clock tower held secrets that no one dared to uncover. Until one stormy night, when lightning struck and everything changed...'
              },
              {
                emoji: '❤️',
                title: 'Love Story',
                desc: 'Heartwarming romance',
                story: 'Sarah never believed in love at first sight until she walked into the old bookstore and saw him reading her favorite novel. Their eyes met, and time stood still as they discovered their shared love for stories.'
              },
              {
                emoji: '🚀',
                title: 'Sci-Fi',
                desc: 'Intergalactic adventure',
                story: "Captain Ray's ship was caught in a cosmic storm when an alien vessel emerged from the vortex. First contact was about to begin, and humanity wasn't ready for what the stars had brought."
              }
            ].map((example, i) => (
              <button
                key={i}
                onClick={() => {
                  setStory(example.story);
                  const textarea = document.querySelector('textarea');
                  if (textarea) textarea.focus();
                }}
                className="group bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md hover:shadow-2xl transition-all duration-300 text-left border border-gray-100 dark:border-gray-700 transform hover:-translate-y-2"
              >
                <span className="text-4xl block mb-3 group-hover:scale-110 group-hover:rotate-12 transition-transform duration-300">
                  {example.emoji}
                </span>
                <h3 className="font-semibold text-gray-800 dark:text-white mb-1">{example.title}</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">{example.desc}</p>
                <span className="text-blue-600 dark:text-blue-400 text-sm font-medium group-hover:underline">
                  Click to use →
                </span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home