import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom'
import axios from 'axios'
import Home from './pages/Home'
import ConstitutionalDashboard from './pages/Dashboard'
import AdminDashboard from './pages/AdminDashboard'
import './App.css'

const API_BASE = 'http://localhost:8000'

function AppContent() {
    const [articles, setArticles] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const location = useLocation()

    useEffect(() => {
        // Only fetch articles if we are on the Constitutional Dashboard
        if (location.pathname === '/constitutional') {
            fetchArticles()
        } else {
            setLoading(false) // Don't block other pages
        }
    }, [location.pathname])

    const fetchArticles = async () => {
        try {
            setLoading(true)
            const response = await axios.get(`${API_BASE}/api/articles/`)
            setArticles(response.data)
            setError(null)
        } catch (err) {
            setError('Failed to load articles. Make sure the backend is running on port 8000.')
            console.error('Error fetching articles:', err)
        } finally {
            setLoading(false)
        }
    }

    const handleToggle = async (articleNumber, toggleId, newState) => {
        try {
            const response = await axios.post(
                `${API_BASE}/api/articles/${articleNumber}/toggle`,
                { toggle_id: toggleId, new_state: newState }
            )

            // Update the specific article in state
            setArticles(prev => prev.map(article =>
                article.article_number === articleNumber
                    ? response.data.updated_article
                    : article
            ))
        } catch (err) {
            console.error('Error applying toggle:', err)
        }
    }

    return (
        <div className="app">
            <Routes>
                <Route path="/" element={<Home />} />
                <Route
                    path="/constitutional"
                    element={
                        loading ? (
                            <div className="loading-screen">
                                <div className="loading-spinner"></div>
                                <h2 className="gradient-text">Loading Constitutional Engine...</h2>
                            </div>
                        ) : error ? (
                            <div className="error-screen">
                                <h2>⚠️ Error</h2>
                                <p>{error}</p>
                                <button className="btn btn-primary" onClick={fetchArticles}>
                                    Retry
                                </button>
                            </div>
                        ) : (
                            <ConstitutionalDashboard
                                articles={articles}
                                onToggle={handleToggle}
                                onRefresh={fetchArticles}
                            />
                        )
                    }
                />
                <Route path="/administrative" element={<AdminDashboard />} />
            </Routes>
        </div>
    )
}

function App() {
    return (
        <Router>
            <AppContent />
        </Router>
    )
}

export default App
