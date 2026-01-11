import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './ResourceDebateView.css';

const ResourceDebateView = ({ data, onClose }) => {
    if (!data) return null;

    const { transcript, mitigations, summary, risk_contribution } = data;

    return (
        <motion.div
            className="debate-modal-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
        >
            <motion.div
                className="debate-modal-content"
                initial={{ y: 50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                exit={{ y: 50, opacity: 0 }}
                onClick={e => e.stopPropagation()}
            >
                <div className="modal-header">
                    <h2>Resource Debate Transcription</h2>
                    <button className="close-btn" onClick={onClose}>&times;</button>
                </div>

                <div className="debate-summary">
                    <div className="summary-item">
                        <span className="label">Risk Score</span>
                        <span className="value critical">{risk_contribution}%</span>
                    </div>
                    <div className="summary-item">
                        <span className="label">Consensus</span>
                        <p>{summary}</p>
                    </div>
                </div>

                <div className="transcript-container">
                    {transcript.map((entry, index) => (
                        <div key={index} className={`debate-entry ${entry.speaker.toLowerCase().split(' ')[0]}`}>
                            <div className="speaker-label">{entry.speaker}</div>
                            <div className="argument-bubble">
                                {entry.argument}
                            </div>
                        </div>
                    ))}
                </div>

                {mitigations && mitigations.length > 0 && (
                    <div className="mitigations-section">
                        <h3>Recommended Mitigations</h3>
                        <div className="mitigation-grid">
                            {mitigations.map((m, idx) => (
                                <div key={idx} className="mitigation-card">
                                    <h4>{m.strategy}</h4>
                                    <p>{m.action_plan}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </motion.div>
        </motion.div>
    );
};

export default ResourceDebateView;
