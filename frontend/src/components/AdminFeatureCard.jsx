import { motion } from 'framer-motion'
import './ArticleCard.css' // Reuse basic card styles

function AdminFeatureCard({ feature, onClick, index }) {
    const getStatusBadgeClass = (status) => {
        const s = status.toLowerCase();
        if (s.includes('critical')) return 'badge-critical';
        if (s.includes('high')) return 'badge-high';
        if (s.includes('moderate')) return 'badge-warning';
        return 'badge-normal';
    }

    return (
        <motion.div
            className="article-card card glass-card"
            onClick={onClick}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ scale: 1.02 }}
        >
            <div className="article-card-header">
                <div className="article-info">
                    <h3 className="article-title">{feature.name}</h3>
                    <p className="article-subtitle">ID: {feature.id.toUpperCase()}</p>
                </div>
            </div>

            <div className="article-card-body">
                <div className="risk-gauge-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                    {/* Simplified visual for risk contribution */}
                    <div style={{
                        width: '80px', height: '80px',
                        borderRadius: '50%', border: '4px solid rgba(255,255,255,0.1)',
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        position: 'relative'
                    }}>
                        <span style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'white' }}>
                            {feature.risk_contribution}%
                        </span>
                        <svg style={{ position: 'absolute', width: '100%', height: '100%', transform: 'rotate(-90deg)' }}>
                            <circle
                                cx="40" cy="40" r="36"
                                fill="transparent"
                                stroke={feature.risk_contribution > 15 ? "var(--color-risk-high)" : "var(--color-risk-low)"}
                                strokeWidth="4"
                                strokeDasharray={`${feature.risk_contribution * 2.26} 226`}
                            />
                        </svg>
                    </div>
                    <span style={{ marginTop: '0.5rem', fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>Risk Contrib.</span>
                </div>

                <div className="article-details">
                    <div className="status-badge-container">
                        <span className={`badge ${getStatusBadgeClass(feature.status)}`}>
                            {feature.status}
                        </span>
                    </div>

                    <p className="article-description">{feature.description}</p>
                </div>
            </div>

            <div className="article-card-footer">
                <div className="feature-indicators">
                    {/* Mock indicators for now */}
                    <span className="feature-dot" title="Details Available">📊</span>
                    {feature.id === 'f1' && <span className="feature-dot" title="Interactive Debate">💬</span>}
                    {feature.id === 'f3' && <span className="feature-dot" title="Bottlenecks">⚠️</span>}
                </div>
                <button className="view-details-btn">View Analysis →</button>
            </div>
        </motion.div>
    )
}

export default AdminFeatureCard
