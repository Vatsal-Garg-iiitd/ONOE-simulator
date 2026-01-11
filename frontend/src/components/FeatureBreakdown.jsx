import { useState } from 'react'
import { motion } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, LineChart, Line, Legend } from 'recharts'
import './FeatureBreakdown.css'

const FEATURE_INFO = {
    F1: {
        name: 'AI Debate Agent',
        icon: '💬',
        description: 'Simulates Government vs Supreme Court constitutional arguments',
        color: '#667eea',
        gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    },
    F2: {
        name: 'RAG System',
        icon: '📚',
        description: 'Retrieves evidence from Constitution and Kovind Committee Report',
        color: '#11998e',
        gradient: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)'
    },
    F3: {
        name: 'Precedent Analysis',
        icon: '⚖️',
        description: 'Analyzes relevant Supreme Court cases',
        color: '#f093fb',
        gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
    },
    F4: {
        name: 'Monte Carlo Simulation',
        icon: '📊',
        description: 'Probabilistic risk modeling with confidence intervals',
        color: '#fa709a',
        gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
    },
    F5: {
        name: 'Real-time Explorer',
        icon: '🔄',
        description: 'Interactive toggles for "what-if" scenarios',
        color: '#4facfe',
        gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
    },
    F6: {
        name: 'Political Support Tracker',
        icon: '🏛️',
        description: 'Tracks parliamentary majority requirements',
        color: '#43e97b',
        gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
    },
    F7: {
        name: 'Timeline Feasibility',
        icon: '⏱️',
        description: 'Assesses amendment completion timelines',
        color: '#fa709a',
        gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
    },
    F8: {
        name: 'Priority Ranking',
        icon: '🎯',
        description: 'Ranks articles by risk and impact',
        color: '#ff0844',
        gradient: 'linear-gradient(135deg, #ff0844 0%, #ffb199 100%)'
    }
}

function FeatureBreakdown({ article }) {
    const [selectedView, setSelectedView] = useState('breakdown') // breakdown, waterfall, radar

    if (!article) return null

    const { components, base_risk, final_risk } = article

    // Build feature data array
    const features = []
    let cumulativeRisk = base_risk

    // Feature 1: Debate
    if (components.feature_1_debate !== null && components.feature_1_debate !== undefined) {
        const riskContribution = components.feature_1_debate
        const reason = article.debate_result 
            ? `Vulnerability Score: ${(article.debate_result.vulnerability_score * 100).toFixed(1)}% - ${article.debate_result.court_argument.substring(0, 150)}...`
            : 'AI-simulated debate reveals constitutional vulnerabilities'
        features.push({
            id: 'F1',
            name: FEATURE_INFO.F1.name,
            icon: FEATURE_INFO.F1.icon,
            riskContribution,
            cumulativeRisk: cumulativeRisk + riskContribution,
            reason,
            color: FEATURE_INFO.F1.color,
            gradient: FEATURE_INFO.F1.gradient,
            details: article.debate_result ? {
                government: article.debate_result.government_argument,
                court: article.debate_result.court_argument,
                vulnerability: article.debate_result.vulnerability_score
            } : null
        })
        cumulativeRisk += riskContribution
    }

    // Feature 2: RAG
    if (article.rag_evidence && article.rag_evidence.length > 0) {
        const riskContribution = 0 // RAG doesn't directly contribute to risk, but provides evidence
        const topEvidence = article.rag_evidence[0]
        const reason = `Found ${article.rag_evidence.length} evidence document(s) - "${topEvidence.quote.substring(0, 100)}..."`
        features.push({
            id: 'F2',
            name: FEATURE_INFO.F2.name,
            icon: FEATURE_INFO.F2.icon,
            riskContribution,
            cumulativeRisk,
            reason,
            color: FEATURE_INFO.F2.color,
            gradient: FEATURE_INFO.F2.gradient,
            details: {
                evidenceCount: article.rag_evidence.length,
                evidence: article.rag_evidence
            }
        })
    }

    // Feature 3: Precedent
    if (components.feature_3_precedent !== null && components.feature_3_precedent !== undefined) {
        const riskContribution = components.feature_3_precedent
        const topPrecedent = article.precedents && article.precedents.length > 0 ? article.precedents[0] : null
        const reason = topPrecedent 
            ? `${article.precedents.length} relevant case(s) found - ${topPrecedent.case_name} (${topPrecedent.year}): ${topPrecedent.relevance.substring(0, 100)}...`
            : 'Historical Supreme Court precedents indicate constitutional risks'
        features.push({
            id: 'F3',
            name: FEATURE_INFO.F3.name,
            icon: FEATURE_INFO.F3.icon,
            riskContribution,
            cumulativeRisk: cumulativeRisk + riskContribution,
            reason,
            color: FEATURE_INFO.F3.color,
            gradient: FEATURE_INFO.F3.gradient,
            details: {
                precedents: article.precedents || []
            }
        })
        cumulativeRisk += riskContribution
    }

    // Feature 4: Monte Carlo
    if (components.feature_4_confidence) {
        const mc = components.feature_4_confidence
        const riskContribution = (typeof mc === 'object' && mc.risk_contribution !== undefined) 
            ? mc.risk_contribution 
            : 0
        const ci = mc.confidence_interval_95 || [0, 0]
        const mean = mc.mean || 0
        const stdDev = mc.std_dev || 0
        const reason = `95% Confidence Interval: [${ci[0].toFixed(1)}, ${ci[1].toFixed(1)}] - Mean: ${mean.toFixed(1)} ± ${stdDev.toFixed(1)}`
        features.push({
            id: 'F4',
            name: FEATURE_INFO.F4.name,
            icon: FEATURE_INFO.F4.icon,
            riskContribution,
            cumulativeRisk: cumulativeRisk + riskContribution,
            reason,
            color: FEATURE_INFO.F4.color,
            gradient: FEATURE_INFO.F4.gradient,
            details: mc
        })
        cumulativeRisk += riskContribution
    }

    // Feature 5: Explorer
    if (components.feature_5_explorer !== null && components.feature_5_explorer !== undefined) {
        const riskContribution = components.feature_5_explorer
        const toggleCount = article.explorer_toggles ? article.explorer_toggles.length : 0
        const reason = `${toggleCount} interactive scenario(s) analyzed - Current state indicates ${riskContribution > 0 ? 'increased' : 'reduced'} risk`
        features.push({
            id: 'F5',
            name: FEATURE_INFO.F5.name,
            icon: FEATURE_INFO.F5.icon,
            riskContribution,
            cumulativeRisk: cumulativeRisk + riskContribution,
            reason,
            color: FEATURE_INFO.F5.color,
            gradient: FEATURE_INFO.F5.gradient,
            details: {
                toggles: article.explorer_toggles || []
            }
        })
        cumulativeRisk += riskContribution
    }

    // Feature 6: Political
    if (components.feature_6_political !== null && components.feature_6_political !== undefined) {
        const riskContribution = components.feature_6_political
        const support = article.political_support
        const reason = support 
            ? `Current support: ${support.current_support}% | Required: ${support.required_support}% - ${support.current_support < support.required_support ? 'Insufficient' : 'Sufficient'} parliamentary majority`
            : 'Political support analysis indicates amendment feasibility challenges'
        features.push({
            id: 'F6',
            name: FEATURE_INFO.F6.name,
            icon: FEATURE_INFO.F6.icon,
            riskContribution,
            cumulativeRisk: cumulativeRisk + riskContribution,
            reason,
            color: FEATURE_INFO.F6.color,
            gradient: FEATURE_INFO.F6.gradient,
            details: support
        })
        cumulativeRisk += riskContribution
    }

    // Feature 7: Timeline
    if (components.feature_7_timeline !== null && components.feature_7_timeline !== undefined) {
        const riskContribution = components.feature_7_timeline
        const timeline = article.timeline
        const reason = timeline 
            ? `${timeline.months_needed} months needed vs ${timeline.months_available} available - ${timeline.feasible ? 'Feasible' : 'Not Feasible'} by ${timeline.target_year}`
            : 'Timeline analysis indicates amendment completion challenges'
        features.push({
            id: 'F7',
            name: FEATURE_INFO.F7.name,
            icon: FEATURE_INFO.F7.icon,
            riskContribution,
            cumulativeRisk: cumulativeRisk + riskContribution,
            reason,
            color: FEATURE_INFO.F7.color,
            gradient: FEATURE_INFO.F7.gradient,
            details: timeline
        })
        cumulativeRisk += riskContribution
    }

    // Feature 8: Priority
    if (components.feature_8_priority !== null && components.feature_8_priority !== undefined) {
        const priority = components.feature_8_priority
        const reason = `Ranked #${priority} priority based on risk score (${final_risk.toFixed(1)}/100) and impact analysis`
        features.push({
            id: 'F8',
            name: FEATURE_INFO.F8.name,
            icon: FEATURE_INFO.F8.icon,
            riskContribution: 0, // Priority doesn't add risk, it ranks
            cumulativeRisk,
            reason,
            color: FEATURE_INFO.F8.color,
            gradient: FEATURE_INFO.F8.gradient,
            details: {
                priorityRank: priority
            }
        })
    }

    // Prepare chart data
    const barChartData = [
        { name: 'Base Risk', value: base_risk, type: 'Base' },
        ...features.filter(f => f.riskContribution !== 0).map(f => ({
            name: f.name,
            value: f.riskContribution,
            type: 'Feature'
        }))
    ]

    const waterfallData = [
        { name: 'Base', value: base_risk, cumulative: base_risk }
    ]
    let runningTotal = base_risk
    features.forEach(f => {
        if (f.riskContribution !== 0) {
            runningTotal += f.riskContribution
            waterfallData.push({
                name: f.name,
                value: f.riskContribution,
                cumulative: runningTotal
            })
        }
    })
    waterfallData.push({ name: 'Final', value: final_risk, cumulative: final_risk })

    const pieData = features
        .filter(f => f.riskContribution > 0)
        .map(f => ({
            name: f.name,
            value: Math.abs(f.riskContribution)
        }))

    const radarData = features
        .filter(f => f.riskContribution !== 0)
        .map(f => ({
            feature: f.name,
            contribution: Math.abs(f.riskContribution),
            fullMark: 20
        }))

    const COLORS = ['#667eea', '#11998e', '#f093fb', '#fa709a', '#4facfe', '#43e97b', '#ff0844', '#fee140']

    return (
        <div className="feature-breakdown">
            <div className="breakdown-header">
                <h3 className="breakdown-title">
                    <span className="title-icon">🔬</span>
                    Feature Risk Breakdown Analysis
                </h3>
                <div className="view-toggle">
                    <button
                        className={`toggle-btn ${selectedView === 'breakdown' ? 'active' : ''}`}
                        onClick={() => setSelectedView('breakdown')}
                    >
                        Breakdown
                    </button>
                    <button
                        className={`toggle-btn ${selectedView === 'waterfall' ? 'active' : ''}`}
                        onClick={() => setSelectedView('waterfall')}
                    >
                        Waterfall
                    </button>
                    <button
                        className={`toggle-btn ${selectedView === 'radar' ? 'active' : ''}`}
                        onClick={() => setSelectedView('radar')}
                    >
                        Radar
                    </button>
                </div>
            </div>

            {/* Risk Summary Cards */}
            <div className="risk-summary">
                <div className="summary-card holographic">
                    <div className="summary-label">Base Risk</div>
                    <div className="summary-value">{base_risk.toFixed(1)}</div>
                </div>
                <div className="summary-card holographic">
                    <div className="summary-label">Feature Contributions</div>
                    <div className="summary-value">
                        +{features.reduce((sum, f) => sum + (f.riskContribution || 0), 0).toFixed(1)}
                    </div>
                </div>
                <div className="summary-card holographic critical">
                    <div className="summary-label">Final Risk Score</div>
                    <div className="summary-value">{final_risk.toFixed(1)}</div>
                </div>
            </div>

            {/* Chart Views */}
            {selectedView === 'breakdown' && (
                <motion.div
                    className="chart-view"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <div className="chart-card holographic">
                        <h4 className="chart-title">Risk Contribution by Feature</h4>
                        <ResponsiveContainer width="100%" height={300}>
                            <BarChart data={barChartData}>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                <XAxis 
                                    dataKey="name" 
                                    stroke="#a0aec0"
                                    angle={-45}
                                    textAnchor="end"
                                    height={100}
                                />
                                <YAxis stroke="#a0aec0" />
                                <Tooltip
                                    contentStyle={{
                                        background: 'rgba(10, 14, 26, 0.95)',
                                        border: '1px solid rgba(102, 126, 234, 0.5)',
                                        borderRadius: '8px',
                                        color: '#fff'
                                    }}
                                />
                                <Bar dataKey="value" fill="#667eea" radius={[8, 8, 0, 0]}>
                                    {barChartData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={entry.type === 'Base' ? '#4a5568' : COLORS[index % COLORS.length]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>

                    <div className="chart-card holographic">
                        <h4 className="chart-title">Feature Contribution Distribution</h4>
                        <ResponsiveContainer width="100%" height={300}>
                            <PieChart>
                                <Pie
                                    data={pieData}
                                    cx="50%"
                                    cy="50%"
                                    labelLine={false}
                                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                                    outerRadius={100}
                                    fill="#8884d8"
                                    dataKey="value"
                                >
                                    {pieData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{
                                        background: 'rgba(10, 14, 26, 0.95)',
                                        border: '1px solid rgba(102, 126, 234, 0.5)',
                                        borderRadius: '8px',
                                        color: '#fff'
                                    }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>
            )}

            {selectedView === 'waterfall' && (
                <motion.div
                    className="chart-view"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <div className="chart-card holographic">
                        <h4 className="chart-title">Risk Accumulation Waterfall</h4>
                        <ResponsiveContainer width="100%" height={400}>
                            <BarChart data={waterfallData} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                                <XAxis type="number" stroke="#a0aec0" />
                                <YAxis dataKey="name" type="category" stroke="#a0aec0" width={150} />
                                <Tooltip
                                    contentStyle={{
                                        background: 'rgba(10, 14, 26, 0.95)',
                                        border: '1px solid rgba(102, 126, 234, 0.5)',
                                        borderRadius: '8px',
                                        color: '#fff'
                                    }}
                                />
                                <Bar dataKey="cumulative" fill="#667eea" radius={[0, 8, 8, 0]}>
                                    {waterfallData.map((entry, index) => (
                                        <Cell 
                                            key={`cell-${index}`} 
                                            fill={
                                                index === 0 ? '#4a5568' : 
                                                index === waterfallData.length - 1 ? '#ff0844' : 
                                                COLORS[(index - 1) % COLORS.length]
                                            } 
                                        />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>
            )}

            {selectedView === 'radar' && (
                <motion.div
                    className="chart-view"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <div className="chart-card holographic">
                        <h4 className="chart-title">Feature Impact Radar</h4>
                        <ResponsiveContainer width="100%" height={400}>
                            <RadarChart data={radarData}>
                                <PolarGrid stroke="rgba(255,255,255,0.2)" />
                                <PolarAngleAxis dataKey="feature" stroke="#a0aec0" />
                                <PolarRadiusAxis angle={90} domain={[0, 20]} stroke="#a0aec0" />
                                <Radar
                                    name="Risk Contribution"
                                    dataKey="contribution"
                                    stroke="#667eea"
                                    fill="#667eea"
                                    fillOpacity={0.6}
                                />
                                <Tooltip
                                    contentStyle={{
                                        background: 'rgba(10, 14, 26, 0.95)',
                                        border: '1px solid rgba(102, 126, 234, 0.5)',
                                        borderRadius: '8px',
                                        color: '#fff'
                                    }}
                                />
                            </RadarChart>
                        </ResponsiveContainer>
                    </div>
                </motion.div>
            )}

            {/* Feature Details List */}
            <div className="features-list">
                <h4 className="list-title">Detailed Feature Analysis</h4>
                {features.map((feature, index) => (
                    <motion.div
                        key={feature.id}
                        className="feature-card holographic"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                    >
                        <div className="feature-header">
                            <div className="feature-icon-wrapper" style={{ background: feature.gradient }}>
                                <span className="feature-icon">{feature.icon}</span>
                            </div>
                            <div className="feature-title-section">
                                <h5 className="feature-name">{feature.name}</h5>
                                <div className="feature-meta">
                                    <span className="feature-id">{feature.id}</span>
                                    {feature.riskContribution !== 0 && (
                                        <span className={`risk-badge ${feature.riskContribution > 0 ? 'positive' : 'negative'}`}>
                                            {feature.riskContribution > 0 ? '+' : ''}{feature.riskContribution.toFixed(1)} pts
                                        </span>
                                    )}
                                </div>
                            </div>
                        </div>
                        <div className="feature-body">
                            <p className="feature-reason">{feature.reason}</p>
                            {feature.details && (
                                <div className="feature-details">
                                    {feature.id === 'F1' && feature.details && (
                                        <div className="detail-section">
                                            <strong>Court Argument:</strong>
                                            <p>{feature.details.court}</p>
                                        </div>
                                    )}
                                    {feature.id === 'F2' && feature.details && (
                                        <div className="detail-section">
                                            <strong>Evidence Documents:</strong>
                                            <p>{feature.details.evidenceCount} document(s) retrieved</p>
                                        </div>
                                    )}
                                    {feature.id === 'F3' && feature.details && (
                                        <div className="detail-section">
                                            <strong>Relevant Cases:</strong>
                                            <p>{feature.details.precedents.length} precedent(s) found</p>
                                        </div>
                                    )}
                                    {feature.id === 'F4' && feature.details && (
                                        <div className="detail-section">
                                            <strong>Simulation Results:</strong>
                                            <p>Mean: {(feature.details.mean || 0).toFixed(1)}, CI: [{(feature.details.confidence_interval_95?.[0] || 0).toFixed(1)}, {(feature.details.confidence_interval_95?.[1] || 0).toFixed(1)}]</p>
                                        </div>
                                    )}
                                    {feature.id === 'F6' && feature.details && (
                                        <div className="detail-section">
                                            <strong>Political Support:</strong>
                                            <p>{feature.details.current_support}% current vs {feature.details.required_support}% required</p>
                                        </div>
                                    )}
                                    {feature.id === 'F7' && feature.details && (
                                        <div className="detail-section">
                                            <strong>Timeline:</strong>
                                            <p>{feature.details.months_needed} months needed, {feature.details.feasible ? 'Feasible' : 'Not Feasible'}</p>
                                        </div>
                                    )}
                                </div>
                            )}
                        </div>
                        <div className="feature-footer">
                            <div className="cumulative-indicator">
                                <span className="cumulative-label">Cumulative Risk:</span>
                                <span className="cumulative-value">{feature.cumulativeRisk.toFixed(1)}</span>
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>
        </div>
    )
}

export default FeatureBreakdown

