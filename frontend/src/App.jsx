// import { BrowserRouter, Routes, Route } from 'react-router-dom'
// import { ThemeProvider } from './context/ThemeContext'
// import Layout from './components/layout/Layout'
// import Home from './pages/Home'
// import Results from './pages/Results'
// import Dashboard from './pages/Dashboard'

// function App() {
//   return (
//     <ThemeProvider>
//       <BrowserRouter>
//         <Layout>
//           <Routes>
//             <Route path="/" element={<Home />} />
//             <Route path="/results" element={<Results />} />
//             <Route path="/results/:id" element={<Results />} />
//             <Route path="/dashboard" element={<Dashboard />} />
//           </Routes>
//         </Layout>
//       </BrowserRouter>
//     </ThemeProvider>
//   )
// }

// export default App

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'
import Layout from './components/layout/Layout'
import Home from './pages/Home'
import Results from './pages/Results'
import Dashboard from './pages/Dashboard'

function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/results" element={<Results />} />
            <Route path="/results/:id" element={<Results />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </Layout>
      </BrowserRouter>
    </ThemeProvider>
  )
}

export default App