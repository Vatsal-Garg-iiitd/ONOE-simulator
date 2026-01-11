import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';
import axios from 'axios';
import BottleneckExplorer from '../components/BottleneckExplorer';
import ResourceDebateView from '../components/ResourceDebateView';
import './AdminDashboard.css';

const API_BASE = 'http://localhost:8000';

function AdminDashboard() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [sliders, setSliders] = useState([]);
    const [selectedFeature, setSelectedFeature] = useState(null);

    useEffect(() => {
        fetchDashboard();
    }, []);

    const fetchDashboard = async () => {
        try {
            const response = await axios.get(`${API_BASE}/api/admin/dashboard`);
            setData(response.data);

            const backendSliders = response.data.bottleneck_sliders.map(s => ({
                ...s,
                currentValue: s.defaultValue
            }));
            setSliders(backendSliders);

            setLoading(false);
        } catch (error) {
            console.error("Failed to load admin dashboard", error);
            setLoading(false);
        }
    };

    const handleImpactUpdate = async (sliderId, newValue) => {
        const updatedSliders = sliders.map(s =>
            s.id === sliderId ? { ...s, currentValue: newValue } : s
        );
        setSliders(updatedSliders);

        try {
            const payload = updatedSliders.reduce((acc, s) => {
                acc[s.id] = s.currentValue;
                return acc;
            }, {});

            const response = await axios.post(`${API_BASE}/api/admin/impact`, { sliders: payload });
            console.log("New Risk Impact:", response.data);
        } catch (error) {
            console.error("Error calculating impact", error);
        }
    };

    if (loading) return <div className="loading-screen">Loading Administrative Engine...</div>;
    if (!data) return <div className="error-screen">Failed to load data</div>;

    return (
        <div className="admin-dashboard">
            <header className="dashboard-header">
                <div className="header-content">
                    <Link to="/" className="back-link">← Back to Dashboard</Link>
                    <h1>🏗️ ADMINISTRATIVE ENGINE <span className="highlight-text">DETAILED ANALYSIS</span></h1>
                    <nav className="admin-nav">
                        <button className="nav-btn active">Features</button>
                        <button className="nav-btn">Bottleneck Explorer</button>
                        <button className="nav-btn">Stakeholder Readiness</button>
                        <button className="nav-btn">Timeline</button>
                    </nav>
                </div>
            </header>

            <main className="container">
                {/* Features Grid */}
                <section className="features-grid">
                    {data.features.map(feature => (
                        <motion.div
                            key={feature.id}
                            className="feature-card glass-card"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                        >
                            <div className="feature-header">
                                <h3>{feature.name}</h3>
                                <span className={`status-badge ${feature.status.toLowerCase().replace(' ', '-')}`}>
                                    {feature.status}
                                </span>
                            </div>
                            <p className="feature-desc">{feature.description}</p>
                            <div className="risk-metric">
                                <span className="label">Risk Contribution:</span>
                                <span className="value">{feature.risk_contribution.toFixed(1)}%</span>
                            </div>

                            {/* Feature Actions */}
                            {feature.id === 'f1' && (
                                <button
                                    className="action-btn"
                                    onClick={() => setSelectedFeature(feature)}
                                >
                                    View Debate Transcript
                                </button>
                            )}
                        </motion.div>
                    ))}
                </section>

                {/* Bottleneck Explorer */}
                <section className="bottleneck-section">
                    <BottleneckExplorer
                        sliders={sliders}
                        onUpdateImpact={handleImpactUpdate}
                    />
                </section>
            </main>

            <AnimatePresence>
                {selectedFeature && selectedFeature.id === 'f1' && (
                    <ResourceDebateView
                        data={selectedFeature.data}
                        onClose={() => setSelectedFeature(null)}
                    />
                )}
            </AnimatePresence>
        </div>
    );
}

export default AdminDashboard;
