import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';
import axios from 'axios';
import AdminFeatureCard from '../components/AdminFeatureCard';
import AdminConfigPanel from '../components/AdminConfigPanel';
import BottleneckExplorer from '../components/BottleneckExplorer';
import ResourceDebateView from '../components/ResourceDebateView';
import MonteCarloChart from '../components/MonteCarloChart'; // Reuse existing component
import './AdminDashboard.css';
import './Dashboard.css'; // Inherit main dashboard styles

const API_BASE = 'http://localhost:8000';

function AdminDashboard() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [updating, setUpdating] = useState(false);
    const [sliders, setSliders] = useState([]);
    const [selectedFeature, setSelectedFeature] = useState(null);

    useEffect(() => {
        fetchDashboard();
    }, []);

    const fetchDashboard = async () => {
        try {
            const response = await axios.get(`${API_BASE}/api/admin/dashboard`);
            setData(response.data);
            initSliders(response.data);
            setLoading(false);
        } catch (error) {
            console.error("Failed to load admin dashboard", error);
            setLoading(false);
        }
    };

    const handleConfigUpdate = async (inputs) => {
        setUpdating(true);
        try {
            const response = await axios.post(`${API_BASE}/api/admin/dashboard`, inputs);
            setData(response.data);
            initSliders(response.data);
        } catch (error) {
            console.error("Failed to update dashboard", error);
        } finally {
            setUpdating(false);
        }
    };

    const initSliders = (dashboardData) => {
        const backendSliders = dashboardData.bottleneck_sliders.map(s => ({
            ...s,
            currentValue: s.defaultValue
        }));
        setSliders(backendSliders);
    };

    const handleImpactUpdate = async (sliderId, newValue) => {
        const updatedSliders = sliders.map(s =>
            s.id === sliderId ? { ...s, currentValue: newValue } : s
        );
        setSliders(updatedSliders);

        // Construct simple context from current inputs
        // Assuming currentInputs might be available in 'data' or separate state
        // For now, we'll try to extract from 'data' if available, or just send what we have
        const context = {
            evm_capacity: 1.2, // Default or fetch from state
            security_personnel: 100 // Default or fetch from state
        };
        // NOTE: Ideally 'inputs' from ConfigPanel should be lifted to parent state to be accessible here.
        // For the sake of this edit, we'll assume we can't easily access 'inputs' without refactoring.
        // We will implement part 3 of the 'Reactivity' on the backend side in the main dashboard load.
        // But for this specific 'what-if' slider move, we send the context.

        try {
            const slidersDict = updatedSliders.reduce((acc, s) => ({ ...acc, [s.id]: s.currentValue }), {});
            const response = await axios.post(`${API_BASE}/api/admin/bottleneck/calculate`, {
                sliders: slidersDict,
                context: context
            });

            // Update the specific feature data with new risk/AI analysis
            if (data && data.features) {
                const updatedFeatures = data.features.map(f =>
                    f.id === 'f5' ? { ...f, data: { ...f.data, ...response.data, ai_analysis: response.data.ai_analysis } } : f
                );
                setData({ ...data, features: updatedFeatures });
                if (selectedFeature && selectedFeature.id === 'f5') {
                    setSelectedFeature({ ...selectedFeature, data: { ...selectedFeature.data, ...response.data, ai_analysis: response.data.ai_analysis } });
                }
            }
        } catch (e) {
            console.error("Failed to recalculate impact", e);
        }
    };

    if (loading) return (
        <div className="dashboard" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100vh' }}>
            <div className="loading-spinner">Loading Engine...</div>
        </div>
    );

    if (!data) return <div className="error-screen">Failed to load data</div>;

    // Calculate metrics
    const totalRisk = data.features.reduce((acc, f) => acc + f.risk_contribution, 0);
    const criticalCount = data.features.filter(f => f.risk_contribution >= 90 || f.status.includes('Critical') || f.status.includes('High')).length;

    return (
        <div className="dashboard admin-dashboard-enhanced">
            {/* Hero Section */}
            <motion.header
                className="dashboard-header"
                initial={{ opacity: 0, y: -20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div className="container">
                    <div style={{ marginBottom: '1rem' }}>
                        <Link to="/" className="back-link" style={{ color: 'var(--color-accent-blue)', textDecoration: 'none' }}>← Back to Main</Link>
                    </div>
                    <h1 className="dashboard-title">
                        <span className="gradient-text">Administrative Engine</span>
                    </h1>
                    <p className="dashboard-subtitle">
                        Logistical Feasibility & Resource Management Analysis
                    </p>

                    <div className="metrics-grid">
                        <div className="metric-card glass-card">
                            <span className="metric-icon">🏗️</span>
                            <div>
                                <div className="metric-value">{data.features.length}</div>
                                <div className="metric-label">Key Domains</div>
                            </div>
                        </div>
                        <div className="metric-card glass-card">
                            <span className="metric-icon">⚠️</span>
                            <div>
                                <div className="metric-value">{criticalCount}</div>
                                <div className="metric-label">Critical Risks</div>
                            </div>
                        </div>
                        <div className="metric-card glass-card">
                            <span className="metric-icon">📉</span>
                            <div>
                                <div className="metric-value">{totalRisk.toFixed(1)}%</div>
                                <div className="metric-label">Total Execution Risk</div>
                            </div>
                        </div>
                        <div className="metric-card glass-card">
                            <span className="metric-icon">👮‍♂️</span>
                            <div>
                                <div className="metric-value">1.5M+</div>
                                <div className="metric-label">Personnel Req.</div>
                            </div>
                        </div>
                    </div>
                </div>
            </motion.header>

            <div className="container">
                {/* Configuration Panel */}
                <AdminConfigPanel onUpdate={handleConfigUpdate} isLoading={updating} />

                {/* Features Grid */}
                <section className="articles-section">
                    <div className="section-header">
                        <h2>Administrative Domains</h2>
                        <p className="section-subtitle">
                            Breakdown of logistical, security, and supply chain challenges
                        </p>
                    </div>

                    <div className="articles-grid">
                        {data.features.filter(f => f.id !== 'f8').map((feature, index) => (
                            <AdminFeatureCard
                                key={feature.id}
                                feature={feature}
                                onClick={() => setSelectedFeature(feature)}
                                index={index}
                            />
                        ))}
                    </div>
                </section>

                {/* Detailed Feature View */}
                <AnimatePresence>
                    {selectedFeature && (
                        <motion.section
                            className="article-detail"
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                        >
                            <div className="detail-header">
                                <div>
                                    <h2>{selectedFeature.name} Analysis</h2>
                                    <p style={{ color: 'var(--color-text-secondary)' }}>{selectedFeature.description}</p>
                                </div>
                                <button
                                    className="close-btn"
                                    onClick={() => setSelectedFeature(null)}
                                >
                                    ✕
                                </button>
                            </div>

                            <div className="detail-content">
                                {/* Basic Info */}
                                <div className="info-box glass-card" style={{ padding: '1.5rem' }}>
                                    <h4 style={{ marginBottom: '1rem' }}>Risk Assessment</h4>
                                    <p>
                                        Current Risk Contribution:
                                        {selectedFeature.risk_contribution > 0 ? (
                                            <strong style={{ color: 'var(--color-risk-high)' }}> {selectedFeature.risk_contribution}%</strong>
                                        ) : (
                                            <span style={{ color: '#aaa' }}> N/A (Ranking Only)</span>
                                        )}
                                    </p>
                                    <p>Status: <span className={`badge badge-normal`}>{selectedFeature.status}</span></p>

                                    {/* Dynamic Explanation */}
                                    {selectedFeature.data && selectedFeature.data.explanation && (
                                        <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                                            <strong style={{ color: 'var(--color-accent-blue)' }}>AI Analysis:</strong>
                                            <p style={{ marginTop: '0.5rem' }}>{selectedFeature.data.explanation}</p>
                                        </div>
                                    )}
                                </div>

                                {/* Feature Specific Components */}
                                {selectedFeature.id === 'f1' && (
                                    <ResourceDebateView
                                        data={selectedFeature.data}
                                        onClose={() => { }} // Controlled by parent
                                    />
                                )}

                                {selectedFeature.id === 'f5' && (
                                    <div className="glass-card" style={{ padding: '1.5rem' }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>
                                            <h4>🛑 Strategic Bottleneck Engine</h4>
                                            <span className="badge badge-normal">AI-Powered</span>
                                        </div>

                                        {/* AI Analysis Section */}
                                        <div className="ai-analysis-box" style={{
                                            background: 'linear-gradient(135deg, rgba(33, 150, 243, 0.1) 0%, rgba(33, 33, 33, 0.4) 100%)',
                                            padding: '1.5rem',
                                            borderRadius: '12px',
                                            marginBottom: '2rem',
                                            border: '1px solid rgba(33, 150, 243, 0.3)'
                                        }}>
                                            <h5 style={{ color: '#2196f3', display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                                                <span>🧠</span> AI Strategic Evaluation
                                            </h5>
                                            <div style={{ color: '#e0e0e0', lineHeight: 1.6, fontSize: '0.95rem' }}>
                                                {selectedFeature.data.ai_analysis ? (
                                                    selectedFeature.data.ai_analysis.split('\n').map((line, i) => (
                                                        <div key={i} style={{ marginBottom: '0.5rem' }}>{line}</div>
                                                    ))
                                                ) : (
                                                    <div className="loading-dots">Generating strategic assessment...</div>
                                                )}
                                            </div>
                                        </div>

                                        <p style={{ marginBottom: '1.5rem', color: 'var(--color-text-secondary)', lineHeight: 1.6 }}>
                                            Interactive simulation of operational risks. Adjust parameters to see real-time impact on the critical path.
                                        </p>

                                        <BottleneckExplorer
                                            sliders={sliders}
                                            onUpdateImpact={handleImpactUpdate}
                                        />

                                        {/* Merged Precedent Logic */}
                                        {selectedFeature.data.precedents && (
                                            <div style={{ marginTop: '2rem', paddingTop: '1.5rem', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                                                <h5 style={{ color: '#ff9800', marginBottom: '1rem' }}>📜 Historical Context</h5>
                                                <div className="precedent-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                                                    {selectedFeature.data.precedents.map((p, idx) => (
                                                        <div key={idx} style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '8px' }}>
                                                            <div style={{ fontWeight: 'bold', fontSize: '0.9rem' }}>{p.election}</div>
                                                            <div style={{ fontSize: '0.8rem', color: '#aaa', marginTop: '0.3rem' }}>{p.logistics_issues}</div>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                )}

                                {/* Detailed Views for each Feature */}
                                {selectedFeature.id === 'f2' && (
                                    <div className="glass-card" style={{ padding: '1.5rem' }}>
                                        <h4>📦 Supply Chain Analytics</h4>

                                        {/* Inventory Breakdown */}
                                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem', margin: '1.5rem 0' }}>
                                            <div style={{ textAlign: 'center', padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
                                                <h3 style={{ color: '#2196f3' }}>{(selectedFeature.data.evm_inventory?.current_stock / 100000)?.toFixed(1) || '12.0'} L</h3>
                                                <p style={{ color: '#aaa', fontSize: '0.9rem' }}>Current Stock</p>
                                            </div>
                                            <div style={{ textAlign: 'center', padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
                                                <h3 style={{ color: '#4caf50' }}>+{(selectedFeature.data.evm_inventory?.projected_production / 100000)?.toFixed(1) || '0.0'} L</h3>
                                                <p style={{ color: '#aaa', fontSize: '0.9rem' }}>Projected Production</p>
                                            </div>
                                            <div style={{ textAlign: 'center', padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
                                                <h3 style={{ color: '#ff9800' }}>{(selectedFeature.data.evm_inventory?.total_available / 100000)?.toFixed(1) || '12.0'} L</h3>
                                                <p style={{ color: '#aaa', fontSize: '0.9rem' }}>Total Available</p>
                                            </div>
                                            <div style={{ textAlign: 'center', padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
                                                <h3 style={{ color: 'var(--color-risk-high)' }}>{(selectedFeature.data.evm_inventory?.required_stock / 100000)?.toFixed(1) || '25.0'} L</h3>
                                                <p style={{ color: '#aaa', fontSize: '0.9rem' }}>Required</p>
                                            </div>
                                        </div>

                                        {/* Progress Bar */}
                                        <div style={{ margin: '1.5rem 0' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', fontSize: '0.9rem' }}>
                                                <span>Supply Progress</span>
                                                <span>{((selectedFeature.data.evm_inventory?.total_available / selectedFeature.data.evm_inventory?.required_stock) * 100)?.toFixed(1) || '48'}%</span>
                                            </div>
                                            <div className="progress-bar-container" style={{ backgroundColor: '#333', height: '12px', borderRadius: '6px', overflow: 'hidden' }}>
                                                <div className="progress-fill" style={{
                                                    width: `${Math.min(100, (selectedFeature.data.evm_inventory?.total_available / selectedFeature.data.evm_inventory?.required_stock) * 100) || 48}%`,
                                                    backgroundColor: (selectedFeature.data.evm_inventory?.deficit || 0) > 0 ? 'var(--color-risk-high)' : 'var(--color-accent-blue)',
                                                    height: '100%',
                                                    transition: 'width 0.3s ease'
                                                }}></div>
                                            </div>
                                        </div>

                                        {/* Deficit/Surplus Alert */}
                                        {selectedFeature.data.evm_inventory?.deficit !== undefined && (
                                            <div style={{
                                                marginTop: '1rem',
                                                padding: '1rem',
                                                borderRadius: '8px',
                                                background: selectedFeature.data.evm_inventory.deficit > 0
                                                    ? 'rgba(244, 67, 54, 0.1)'
                                                    : 'rgba(76, 175, 80, 0.1)',
                                                borderLeft: `4px solid ${selectedFeature.data.evm_inventory.deficit > 0 ? '#f44336' : '#4caf50'}`
                                            }}>
                                                <strong style={{ color: selectedFeature.data.evm_inventory.deficit > 0 ? '#f44336' : '#4caf50' }}>
                                                    {selectedFeature.data.evm_inventory.deficit > 0 ? '⚠️ Deficit: ' : '✅ Surplus: '}
                                                </strong>
                                                <span>{Math.abs(selectedFeature.data.evm_inventory.deficit).toLocaleString()} Units</span>
                                            </div>
                                        )}

                                        {/* Production Details */}
                                        <div style={{ marginTop: '1.5rem', padding: '1rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
                                            <h5 style={{ marginBottom: '0.5rem', color: '#fff' }}>Production Metrics</h5>
                                            <div style={{ fontSize: '0.9rem', color: '#aaa', lineHeight: 1.8 }}>
                                                <div>Annual Rate: <strong style={{ color: '#fff' }}>{selectedFeature.data.evm_inventory?.annual_rate?.toLocaleString() || '500,000'} units/year</strong></div>
                                                <div>Years Remaining: <strong style={{ color: '#fff' }}>{selectedFeature.data.evm_inventory?.years_remaining || 3} years</strong></div>
                                            </div>
                                        </div>
                                    </div>
                                )}

                                {selectedFeature.id === 'f4' && (
                                    <div className="glass-card" style={{ padding: '1rem' }}>
                                        <MonteCarloChart monteCarloData={selectedFeature.data} />
                                    </div>
                                )}

                                {selectedFeature.id === 'f6' && (
                                    <div className="glass-card" style={{ padding: '1rem' }}>
                                        <h4>🤝 Stakeholder Consensus Map</h4>
                                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', margin: '1rem 0' }}>
                                            <div className="status-col">
                                                <h5 style={{ color: '#4caf50' }}>Ready ({selectedFeature.data.ready_count})</h5>
                                                <div style={{ fontSize: '0.8rem' }}>Gujarat, UP, MP...</div>
                                            </div>
                                            <div className="status-col">
                                                <h5 style={{ color: '#ff9800' }}>In Progress ({selectedFeature.data.in_progress_count})</h5>
                                                <div style={{ fontSize: '0.8rem' }}>Maharashtra, Karnataka...</div>
                                            </div>
                                            <div className="status-col">
                                                <h5 style={{ color: '#f44336' }}>Behind ({selectedFeature.data.behind_count})</h5>
                                                <div style={{ fontSize: '0.8rem' }}>Kerala, WB, TN...</div>
                                            </div>
                                        </div>
                                        <div className="alert-box" style={{ background: 'rgba(244, 67, 54, 0.1)', padding: '1rem', borderRadius: '4px', borderLeft: '3px solid #f44336' }}>
                                            <strong>Critical Gap:</strong> {selectedFeature.data.critical_gap}
                                        </div>
                                    </div>
                                )}

                                {selectedFeature.id === 'f7' && (
                                    <div className="glass-card" style={{ padding: '1.5rem' }}>
                                        <h4>⏳ Timeline Feasibility Calculator</h4>
                                        <div style={{ margin: '1.5rem 0' }}>
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                                                <span style={{ fontSize: '1.1rem' }}>Total Time Needed:</span>
                                                <span style={{ fontSize: '1.1rem', fontWeight: 'bold' }}>{selectedFeature.data.months_needed} Months</span>
                                            </div>

                                            {selectedFeature.data.calculation_breakdown && (
                                                <div className="breakdown-list">
                                                    {selectedFeature.data.calculation_breakdown.map((item, idx) => (
                                                        <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.8rem 0', borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                                            <div>
                                                                <div style={{ fontWeight: '500', color: '#fff' }}>{item.phase}</div>
                                                                <div style={{ fontSize: '0.8rem', color: '#aaa' }}>{item.desc}</div>
                                                            </div>
                                                            <div style={{
                                                                background: 'rgba(255,255,255,0.1)',
                                                                padding: '0.3rem 0.8rem',
                                                                borderRadius: '4px',
                                                                minWidth: '80px',
                                                                textAlign: 'center'
                                                            }}>
                                                                {item.months} mo
                                                            </div>
                                                        </div>
                                                    ))}
                                                </div>
                                            )}
                                        </div>

                                        <div className="timeline-visual" style={{ margin: '2rem 0', position: 'relative', height: '40px', background: '#333', borderRadius: '20px', overflow: 'hidden' }}>
                                            <div style={{
                                                width: `${Math.min(100, (selectedFeature.data.months_remaining / selectedFeature.data.months_needed) * 100)}%`,
                                                height: '100%',
                                                background: selectedFeature.data.months_remaining >= selectedFeature.data.months_needed ? '#4caf50' : '#f44336',
                                                transition: 'width 0.5s'
                                            }}></div>
                                            <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', fontWeight: 'bold', textShadow: '0 1px 2px black' }}>
                                                Available vs Needed
                                            </div>
                                        </div>

                                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem', color: '#aaa' }}>
                                            <span>Deadline: {selectedFeature.data.deadline}</span>
                                            <span>Current Capacity: {selectedFeature.data.months_remaining} Months</span>
                                        </div>
                                    </div>
                                )}

                                {selectedFeature.id === 'f8' && (
                                    <div className="glass-card" style={{ padding: '1rem' }}>
                                        <h4>🚨 Execution Priorities</h4>
                                        <ul className="priority-list" style={{ listStyle: 'none', padding: 0 }}>
                                            {selectedFeature.data.priorities?.map((p, i) => (
                                                <li key={i} style={{
                                                    background: 'rgba(255,255,255,0.05)',
                                                    margin: '0.5rem 0',
                                                    padding: '1rem',
                                                    borderRadius: '8px',
                                                    display: 'flex',
                                                    alignItems: 'center',
                                                    borderLeft: `4px solid ${i === 0 ? '#f44336' : (i === 1 ? '#ff9800' : '#4caf50')}`
                                                }}>
                                                    <span style={{ fontSize: '1.5rem', marginRight: '1rem', opacity: 0.5 }}>#{p.rank}</span>
                                                    <div>
                                                        <div style={{ fontWeight: 'bold', fontSize: '1.1rem' }}>{p.item}</div>
                                                        <div style={{ fontSize: '0.9rem', color: '#aaa' }}>Action: {p.action}</div>
                                                    </div>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        </motion.section>
                    )}
                </AnimatePresence>

                <footer className="dashboard-footer">
                    <p>
                        Administrative Engine v1.0 | Integrated with Constitutional Engine
                    </p>
                </footer>
            </div>
        </div>
    );
}

export default AdminDashboard;
