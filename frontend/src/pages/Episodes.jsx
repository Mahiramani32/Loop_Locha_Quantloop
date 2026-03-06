// import { useState, useEffect } from 'react'
// import { useLocation, useNavigate } from 'react-router-dom'
// import Button from '../components/common/Button'

// const Episodes = () => {
//   const location = useLocation()
//   const navigate = useNavigate()
//   const [episodes, setEpisodes] = useState([])
//   const [genre, setGenre] = useState('Thriller')
//   const [tone, setTone] = useState('Suspenseful')
//   const [selectedEpisode, setSelectedEpisode] = useState(null)
//   const [loading, setLoading] = useState(false)

//   // Get story data from location or localStorage
//   const story = location.state?.story || JSON.parse(localStorage.getItem('currentStory') || 'null')

//   // Mock data - will be replaced with actual backend data
//   useEffect(() => {
//     const fetchEpisodes = async () => {
//       setLoading(true)
//       try {
//         await new Promise(resolve => setTimeout(resolve, 1000))
        
//         // Mock data - backend will send actual episodes (any number)
//         const mockEpisodes = [
//           { id: 1, title: "The Mysterious Beginning", description: "A stranger arrives in a small town, bringing secrets that will change everything." },
//           { id: 2, title: "The Secret Ingredient", description: "Dark secrets are revealed as the protagonist digs deeper into the mystery." },
//           { id: 3, title: "Shadows of the Past", description: "The protagonist discovers a hidden truth about their family history." },
//           { id: 4, title: "Twist in the Tale", description: "Nothing is what it seems as a major plot twist changes everything." },
//           { id: 5, title: "Racing Against Time", description: "The clock is ticking as the antagonist makes their final move." },
//           { id: 6, title: "The Final Revelation", description: "All secrets are unveiled in a shocking confrontation." },
//           { id: 7, title: "Endgame", description: "The thrilling conclusion where everything comes together." },
//         ]
        
//         setEpisodes(mockEpisodes)
//         setSelectedEpisode(mockEpisodes[1])
//       } catch (error) {
//         console.error('Error fetching episodes:', error)
//       } finally {
//         setLoading(false)
//       }
//     }

//     fetchEpisodes()
//   }, [genre, tone])

//   const genres = ['Thriller', 'Mystery', 'Romance', 'Sci-Fi', 'Fantasy', 'Horror', 'Drama', 'Comedy']
//   const tones = ['Suspenseful', 'Dark', 'Light-hearted', 'Mysterious', 'Action-packed', 'Emotional', 'Humorous', 'Serious']

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300 relative overflow-hidden">
      
//       {/* Floating Emojis Background (matches Home page) */}
//       <div className="fixed inset-0 pointer-events-none opacity-10 dark:opacity-20">
//         {['📺', '🎬', '📽️', '🎭', '📝', '✨'].map((emoji, i) => (
//           <span
//             key={i}
//             className="absolute text-8xl animate-float"
//             style={{
//               left: `${Math.random() * 100}%`,
//               top: `${Math.random() * 100}%`,
//               animationDelay: `${i * 0.5}s`,
//               animationDuration: `${3 + i}s`
//             }}
//           >
//             {emoji}
//           </span>
//         ))}
//       </div>

//       {/* Main Content */}
//       <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
//         {/* Header with Back Button */}
//         <div className="flex items-center mb-6 animate-fade-in">
//           <Button 
//             onClick={() => navigate(-1)}
//             variant="secondary"
//             size="small"
//           >
//             ← Back
//           </Button>
//           <h1 className="text-3xl font-bold text-gray-800 dark:text-white ml-4">
//             Story Episodes
//           </h1>
//         </div>

//         {/* Story Preview Card (matches Home page style) */}
//         {story && (
//           <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 mb-6 border border-gray-100 dark:border-gray-700 animate-slide-up">
//             <p className="text-gray-600 dark:text-gray-300 text-sm line-clamp-2">
//               <span className="text-blue-600 dark:text-blue-400 mr-2">📖</span>
//               {typeof story === 'string' ? story.substring(0, 150) + '...' : 'Your story'}
//             </p>
//           </div>
//         )}

//         {/* Controls Row - matches Home page card style */}
//         <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 mb-8 border border-gray-100 dark:border-gray-700 transform transition-all duration-300 hover:shadow-2xl animate-slide-up">
//           <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            
//             {/* Genre Dropdown */}
//             <div>
//               <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
//                 Genre
//               </label>
//               <select 
//                 value={genre}
//                 onChange={(e) => setGenre(e.target.value)}
//                 className="w-full p-3 rounded-lg border-2 border-gray-200 dark:border-gray-700 
//                          bg-white dark:bg-gray-900 text-gray-800 dark:text-white
//                          focus:border-blue-500 dark:focus:border-blue-400 focus:ring-4 focus:ring-blue-100 dark:focus:ring-blue-900/30 
//                          outline-none transition-all"
//               >
//                 {genres.map(g => (
//                   <option key={g} value={g}>{g}</option>
//                 ))}
//               </select>
//             </div>

//             {/* Episodes Info */}
//             <div>
//               <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
//                 Episodes
//               </label>
//               <div className="p-3 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800 rounded-lg text-gray-800 dark:text-white font-semibold border-2 border-gray-200 dark:border-gray-700">
//                 {loading ? 'Loading...' : `${episodes.length} Episodes`}
//               </div>
//             </div>

//             {/* Tone Dropdown */}
//             <div>
//               <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
//                 Tone
//               </label>
//               <select 
//                 value={tone}
//                 onChange={(e) => setTone(e.target.value)}
//                 className="w-full p-3 rounded-lg border-2 border-gray-200 dark:border-gray-700 
//                          bg-white dark:bg-gray-900 text-gray-800 dark:text-white
//                          focus:border-blue-500 dark:focus:border-blue-400 focus:ring-4 focus:ring-blue-100 dark:focus:ring-blue-900/30 
//                          outline-none transition-all"
//               >
//                 {tones.map(t => (
//                   <option key={t} value={t}>{t}</option>
//                 ))}
//               </select>
//             </div>

//             {/* Generate Button - matches Home page button style */}
//             <div>
//               <button
//                 onClick={() => alert('Generate new story arc - Backend integration pending')}
//                 className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
//               >
//                 Generate Story Arc <span className="ml-2">✨</span>
//               </button>
//             </div>
//           </div>
//         </div>

//         {/* Loading State */}
//         {loading ? (
//           <div className="flex justify-center items-center py-20">
//             <div className="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
//           </div>
//         ) : (
//           /* Two Column Layout - Episodes List + Selected Episode Detail */
//           <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
//             {/* Episodes List - Left Column (1/3 width) */}
//             <div className="lg:col-span-1">
//               <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-4 border border-gray-100 dark:border-gray-700">
//                 <h2 className="text-lg font-semibold text-gray-800 dark:text-white mb-4 px-2">
//                   Episodes
//                 </h2>
//                 <div className="space-y-2 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
//                   {episodes.map((ep, index) => (
//                     <button
//                       key={ep.id}
//                       onClick={() => setSelectedEpisode(ep)}
//                       className={`w-full text-left p-4 rounded-xl transition-all duration-300 transform hover:scale-102
//                                 ${selectedEpisode?.id === ep.id 
//                                   ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg' 
//                                   : 'bg-gray-50 dark:bg-gray-700/50 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 hover:shadow-md'
//                                 }`}
//                     >
//                       <div className="font-medium flex items-center">
//                         <span className="mr-2">📺</span>
//                         Episode {index + 1}
//                       </div>
//                       <div className={`text-sm mt-1 ${selectedEpisode?.id === ep.id ? 'text-blue-100' : 'text-gray-500 dark:text-gray-400'}`}>
//                         {ep.title}
//                       </div>
//                     </button>
//                   ))}
//                 </div>
//               </div>
//             </div>

//             {/* Selected Episode Detail - Right Column (2/3 width) */}
//             <div className="lg:col-span-2">
//               {selectedEpisode && (
//                 <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 border border-gray-100 dark:border-gray-700 transform transition-all duration-300 hover:shadow-2xl">
                  
//                   {/* Episode Header */}
//                   <div className="flex flex-col sm:flex-row justify-between items-start gap-4 mb-6">
//                     <div>
//                       <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-2">
//                         {selectedEpisode.title}
//                       </h2>
//                       <p className="text-gray-600 dark:text-gray-400 flex items-center">
//                         <span className="mr-2">📺</span>
//                         Episode {episodes.findIndex(e => e.id === selectedEpisode.id) + 1} of {episodes.length}
//                       </p>
//                     </div>
                    
//                     {/* Action Buttons - matches Home page button style */}
//                     <div className="flex flex-wrap gap-2">
//                       <button
//                         onClick={() => alert(`Regenerate episode - Backend integration pending`)}
//                         className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-all duration-300 transform hover:scale-105 text-sm font-medium"
//                       >
//                         🔄 Regenerate
//                       </button>
//                       <button
//                         onClick={() => alert(`Improve cliffhanger - Backend integration pending`)}
//                         className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-all duration-300 transform hover:scale-105 text-sm font-medium"
//                       >
//                         ⚡ Improve Cliffhanger
//                       </button>
//                       <button
//                         onClick={() => alert(`Export episode - Backend integration pending`)}
//                         className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 text-sm font-medium shadow-md"
//                       >
//                         📤 Export
//                       </button>
//                     </div>
//                   </div>

//                   {/* Episode Content - with theme styling */}
//                   <div className="prose dark:prose-invert max-w-none">
//                     <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
//                       {selectedEpisode.description}
//                     </p>
//                     <p className="text-gray-700 dark:text-gray-300 leading-relaxed mt-4">
//                       Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
//                     </p>
//                   </div>

//                   {/* Cliffhanger Preview - matches Home page card style */}
//                   <div className="mt-6 p-4 bg-gradient-to-r from-yellow-50 to-amber-50 dark:from-yellow-900/20 dark:to-amber-900/20 rounded-xl border border-yellow-200 dark:border-yellow-800">
//                     <h3 className="text-sm font-semibold text-yellow-800 dark:text-yellow-300 mb-2 flex items-center">
//                       <span className="mr-2">⚡</span>
//                       Cliffhanger Ending
//                     </h3>
//                     <p className="text-yellow-700 dark:text-yellow-400 text-sm">
//                       Just as they were about to discover the truth, a mysterious figure appeared in the shadows...
//                     </p>
//                   </div>
//                 </div>
//               )}
//             </div>
//           </div>
//         )}
//       </div>

//       {/* Add custom scrollbar styles */}
//       <style jsx>{`
//         .custom-scrollbar::-webkit-scrollbar {
//           width: 6px;
//         }
//         .custom-scrollbar::-webkit-scrollbar-track {
//           background: #f1f1f1;
//           border-radius: 10px;
//         }
//         .custom-scrollbar::-webkit-scrollbar-thumb {
//           background: #cbd5e0;
//           border-radius: 10px;
//         }
//         .custom-scrollbar::-webkit-scrollbar-thumb:hover {
//           background: #94a3b8;
//         }
//         .dark .custom-scrollbar::-webkit-scrollbar-track {
//           background: #2d3748;
//         }
//         .dark .custom-scrollbar::-webkit-scrollbar-thumb {
//           background: #4a5568;
//         }
//         .dark .custom-scrollbar::-webkit-scrollbar-thumb:hover {
//           background: #718096;
//         }
//       `}</style>
//     </div>
//   )
// }

// export default Episodes

import { useState, useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

const Episodes = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const [episodes, setEpisodes] = useState([])
  const [genre, setGenre] = useState('Thriller')
  const [tone, setTone] = useState('Suspenseful')
  const [selectedEpisode, setSelectedEpisode] = useState(null)
  const [loading, setLoading] = useState(false)

  // Get story data from location
  const story = location.state?.story || ''
  const storyTitle = location.state?.storyTitle || 'Your Story'
  const storyId = location.state?.storyId || null

  // Mock data - will be replaced with actual backend data
  // BACKEND WILL SEND ANY NUMBER OF EPISODES (NOT FIXED TO 7)
  useEffect(() => {
    const fetchEpisodes = async () => {
      setLoading(true)
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // MOCK DATA - BACKEND WILL REPLACE THIS WITH ACTUAL EPISODES
        // The number of episodes can be ANY (5, 8, 10, etc.)
        const mockEpisodes = [
          { id: 1, title: "The Mysterious Beginning", description: "A stranger arrives in a small town, bringing secrets that will change everything." },
          { id: 2, title: "The Secret Ingredient", description: "Dark secrets are revealed as the protagonist digs deeper into the mystery." },
          { id: 3, title: "Shadows of the Past", description: "The protagonist discovers a hidden truth about their family history." },
          { id: 4, title: "Twist in the Tale", description: "Nothing is what it seems as a major plot twist changes everything." },
          { id: 5, title: "Racing Against Time", description: "The clock is ticking as the antagonist makes their final move." },
          { id: 6, title: "The Final Revelation", description: "All secrets are unveiled in a shocking confrontation." },
          { id: 7, title: "Endgame", description: "The thrilling conclusion where everything comes together." },
        ]
        
        setEpisodes(mockEpisodes)
        setSelectedEpisode(mockEpisodes[0]) // Select first episode by default
      } catch (error) {
        console.error('Error fetching episodes:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchEpisodes()
  }, [genre, tone, storyId]) // Re-fetch when genre, tone, or story changes

  const genres = ['Thriller', 'Mystery', 'Romance', 'Sci-Fi', 'Fantasy', 'Horror', 'Drama', 'Comedy']
  const tones = ['Suspenseful', 'Dark', 'Light-hearted', 'Mysterious', 'Action-packed', 'Emotional', 'Humorous', 'Serious']

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 transition-colors duration-300 relative overflow-hidden">
      
      {/* Floating Emojis Background */}
      <div className="fixed inset-0 pointer-events-none opacity-10 dark:opacity-20">
        {['📺', '🎬', '📽️', '🎭', '📝', '✨'].map((emoji, i) => (
          <span
            key={i}
            className="absolute text-8xl animate-float"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${i * 0.5}s`,
              animationDuration: `${3 + i}s`
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
              {typeof story === 'string' ? story.substring(0, 150) + '...' : 'Your story'}
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
                {genres.map(g => (
                  <option key={g} value={g}>{g}</option>
                ))}
              </select>
            </div>

            {/* Episodes Info - DYNAMIC COUNT */}
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Episodes
              </label>
              <div className="p-3 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-gray-900 dark:to-gray-800 rounded-lg text-gray-800 dark:text-white font-semibold border-2 border-gray-200 dark:border-gray-700">
                {loading ? 'Loading...' : `${episodes.length} Episodes`}
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
                {tones.map(t => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>

            {/* Generate Button */}
            <div>
              <button
                onClick={() => alert('Generate new story arc - Backend integration pending')}
                className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
              >
                Generate Story Arc <span className="ml-2">✨</span>
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
            
            {/* Episodes List - Left Column - DYNAMIC SCROLLING LIST */}
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
                                ${selectedEpisode?.id === ep.id 
                                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg' 
                                  : 'bg-gray-50 dark:bg-gray-700/50 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 hover:shadow-md'
                                }`}
                    >
                      <div className="font-medium flex items-center">
                        <span className="mr-2">📺</span>
                        Episode {index + 1}
                      </div>
                      <div className={`text-sm mt-1 ${selectedEpisode?.id === ep.id ? 'text-blue-100' : 'text-gray-500 dark:text-gray-400'}`}>
                        {ep.title}
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
                        Episode {episodes.findIndex(e => e.id === selectedEpisode.id) + 1} of {episodes.length}
                      </p>
                    </div>
                    
                    {/* Action Buttons */}
                    <div className="flex flex-wrap gap-2">
                      <button
                        onClick={() => alert(`Regenerate episode - Backend integration pending`)}
                        className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-all duration-300 transform hover:scale-105 text-sm font-medium"
                      >
                        🔄 Regenerate
                      </button>
                      <button
                        onClick={() => alert(`Improve cliffhanger - Backend integration pending`)}
                        className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-all duration-300 transform hover:scale-105 text-sm font-medium"
                      >
                        ⚡ Improve Cliffhanger
                      </button>
                      <button
                        onClick={() => alert(`Export episode - Backend integration pending`)}
                        className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 text-sm font-medium shadow-md"
                      >
                        📤 Export
                      </button>
                    </div>
                  </div>

                  {/* Episode Content */}
                  <div className="prose dark:prose-invert max-w-none">
                    <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                      {selectedEpisode.description}
                    </p>
                    <p className="text-gray-700 dark:text-gray-300 leading-relaxed mt-4">
                      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                    </p>
                  </div>

                  {/* Cliffhanger Preview */}
                  <div className="mt-6 p-4 bg-gradient-to-r from-yellow-50 to-amber-50 dark:from-yellow-900/20 dark:to-amber-900/20 rounded-xl border border-yellow-200 dark:border-yellow-800">
                    <h3 className="text-sm font-semibold text-yellow-800 dark:text-yellow-300 mb-2 flex items-center">
                      <span className="mr-2">⚡</span>
                      Cliffhanger Ending
                    </h3>
                    <p className="text-yellow-700 dark:text-yellow-400 text-sm">
                      Just as they were about to discover the truth, a mysterious figure appeared in the shadows...
                    </p>
                  </div>
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
  )
}

export default Episodes