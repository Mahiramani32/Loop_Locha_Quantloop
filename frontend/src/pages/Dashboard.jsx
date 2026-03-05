import { useNavigate } from 'react-router-dom'
import Button from '../components/common/Button'

const Dashboard = () => {
  const navigate = useNavigate()

  // Mock data - will be replaced with real API data
  const stories = [
    { id: 1, title: "The Mysterious Forest", date: "2024-03-15", score: 82, preview: "Once upon a time in a dark forest..." },
    { id: 2, title: "Love at First Sight", date: "2024-03-14", score: 76, preview: "Sarah had always dreamed of..." },
    { id: 3, title: "The Last Adventure", date: "2024-03-13", score: 91, preview: "Captain Jack stood at the ship's bow..." },
    { id: 4, title: "Midnight Mystery", date: "2024-03-12", score: 68, preview: "The clock struck midnight and..." },
    { id: 5, title: "Dreams of Tomorrow", date: "2024-03-11", score: 88, preview: "In a world where dreams come true..." },
  ]

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">
          Your Story Dashboard 📊
        </h1>
        <Button onClick={() => navigate('/')}>
          + New Story
        </Button>
      </div>

      {/* Search Bar */}
      <div className="mb-6">
        <input
          type="text"
          placeholder="Search your stories..."
          className="w-full p-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none"
        />
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <p className="text-gray-600 text-sm">Total Stories</p>
          <p className="text-3xl font-bold text-gray-800">24</p>
        </div>
        <div className="bg-white rounded-xl shadow-lg p-6">
          <p className="text-gray-600 text-sm">Average Score</p>
          <p className="text-3xl font-bold text-green-600">81%</p>
        </div>
        <div className="bg-white rounded-xl shadow-lg p-6">
          <p className="text-gray-600 text-sm">Best Story</p>
          <p className="text-3xl font-bold text-blue-600">91%</p>
        </div>
      </div>

      {/* Stories List */}
      <h2 className="text-xl font-semibold mb-4">Recent Stories</h2>
      <div className="space-y-4">
        {stories.map((story) => (
          <div 
            key={story.id}
            className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow cursor-pointer"
            onClick={() => navigate(`/results/${story.id}`)}
          >
            <div className="flex justify-between items-start mb-2">
              <h3 className="text-lg font-semibold text-gray-800">{story.title}</h3>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                story.score >= 80 ? 'bg-green-100 text-green-700' :
                story.score >= 60 ? 'bg-yellow-100 text-yellow-700' :
                'bg-red-100 text-red-700'
              }`}>
                {story.score}%
              </span>
            </div>
            <p className="text-gray-600 mb-2">{story.preview}</p>
            <p className="text-sm text-gray-400">{story.date}</p>
          </div>
        ))}
      </div>

      {/* Load More Button */}
      <div className="flex justify-center mt-8">
        <Button variant="secondary" onClick={() => alert('Loading more...')}>
          Load More Stories
        </Button>
      </div>
    </div>
  )
}

export default Dashboard