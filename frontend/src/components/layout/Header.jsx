import { Link, useLocation } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";

const Header = () => {
  const location = useLocation();
  const { isDark, toggleTheme } = useTheme();

  return (
    <header className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-md shadow-lg sticky top-0 z-50 border-b border-gray-200 dark:border-gray-800 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3 group">
            <span className="text-3xl group-hover:rotate-12 transition-transform duration-300">
              📚
            </span>
            <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 text-transparent bg-clip-text">
              StoryAnalyzer
            </span>
          </Link>

          {/* Navigation & Theme Toggle */}
          <div className="flex items-center space-x-2">
            <nav className="flex items-center space-x-1">
              <Link
                to="/"
                className={`px-4 py-2 rounded-lg transition-all duration-300 ${
                  location.pathname === "/"
                    ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-md"
                    : "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
                }`}
              >
                <span className="mr-2">🏠</span>
                Home
              </Link>
              <Link
                to="/dashboard"
                className={`px-4 py-2 rounded-lg transition-all duration-300 ${
                  location.pathname === "/dashboard"
                    ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-md"
                    : "text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800"
                }`}
              >
                <span className="mr-2">📊</span>
                Dashboard
              </Link>
            </nav>

            {/* Dark/Light Toggle Button */}
            <button
              onClick={toggleTheme}
              className="ml-4 p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-all duration-300 transform hover:scale-110 active:scale-95"
              aria-label="Toggle theme"
            >
              {isDark ? (
                <span className="text-2xl animate-spin-slow">☀️</span>
              ) : (
                <span className="text-2xl animate-bounce-slow">🌙</span>
              )}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
