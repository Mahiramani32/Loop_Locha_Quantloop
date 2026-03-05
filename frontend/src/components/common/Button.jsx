const Button = ({ children, onClick, type = "button", variant = "primary" }) => {
  const baseClasses = "px-6 py-2 rounded-lg font-semibold transition-all duration-200"
  
  const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300"
  }

  return (
    <button
      type={type}
      onClick={onClick}
      className={`${baseClasses} ${variants[variant]}`}
    >
      {children}
    </button>
  )
}

export default Button