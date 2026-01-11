import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import './ResourceDebateView.css';

const ResourceDebateView = ({ data, onClose }) => {
    if (!data) return null;

    const { transcript, mitigations, summary, risk_contribution } = data;

    // Speaker color mapping
    const getSpeakerColor = (speaker) => {
        const lowerSpeaker = speaker.toLowerCase();
        if (lowerSpeaker.includes('election') || lowerSpeaker.includes('commission')) {
            return { bg: 'rgba(59, 130, 246, 0.15)', border: 'rgba(59, 130, 246, 0.5)', text: '#60a5fa' };
        } else if (lowerSpeaker.includes('manufacturer') || lowerSpeaker.includes('bel') || lowerSpeaker.includes('ecil')) {
            return { bg: 'rgba(168, 85, 247, 0.15)', border: 'rgba(168, 85, 247, 0.5)', text: '#c084fc' };
        } else if (lowerSpeaker.includes('security') || lowerSpeaker.includes('mha')) {
            return { bg: 'rgba(239, 68, 68, 0.15)', border: 'rgba(239, 68, 68, 0.5)', text: '#f87171' };
        } else if (lowerSpeaker.includes('logistics')) {
            return { bg: 'rgba(251, 146, 60, 0.15)', border: 'rgba(251, 146, 60, 0.5)', text: '#fb923c' };
        } else if (lowerSpeaker.includes('analyst') || lowerSpeaker.includes('ai')) {
            return { bg: 'rgba(34, 197, 94, 0.15)', border: 'rgba(34, 197, 94, 0.5)', text: '#4ade80' };
        }
        return { bg: 'rgba(148, 163, 184, 0.15)', border: 'rgba(148, 163, 184, 0.5)', text: '#94a3b8' };
    };

    // Type badge styling
    const getTypeBadge = (type) => {
        const badges = {
            demand: { label: 'DEMAND', color: '#3b82f6' },
            constraint: { label: 'CONSTRAINT', color: '#a855f7' },
            blocker: { label: 'BLOCKER', color: '#ef4444' },
            risk: { label: 'RISK', color: '#f59e0b' },
            assessment: { label: 'ASSESSMENT', color: '#10b981' }
        };
        return badges[type] || { label: type.toUpperCase(), color: '#6b7280' };
    };

    return (
        <AnimatePresence>
            <motion.div
                className="debate-modal-overlay"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                onClick={onClose}
            >
                <motion.div
                    className="debate-modal-content resource-debate-modal"
                    initial={{ y: 50, opacity: 0, scale: 0.95 }}
                    animate={{ y: 0, opacity: 1, scale: 1 }}
                    exit={{ y: 50, opacity: 0, scale: 0.95 }}
                    onClick={e => e.stopPropagation()}
                >
                    {/* Header */}
                    <div className="modal-header">
                        <div>
                            <h2>⚡ Resource Demand Debate Transcript</h2>
                            <p className="debate-subtitle">Multi-stakeholder analysis using LangGraph workflow</p>
                        </div>
                        <button className="close-btn" onClick={onClose}>&times;</button>
                    </div>

                    {/* Summary Box */}
                    <motion.div
                        className="debate-summary glass-card"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.2 }}
                    >
                        <div className="summary-header">
                            <span className="summary-icon">📊</span>
                            <h3>Final Assessment</h3>
                        </div>
                        <p>{summary}</p>
                        <div className="risk-badge">
                            Risk Contribution: <strong>{risk_contribution}%</strong>
                        </div>
                    </motion.div>

                    {/* Transcript Section */}
                    <div className="transcript-section">
                        <h3 className="transcript-title">
                            <span>💬</span> Debate Exchanges ({transcript.length} turns)
                        </h3>

                        <div className="transcript-container">
                            {transcript.map((entry, index) => {
                                const colors = getSpeakerColor(entry.speaker);
                                const typeBadge = getTypeBadge(entry.type);

                                return (
                                    <motion.div
                                        key={index}
                                        className="transcript-entry"
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: 0.3 + (index * 0.1) }}
                                    >
                                        {/* Speaker Header */}
                                        <div className="speaker-header">
                                            <div
                                                className="speaker-avatar"
                                                style={{
                                                    background: colors.bg,
                                                    border: `2px solid ${colors.border}`,
                                                    color: colors.text
                                                }}
                                            >
                                                {entry.speaker.charAt(0)}
                                            </div>
                                            <div className="speaker-info">
                                                <span className="speaker-name" style={{ color: colors.text }}>
                                                    {entry.speaker}
                                                </span>
                                                <span
                                                    className="argument-type"
                                                    style={{
                                                        background: `${typeBadge.color}20`,
                                                        color: typeBadge.color,
                                                        border: `1px solid ${typeBadge.color}40`
                                                    }}
                                                >
                                                    {typeBadge.label}
                                                </span>
                                            </div>
                                        </div>

                                        {/* Argument Bubble */}
                                        <div
                                            className="argument-bubble"
                                            style={{
                                                background: colors.bg,
                                                borderLeft: `4px solid ${colors.border}`
                                            }}
                                        >
                                            <p>{entry.argument}</p>
                                        </div>
                                    </motion.div>
                                );
                            })}
                        </div>
                    </div>

                    {/* Mitigations Section */}
                    {mitigations && mitigations.length > 0 && (
                        <motion.div
                            className="mitigations-section"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.5 + (transcript.length * 0.1) }}
                        >
                            <h3 className="mitigations-title">
                                <span>🛡️</span> Strategic Mitigations
                            </h3>
                            <div className="mitigation-grid">
                                {mitigations.map((m, idx) => (
                                    <motion.div
                                        key={idx}
                                        className="mitigation-card glass-card"
                                        whileHover={{ scale: 1.02, boxShadow: '0 8px 20px rgba(0,0,0,0.3)' }}
                                    >
                                        <div className="mitigation-number">{idx + 1}</div>
                                        <h4>{m.strategy}</h4>
                                        <p>{m.action_plan}</p>
                                    </motion.div>
                                ))}
                            </div>
                        </motion.div>
                    )}
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
};

export default ResourceDebateView;
