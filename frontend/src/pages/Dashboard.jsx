import { useState } from 'react'
import { motion } from 'framer-motion'
import ArticleCard from '../components/ArticleCard'
import CriticalBlocker from '../components/CriticalBlocker'
import DebateVisualization from '../components/DebateVisualization'
import ExplorerToggles from '../components/ExplorerToggles'
import MonteCarloChart from '../components/MonteCarloChart'
import FeatureBreakdown from '../components/FeatureBreakdown'
import './Dashboard.css'

function ConstitutionalDashboard({ articles, onToggle, onRefresh }) {
    const [selectedArticleId, setSelectedArticleId] = useState(null)

    // Find Article 356 (critical blocker)
    const article356 = articles.find(a => a.article_number === 356)

    // Calculate overall metrics
    const criticalCount = articles.filter(a => a.status === 'CRITICAL BLOCKER').length
    const averageRisk = articles.reduce((sum, a) => sum + a.final_risk, 0) / articles.length

    // Sort articles by priority
    const sortedArticles = [...articles].sort((a, b) =>
        (a.priority_rank || 999) - (b.priority_rank || 999)
    )

    // Derive selected article from props to ensure reactivity
    const selectedArticle = articles.find(a => a.article_number === selectedArticleId)

    const handleArticleClick = (article) => {
        setSelectedArticleId(article.article_number === selectedArticleId ? null : article.article_number)
    }

    return (
        <div className="dashboard">
            {/* Hero Section */}
            <motion.header
                className="dashboard-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div className="container">
                    <h1 className="dashboard-title">
                        <span className="gradient-text">Constitutional Engine</span>
                    </h1>
                    <p className="dashboard-subtitle">
                        Advanced AI-Powered Analysis of One Nation One Election Feasibility
                    </p>

                    <div className="metrics-grid">
                        <div className="metric-card glass-card">
                            <span className="metric-icon">📊</span>
                            <div>
                                <div className="metric-value">{articles.length}</div>
                                <div className="metric-label">Articles Analyzed</div>
                            </div>
                        </div>
                        <div className="metric-card glass-card">
                            <span className="metric-icon">⚠️</span>
                            <div>
                                <div className="metric-value">{criticalCount}</div>
                                <div className="metric-label">Critical Blockers</div>
                            </div>
                        </div>
                        <div className="metric-card glass-card">
                            <span className="metric-icon">📈</span>
                            <div>
                                <div className="metric-value">{averageRisk.toFixed(1)}</div>
                                <div className="metric-label">Average Risk Score</div>
                            </div>
                        </div>
                        <div className="metric-card glass-card">
                            <span className="metric-icon">🎯</span>
                            <div>
                                <div className="metric-value">8</div>
                                <div className="metric-label">Advanced Features</div>
                            </div>
                        </div>
                    </div>
                </div>
            </motion.header>

            <div className="container">
                {/* Critical Blocker Section */}
                {article356 && <CriticalBlocker article={article356} />}

                {/* Articles Grid */}
                <section className="articles-section">
                    <div className="section-header">
                        <h2>Constitutional Articles Analysis</h2>
                        <p className="section-subtitle">
                            Click on any article to view detailed analysis with interactive features
                        </p>
                    </div>

                    <div className="articles-grid">
                        {sortedArticles.map((article, index) => (
                            <ArticleCard
                                key={article.article_number}
                                article={article}
                                onClick={() => handleArticleClick(article)}
                                index={index}
                            />
                        ))}
                    </div>
                </section>

                {/* Detailed Article View */}
                {selectedArticle && (
                    <motion.section
                        className="article-detail"
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                    >
                        <div className="detail-header">
                            <h2>Article {selectedArticle.article_number} - Detailed Analysis</h2>
                            <button
                                className="close-btn"
                                onClick={() => setSelectedArticleId(null)}
                            >
                                ✕
                            </button>
                        </div>

                        <div className="detail-content">
                            {/* Feature Breakdown - Show First */}
                            <FeatureBreakdown article={selectedArticle} />

                            {/* Debate Visualization */}
                            {selectedArticle.debate_result && (
                                <DebateVisualization debate={selectedArticle.debate_result} />
                            )}

                            {/* Monte Carlo Chart */}
                            {selectedArticle.components.feature_4_confidence && (
                                <MonteCarloChart monteCarloData={selectedArticle.components.feature_4_confidence} />
                            )}

                            {/* Explorer Toggles */}
                            {selectedArticle.explorer_toggles && selectedArticle.explorer_toggles.length > 0 && (
                                <ExplorerToggles
                                    toggles={selectedArticle.explorer_toggles}
                                    articleNumber={selectedArticle.article_number}
                                    onToggle={onToggle}
                                />
                            )}

                            {/* Precedents */}
                            {selectedArticle.precedents && selectedArticle.precedents.length > 0 && (
                                <div className="precedents-section">
                                    <h4>⚖️ Relevant Supreme Court Precedents</h4>
                                    <div className="precedents-list">
                                        {selectedArticle.precedents.map((precedent, idx) => (
                                            <div key={idx} className="precedent-item glass-card">
                                                <div className="precedent-header">
                                                    <strong>{precedent.case_name}</strong>
                                                    <span className="precedent-year">({precedent.year})</span>
                                                </div>
                                                <p className="precedent-relevance">{precedent.relevance}</p>
                                                <div className="precedent-impact">
                                                    Impact Score: <span className="impact-score">{precedent.impact_score}/5</span>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* RAG Evidence */}
                            {selectedArticle.rag_evidence && selectedArticle.rag_evidence.length > 0 && (
                                <div className="rag-evidence-section">
                                    <h4>📚 Documentary Evidence (RAG)</h4>
                                    <div className="evidence-list">
                                        {selectedArticle.rag_evidence.map((evidence, idx) => (
                                            <div key={idx} className="evidence-card glass-card">
                                                <div className="evidence-source-tag">{evidence.source}</div>
                                                <blockquote className="evidence-text">"{evidence.quote}"</blockquote>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Timeline & Political Support */}
                            <div className="additional-info">
                                {selectedArticle.timeline && (
                                    <div className="info-box glass-card">
                                        <h5>⏱️ Timeline Feasibility</h5>
                                        <div className="timeline-data">
                                            <div className="timeline-item">
                                                <span>Months Needed:</span>
                                                <strong>{selectedArticle.timeline.months_needed}</strong>
                                            </div>
                                            <div className="timeline-item">
                                                <span>Months Available:</span>
                                                <strong>{selectedArticle.timeline.months_available}</strong>
                                            </div>
                                            <div className="timeline-item">
                                                <span>Status:</span>
                                                <span className={`status-badge ${selectedArticle.timeline.feasible ? 'feasible' : 'not-feasible'}`}>
                                                    {selectedArticle.timeline.status}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                )}

                                {selectedArticle.political_support && (
                                    <div className="info-box glass-card">
                                        <h5>🏛️ Political Support</h5>
                                        <div className="political-data">
                                            <div className="support-bar">
                                                <div className="support-label">
                                                    Current: {selectedArticle.political_support.current_support}%
                                                </div>
                                                <div className="support-progress">
                                                    <div
                                                        className="support-fill"
                                                        style={{ width: `${selectedArticle.political_support.current_support}%` }}
                                                    />
                                                    <div
                                                        className="support-required"
                                                        style={{ left: `${selectedArticle.political_support.required_support}%` }}
                                                    >
                                                        Required: {selectedArticle.political_support.required_support}%
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>

                            {/* Recommendation */}
                            <div className="recommendation-final">
                                <h4>💡 Recommendation</h4>
                                <p>{selectedArticle.recommendation}</p>
                            </div>
                        </div>
                    </motion.section>
                )}

                {/* Footer */}
                <footer className="dashboard-footer">
                    <p>
                        Constitutional Engine v1.0 | Built with FastAPI + React |
                        Powered by 8 Advanced Features: AI Debate, RAG, Precedent Analysis, Monte Carlo,
                        Explorer, Political Tracker, Timeline, Priority Ranking
                    </p>
                </footer>
            </div>
        </div>
    )
}

export default ConstitutionalDashboard
