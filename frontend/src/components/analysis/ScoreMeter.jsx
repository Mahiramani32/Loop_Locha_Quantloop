const ScoreMeter = ({ label, score, color = "blue" }) => {
  const colors = {
    blue: "bg-blue-600",
    green: "bg-green-600",
    red: "bg-red-600",
    yellow: "bg-yellow-500"
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex justify-between items-center mb-2">
        <span className="text-gray-700 font-medium">{label}</span>
        <span className="text-3xl font-bold text-gray-800">{score}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-4">
        <div 
          className={`${colors[color]} h-4 rounded-full transition-all duration-500`}
          style={{ width: `${score}%` }}
        ></div>
      </div>
    </div>
  )
}

export default ScoreMeter