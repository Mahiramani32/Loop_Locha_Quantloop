import { Link, useLocation } from 'react-router-dom'

const Header = () => {
  const location = useLocation()
  
  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold text-blue-600">
            📖 StoryAnalyzer
          </Link>
          <nav className="space-x-6">
            <Link 
              to="/" 
              className={`${location.pathname === '/' ? 'text-blue-600 font-semibold' : 'text-gray-600'} hover:text-blue-600`}
            >
              Home
            </Link>
            <Link 
              to="/dashboard" 
              className={`${location.pathname === '/dashboard' ? 'text-blue-600 font-semibold' : 'text-gray-600'} hover:text-blue-600`}
            >
              Dashboard
            </Link>
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header