import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Platforms from './pages/Platforms'
import Keywords from './pages/Keywords'
import History from './pages/History'
import RSS from './pages/RSS'
import Settings from './pages/Settings'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/platforms" element={<Platforms />} />
          <Route path="/keywords" element={<Keywords />} />
          <Route path="/history" element={<History />} />
          <Route path="/rss" element={<RSS />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
