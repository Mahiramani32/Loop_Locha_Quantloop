import { useLocation, useNavigate, useParams } from 'react-router-dom'
import Button from '../components/common/Button'
import ScoreMeter from '../components/analysis/ScoreMeter'
import EmotionChart from '../components/analysis/EmotionChart'

const Results = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const { id } = useParams()
  
  // Get story from location state or use ID
  const story = location.state?.story || (id ? `Loading story ${id}...` : '')

  // Mock data for now (will be replaced with real API data)
  const mockData = {
    cliffhangerScore: 82,
    retentionScore: 76,
    emotions: {
      joy: [10, 30, 45, 60, 40, 20],
      sadness: [5, 15, 30, 20, 10, 5],
      anger: [2, 8, 15, 10, 5, 2],
      fear: [15, 25, 35, 30, 20, 10],
      surprise: [20, 10, 25, 40, 35, 15]
    },
    suggestions: [
      "Add more suspense at the end to increase cliffhanger score",
      "Describe the main character's feelings more deeply",
      "Consider adding an unexpected plot twist in the middle",
      "The beginning could use more emotional impact"
    ]
  }

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      {/* Header with back button */}
      <div className="flex items-center mb-8">
        <Button 
          onClick={() => navigate('/')}
          variant="secondary"
        >
          ← Back
        </Button>
        <h1 className="text-3xl font-bold ml-4">Analysis Results</h1>
      </div>

      {/* Story Preview */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 className="text-xl font-semibold mb-2">Your Story</h2>
        <p className="text-gray-600 line-clamp-3">
          {story.substring(0, 200)}...
        </p>
      </div>

      {/* Scores Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <ScoreMeter 
          label="Cliffhanger Score" 
          score={mockData.cliffhangerScore}
          color="blue"
        />
        <ScoreMeter 
          label="Retention Score" 
          score={mockData.retentionScore}
          color="green"
        />
      </div>

      {/* Emotion Chart */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Emotion Journey</h2>
        <EmotionChart data={mockData.emotions} />
      </div>

      {/* Suggestions */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-4">💡 Suggestions to Improve</h2>
        <ul className="space-y-3">
          {mockData.suggestions.map((suggestion, index) => (
            <li key={index} className="flex items-start gap-2">
              <span className="text-blue-600 mt-1">•</span>
              <span className="text-gray-700">{suggestion}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default Results