import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './Home.css'; // We'll assume structure similar to App.css or create new

function Home() {
    return (
        <div className="home-container">
            <header className="hero-section">
                <h1 className="main-title">CONSTITUTIONAL <span className="highlight">ENGINE</span></h1>
                <p className="subtitle">One Nation One Election: Advanced Feasibility Analysis</p>
            </header>

            <div className="engine-selection">
                <Link to="/constitutional" className="engine-card">
                    <motion.div
                        className="card-content"
                        whileHover={{ scale: 1.05 }}
                    >
                        <div className="icon">🏛️</div>
                        <h2>Constitutional Engine</h2>
                        <p>Analyze legal frameworks, Article 356 implications, and historical precedents.</p>
                        <span className="btn-text">Launch Analysis →</span>
                    </motion.div>
                </Link>

                <Link to="/administrative" className="engine-card">
                    <motion.div
                        className="card-content"
                        whileHover={{ scale: 1.05 }}
                    >
                        <div className="icon">🏗️</div>
                        <h2>Administrative Engine</h2>
                        <p>Simulate logistics, supply chain bottlenecks, and stakeholder readiness.</p>
                        <span className="btn-text">Launch Simulation →</span>
                    </motion.div>
                </Link>
            </div>
        </div>
    );
}

export default Home;
