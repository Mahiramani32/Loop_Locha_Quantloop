import { BrowserRouter, Routes, Route } from 'react-router-dom'  // Update this import
import Home from './pages/Home'
import Results from './pages/Results'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App