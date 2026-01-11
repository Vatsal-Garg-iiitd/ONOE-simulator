import { useState } from 'react';
import { motion } from 'framer-motion';

function AdminConfigPanel({ onUpdate, isLoading }) {
    const [inputs, setInputs] = useState({
        target_year: 2029,
        evm_supply: 100,
        security_personnel: 100
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setInputs(prev => ({
            ...prev,
            [name]: parseFloat(value)
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onUpdate(inputs);
    };

    return (
        <motion.div
            className="glass-card config-panel"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            style={{ marginBottom: '2rem', padding: '1.5rem' }}
        >
            <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '2rem', alignItems: 'flex-end', flexWrap: 'wrap' }}>
                <div className="input-group">
                    <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--color-text-secondary)' }}>Target Year</label>
                    <input
                        type="number"
                        name="target_year"
                        value={inputs.target_year}
                        onChange={handleChange}
                        min="2025"
                        max="2035"
                        style={{
                            background: 'rgba(255,255,255,0.1)',
                            border: '1px solid rgba(255,255,255,0.2)',
                            padding: '0.5rem',
                            color: 'white',
                            borderRadius: '4px',
                            width: '120px'
                        }}
                    />
                </div>

                <div className="input-group">
                    <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--color-text-secondary)' }}>EVM Supply (%)</label>
                    <input
                        type="range"
                        name="evm_supply"
                        value={inputs.evm_supply}
                        onChange={handleChange}
                        min="50"
                        max="100"
                        style={{ width: '150px', accentColor: 'var(--color-accent-blue)' }}
                    />
                    <span style={{ marginLeft: '10px', color: 'var(--color-text-primary)' }}>{inputs.evm_supply}%</span>
                </div>

                <div className="input-group">
                    <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--color-text-secondary)' }}>Security Personnel (%)</label>
                    <input
                        type="range"
                        name="security_personnel"
                        value={inputs.security_personnel}
                        onChange={handleChange}
                        min="50"
                        max="100"
                        style={{ width: '150px', accentColor: 'var(--color-accent-blue)' }}
                    />
                    <span style={{ marginLeft: '10px', color: 'var(--color-text-primary)' }}>{inputs.security_personnel}%</span>
                </div>

                <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={isLoading}
                    style={{ marginLeft: 'auto' }}
                >
                    {isLoading ? 'Updating...' : 'Update Simulation'}
                </button>
            </form>
        </motion.div>
    );
}

export default AdminConfigPanel;
