import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import './BottleneckExplorer.css';

// Severity color mapping
const severityColors = {
    CRITICAL: {
        bg: 'rgba(239, 68, 68, 0.15)',
        border: 'rgba(239, 68, 68, 0.5)',
        text: '#ef4444',
        glow: '0 0 10px rgba(239, 68, 68, 0.3)'
    },
    HIGH: {
        bg: 'rgba(251, 146, 60, 0.15)',
        border: 'rgba(251, 146, 60, 0.5)',
        text: '#fb923c',
        glow: '0 0 10px rgba(251, 146, 60, 0.3)'
    },
    MEDIUM: {
        bg: 'rgba(250, 204, 21, 0.15)',
        border: 'rgba(250, 204, 21, 0.5)',
        text: '#facc15',
        glow: '0 0 10px rgba(250, 204, 21, 0.3)'
    }
};

// Category icon mapping
const categoryIcons = {
    manufacturing: '🏭',
    coordination: '🤝',
    timeline: '⏱️',
    security: '🛡️',
    legal: '⚖️',
    supply_chain: '📦',
    other: '⚠️'
};

function BottleneckExplorer({ targetYear, evmSupply, securityPersonnel }) {
    const [bottlenecks, setBottlenecks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [analysisMode, setAnalysisMode] = useState('');
    const [overallStatus, setOverallStatus] = useState('');

    useEffect(() => {
        fetchBottlenecks();
    }, [targetYear, evmSupply, securityPersonnel]);

    const fetchBottlenecks = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/admin/bottleneck/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    target_year: targetYear || 2029,
                    evm_supply: evmSupply || 100,
                    security_personnel: securityPersonnel || 100
                })
            });

            if (response.ok) {
                const data = await response.json();
                setBottlenecks(data.bottlenecks || []);
                setAnalysisMode(data.analysis_mode || 'Unknown');
                setOverallStatus(data.status || '');
            } else {
                console.error('Failed to fetch bottlenecks');
            }
        } catch (error) {
            console.error('Error fetching bottlenecks:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="bottleneck-explorer glass-card">
                <h3 className="section-title">🔍 Bottleneck Analysis</h3>
                <div className="loading-state">
                    <div className="spinner"></div>
                    <p>Analyzing administrative challenges...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="bottleneck-explorer glass-card">
            <div className="bottleneck-header">
                <div>
                    <h3 className="section-title">🔍 Critical Bottleneck Analysis</h3>
                    <p className="analysis-mode">
                        {analysisMode === 'LLM' ? '🤖 AI-Powered Analysis' : '⚙️ Rule-Based Analysis'}
                    </p>
                </div>
                {overallStatus && (
                    <div className="overall-status" style={{
                        padding: '0.5rem 1rem',
                        borderRadius: '8px',
                        background: bottlenecks.some(b => b.severity === 'CRITICAL') ?
                            'rgba(239, 68, 68, 0.2)' : 'rgba(251, 146, 60, 0.2)',
                        border: `1px solid ${bottlenecks.some(b => b.severity === 'CRITICAL') ?
                            'rgba(239, 68, 68, 0.5)' : 'rgba(251, 146, 60, 0.5)'}`,
                        fontSize: '0.9rem',
                        fontWeight: 'bold'
                    }}>
                        {overallStatus}
                    </div>
                )}
            </div>

            <div className="bottleneck-grid">
                {bottlenecks.map((bottleneck, index) => {
                    const colors = severityColors[bottleneck.severity] || severityColors.MEDIUM;
                    const icon = categoryIcons[bottleneck.category] || categoryIcons.other;

                    return (
                        <motion.div
                            key={index}
                            className="bottleneck-card"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                            style={{
                                background: colors.bg,
                                border: `1px solid ${colors.border}`,
                                borderLeft: `4px solid ${colors.border}`,
                                boxShadow: colors.glow
                            }}
                        >
                            <div className="bottleneck-card-header">
                                <span className="bottleneck-icon">{icon}</span>
                                <span
                                    className="bottleneck-severity"
                                    style={{
                                        color: colors.text,
                                        background: `${colors.bg}80`,
                                        border: `1px solid ${colors.border}`
                                    }}
                                >
                                    {bottleneck.severity}
                                </span>
                            </div>

                            <h4 className="bottleneck-name" style={{ color: colors.text }}>
                                {bottleneck.name}
                            </h4>

                            <p className="bottleneck-description">
                                {bottleneck.description}
                            </p>

                            <div className="bottleneck-impact">
                                <strong style={{ color: colors.text }}>Impact:</strong>
                                <p>{bottleneck.impact}</p>
                            </div>
                        </motion.div>
                    );
                })}
            </div>

            {bottlenecks.length === 0 && (
                <div className="no-bottlenecks">
                    <p>✅ No critical bottlenecks detected. All systems operational.</p>
                </div>
            )}

            <button
                className="refresh-btn"
                onClick={fetchBottlenecks}
                style={{
                    marginTop: '1.5rem',
                    padding: '0.75rem 1.5rem',
                    background: 'rgba(59, 130, 246, 0.2)',
                    border: '1px solid rgba(59, 130, 246, 0.5)',
                    borderRadius: '8px',
                    color: '#60a5fa',
                    cursor: 'pointer',
                    transition: 'all 0.2s'
                }}
                onMouseOver={(e) => {
                    e.target.style.background = 'rgba(59, 130, 246, 0.3)';
                    e.target.style.transform = 'translateY(-2px)';
                }}
                onMouseOut={(e) => {
                    e.target.style.background = 'rgba(59, 130, 246, 0.2)';
                    e.target.style.transform = 'translateY(0)';
                }}
            >
                🔄 Refresh Analysis
            </button>
        </div>
    );
}

export default BottleneckExplorer;
