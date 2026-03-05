import { useState } from 'react'
import { useNavigate } from 'react-router-dom'  // Add this import
import Button from '../components/common/Button'

const Home = () => {
  const [story, setStory] = useState('')
  const navigate = useNavigate()  // Add this line

  const handleAnalyze = () => {
    if (story.trim().length < 10) {
      alert('Please write a longer story (at least 10 characters)')
      return
    }
    // Navigate to results page with story data
    navigate('/results', { state: { story } })
  }

  return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <h1 className="text-4xl font-bold text-center mb-4 text-gray-800">
        Story Analyzer 📖
      </h1>
      <p className="text-center text-gray-600 mb-8">
        Paste your story and get AI-powered insights
      </p>
      
      <textarea
        className="w-full h-64 p-4 border-2 border-gray-200 rounded-xl shadow-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all"
        placeholder="Once upon a time..."
        value={story}
        onChange={(e) => setStory(e.target.value)}
      />
      
      <div className="flex justify-center mt-6">
        <Button onClick={handleAnalyze}>  {/* Changed this */}
          Analyze Story 🔍
        </Button>
      </div>
    </div>
  )
}

export default Home