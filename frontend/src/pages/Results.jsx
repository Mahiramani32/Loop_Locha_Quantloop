import { useLocation, useNavigate, useParams } from 'react-router-dom'
// ... rest of imports

const Results = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const { id } = useParams()  // Add this line
  
  // If ID exists, fetch that specific story (will connect to API later)
  const story = location.state?.story || (id ? `Loading story ${id}...` : '')
  
  // ... rest of component