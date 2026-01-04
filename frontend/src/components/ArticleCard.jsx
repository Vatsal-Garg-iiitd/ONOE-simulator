import { motion } from 'framer-motion'
import RiskGauge from './RiskGauge'
import './ArticleCard.css'

function ArticleCard({ article, onClick, index }) {
    const getStatusBadgeClass = (status) => {
        switch (status) {
            case 'CRITICAL BLOCKER':
                return 'badge-critical'
            case 'HIGH_RISK':
                return 'badge-high'
            case 'WARNING':
                return 'badge-warning'
            default:
                return 'badge-normal'
        }
    }

    return (
        <motion.div
            className="article-card card"
            onClick={onClick}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.02 }}
        >
            <div className="article-card-header">
                <div className="article-info">
                    <h3 className="article-title">Article {article.article_number}</h3>
                    <p className="article-subtitle">{article.name.split(':')[1] || article.name}</p>
                </div>
                {article.priority_rank && (
                    <div className="priority-badge">
                        <span className="priority-number">#{article.priority_rank}</span>
                    </div>
                )}
            </div>

            <div className="article-card-body">
                <div className="risk-gauge-container">
                    <RiskGauge risk={article.final_risk} size={140} />
                </div>

                <div className="article-details">
                    <div className="status-badge-container">
                        <span className={`badge ${getStatusBadgeClass(article.status)}`}>
                            {article.status.replace('_', ' ')}
                        </span>
                    </div>

                    <p className="article-description">{article.description}</p>

                    {article.article_number === 356 && (
                        <div className="critical-alert">
                            <span className="alert-icon">⚠️</span>
                            <span>PRIMARY BLOCKER</span>
                        </div>
                    )}
                </div>
            </div>

            <div className="article-card-footer">
                <div className="feature-indicators">
                    {article.components.feature_1_debate !== null && <span className="feature-dot" title="F1: Debate">💬</span>}
                    {article.rag_evidence.length > 0 && <span className="feature-dot" title="F2: RAG">📚</span>}
                    {article.precedents.length > 0 && <span className="feature-dot" title="F3: Precedent">⚖️</span>}
                    {article.components.feature_4_confidence && <span className="feature-dot" title="F4: Monte Carlo">📊</span>}
                    {article.explorer_toggles.length > 0 && <span className="feature-dot" title="F5: Explorer">🔄</span>}
                    {article.political_support && <span className="feature-dot" title="F6: Political">🏛️</span>}
                    {article.timeline && <span className="feature-dot" title="F7: Timeline">⏱️</span>}
                    {article.priority_rank && <span className="feature-dot" title="F8: Priority">🎯</span>}
                </div>
                <button className="view-details-btn">View Details →</button>
            </div>
        </motion.div>
    )
}

export default ArticleCard
