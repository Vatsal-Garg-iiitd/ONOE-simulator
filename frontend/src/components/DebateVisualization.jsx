import { motion } from 'framer-motion'
import './DebateVisualization.css'

function DebateVisualization({ debate }) {
    if (!debate) return null

    const vulnerabilityPercentage = (debate.vulnerability_score * 100).toFixed(1)
    const transcript = debate.debate_transcript || []
    const mitigations = debate.mitigations || []

    // Separate transcript by type
    const governmentPoints = transcript.filter(t => t.speaker === 'GOVERNMENT')
    const courtPoints = transcript.filter(t => t.speaker === 'SUPREME COURT')
    const assessmentPoints = transcript.filter(t => t.speaker === 'ASSESSMENT')
    const mitigationPoints = transcript.filter(t => t.speaker === 'MITIGATION')

    return (
        <div className="debate-visualization">
            <h4 className="debate-title">⚖️ Constitutional Debate Analysis (LangGraph Enhanced)</h4>
            <p className="debate-subtitle">Multi-node AI workflow: Government → Court → Assessment → Mitigation</p>

            <div className="debate-container">
                {/* Government Side */}
                <motion.div
                    className="debate-side government-side"
                    initial={{ x: -50, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.2 }}
                >
                    <div className="debate-header">
                        <span className="debate-icon">🏛️</span>
                        <h5>Government Position</h5>
                    </div>

                    {governmentPoints.length > 0 ? (
                        governmentPoints.map((point, idx) => (
                            <div key={idx} className="debate-point">
                                <p className="debate-text">{point.argument}</p>
                            </div>
                        ))
                    ) : (
                        <p className="debate-text">{debate.government_argument}</p>
                    )}
                </motion.div>

                {/* Vulnerability Meter */}
                <div className="vulnerability-meter">
                    <div className="meter-label">Vulnerability Score</div>
                    <motion.div
                        className="meter-value"
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.5, type: "spring" }}
                    >
                        {vulnerabilityPercentage}%
                    </motion.div>
                    <div className="meter-bar">
                        <motion.div
                            className="meter-fill"
                            initial={{ width: 0 }}
                            animate={{ width: `${vulnerabilityPercentage}%` }}
                            transition={{ delay: 0.7, duration: 1 }}
                        />
                    </div>
                    <div className="meter-probability">
                        {debate.court_challenge_probability || `${vulnerabilityPercentage}%`} Court Challenge
                    </div>
                </div>

                {/* Court Side */}
                <motion.div
                    className="debate-side court-side"
                    initial={{ x: 50, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: 0.2 }}
                >
                    <div className="debate-header">
                        <span className="debate-icon">⚖️</span>
                        <h5>Supreme Court Counter</h5>
                    </div>

                    {courtPoints.length > 0 ? (
                        courtPoints.map((point, idx) => (
                            <div key={idx} className="debate-point">
                                <p className="debate-text">{point.argument}</p>
                            </div>
                        ))
                    ) : (
                        <p className="debate-text">{debate.court_argument}</p>
                    )}
                </motion.div>
            </div>

            {/* Assessment Section */}
            {assessmentPoints.length > 0 && (
                <motion.div
                    className="assessment-section"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.9 }}
                >
                    <h5>📊 AI Assessment</h5>
                    {assessmentPoints.map((point, idx) => (
                        <div key={idx} className="assessment-point">
                            {point.argument}
                        </div>
                    ))}
                </motion.div>
            )}

            {/* Mitigations Section */}
            {(mitigations.length > 0 || mitigationPoints.length > 0) && (
                <motion.div
                    className="mitigations-section"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.1 }}
                >
                    <h5>💡 Risk Mitigation Strategies</h5>
                    <div className="mitigations-grid">
                        {mitigations.map((mitigation, idx) => (
                            <div key={idx} className="mitigation-card">
                                <div className="mitigation-strategy">{mitigation.strategy}</div>
                                <div className="mitigation-basis">{mitigation.legal_basis}</div>
                            </div>
                        ))}
                        {mitigationPoints.map((point, idx) => (
                            <div key={idx} className="mitigation-card">
                                <div className="mitigation-text">{point.argument}</div>
                            </div>
                        ))}
                    </div>
                </motion.div>
            )}

            {/* Full Transcript */}
            {transcript.length > 0 && (
                <motion.div
                    className="full-transcript"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1.3 }}
                >
                    <details>
                        <summary>📜 View Full Debate Transcript ({transcript.length} exchanges)</summary>
                        <div className="transcript-content">
                            {transcript.map((entry, idx) => (
                                <div key={idx} className={`transcript-entry ${entry.type}`}>
                                    <span className="transcript-speaker">{entry.speaker}:</span>
                                    <span className="transcript-text">{entry.argument}</span>
                                </div>
                            ))}
                        </div>
                    </details>
                </motion.div>
            )}
        </div>
    )
}

export default DebateVisualization
