import { useState, useEffect } from 'react'
import axios from 'axios'
import Dashboard from './pages/Dashboard'
import './App.css'

const API_BASE = 'http://localhost:8000'

function App() {
    const [articles, setArticles] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        fetchArticles()
    }, [])

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

    if (loading) {
        return (
            <div className="loading-screen">
                <div className="loading-spinner"></div>
                <h2 className="gradient-text">Loading Constitutional Engine...</h2>
            </div>
        )
    }

    if (error) {
        return (
            <div className="error-screen">
                <h2>⚠️ Error</h2>
                <p>{error}</p>
                <button className="btn btn-primary" onClick={fetchArticles}>
                    Retry
                </button>
            </div>
        )
    }

    return (
        <div className="app">
            <Dashboard
                articles={articles}
                onToggle={handleToggle}
                onRefresh={fetchArticles}
            />
        </div>
    )
}

export default App
