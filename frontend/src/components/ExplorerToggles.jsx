import { motion } from 'framer-motion'
import './ExplorerToggles.css'

function ExplorerToggles({ toggles, articleNumber, onToggle }) {
    if (!toggles || toggles.length === 0) return null

    const handleToggle = (toggleId, currentState) => {
        onToggle(articleNumber, toggleId, !currentState)
    }

    return (
        <div className="explorer-toggles">
            <h4 className="toggles-title">🔄 Interactive Explorer</h4>
            <p className="toggles-subtitle">Toggle scenarios to see real-time risk impact</p>

            <div className="toggles-list">
                {toggles.map((toggle, index) => (
                    <motion.div
                        key={toggle.toggle_id}
                        className="toggle-item glass-card"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                    >
                        <div className="toggle-content">
                            <div className="toggle-info">
                                <h5 className="toggle-question">{toggle.question}</h5>
                                <p className="toggle-description">{toggle.description}</p>
                            </div>

                            <div className="toggle-control">
                                <label className="toggle-switch">
                                    <input
                                        type="checkbox"
                                        checked={toggle.current_state}
                                        onChange={() => handleToggle(toggle.toggle_id, toggle.current_state)}
                                    />
                                    <span className="toggle-slider"></span>
                                </label>
                            </div>
                        </div>

                        <div className="toggle-impact">
                            <div className="impact-item">
                                <span className="impact-label">If YES:</span>
                                <span className={`impact-value ${toggle.impact_if_true < 0 ? 'positive' : 'negative'}`}>
                                    {toggle.impact_if_true > 0 ? '+' : ''}{toggle.impact_if_true} pts
                                </span>
                            </div>
                            <div className="impact-item">
                                <span className="impact-label">If NO:</span>
                                <span className={`impact-value ${toggle.impact_if_false < 0 ? 'positive' : 'negative'}`}>
                                    {toggle.impact_if_false > 0 ? '+' : ''}{toggle.impact_if_false} pts
                                </span>
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>
        </div>
    )
}

export default ExplorerToggles
