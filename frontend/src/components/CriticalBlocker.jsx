import { motion } from 'framer-motion'
import './CriticalBlocker.css'

function CriticalBlocker({ article }) {
    if (article.article_number !== 356) return null

    return (
        <motion.div
            className="critical-blocker"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
        >
            <div className="critical-header">
                <div className="critical-icon">🚨</div>
                <div>
                    <h2 className="critical-title">CRITICAL BLOCKER IDENTIFIED</h2>
                    <p className="critical-subtitle">Article 356: President's Rule - Primary Obstacle to ONOE</p>
                </div>
            </div>

            <div className="critical-content">
                <div className="critical-problem">
                    <h3>⚠️ The Constitutional Gap</h3>
                    <p>
                        <strong>NO PROCEDURE DEFINED</strong> for conducting elections in states under President's Rule
                        during synchronized national elections. The Constitution is completely silent on this scenario.
                    </p>
                    <div className="stat-highlight">
                        <span className="stat-number">73%</span>
                        <span className="stat-text">probability of at least one state under President's Rule during any 5-year ONOE cycle</span>
                    </div>
                </div>

                <div className="features-breakdown">
                    <h3>🎯 All 8 Features Applied</h3>
                    <div className="features-grid">
                        <div className="feature-box">
                            <span className="feature-icon">💬</span>
                            <div>
                                <strong>F1: Debate</strong>
                                <p>+{article.components.feature_1_debate?.toFixed(1)} pts</p>
                            </div>
                        </div>
                        <div className="feature-box">
                            <span className="feature-icon">📚</span>
                            <div>
                                <strong>F2: RAG Evidence</strong>
                                <p>{article.rag_evidence.length} sources</p>
                            </div>
                        </div>
                        <div className="feature-box">
                            <span className="feature-icon">⚖️</span>
                            <div>
                                <strong>F3: Precedents</strong>
                                <p>+{article.components.feature_3_precedent?.toFixed(1)} pts</p>
                            </div>
                        </div>
                        <div className="feature-box">
                            <span className="feature-icon">📊</span>
                            <div>
                                <strong>F4: Monte Carlo</strong>
                                <p>+{article.components.feature_4_confidence?.risk_contribution?.toFixed(1)} pts</p>
                            </div>
                        </div>
                        <div className="feature-box">
                            <span className="feature-icon">🔄</span>
                            <div>
                                <strong>F5: Explorer</strong>
                                <p>+{article.components.feature_5_explorer?.toFixed(1)} pts</p>
                            </div>
                        </div>
                        <div className="feature-box">
                            <span className="feature-icon">🏛️</span>
                            <div>
                                <strong>F6: Political</strong>
                                <p>+{article.components.feature_6_political?.toFixed(1)} pts</p>
                            </div>
                        </div>
                        <div className="feature-box">
                            <span className="feature-icon">⏱️</span>
                            <div>
                                <strong>F7: Timeline</strong>
                                <p>+{article.components.feature_7_timeline?.toFixed(1)} pts</p>
                            </div>
                        </div>
                        <div className="feature-box">
                            <span className="feature-icon">🎯</span>
                            <div>
                                <strong>F8: Priority</strong>
                                <p>Rank #{article.priority_rank}</p>
                            </div>
                        </div>
                    </div>
                </div>

                {article.rag_evidence.length > 0 && (
                    <div className="evidence-section">
                        <h3>📄 Documentary Evidence</h3>
                        {article.rag_evidence.map((evidence, idx) => (
                            <div key={idx} className="evidence-item">
                                <div className="evidence-source">{evidence.source}</div>
                                <blockquote className="evidence-quote">"{evidence.quote}"</blockquote>
                            </div>
                        ))}
                    </div>
                )}

                <div className="recommendation-box">
                    <h3>💡 Recommendation</h3>
                    <p className="recommendation-text">{article.recommendation}</p>
                </div>
            </div>
        </motion.div>
    )
}

export default CriticalBlocker
