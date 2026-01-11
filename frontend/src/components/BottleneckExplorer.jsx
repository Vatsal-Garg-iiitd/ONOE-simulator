import React from 'react';
import './BottleneckExplorer.css'; // We'll assume basic styling or inline it

function BottleneckExplorer({ sliders, onUpdateImpact }) {
    if (!sliders) return null;

    const handleSliderChange = (e, sliderId) => {
        const newValue = parseFloat(e.target.value);
        // Create updated slider values map based on current state (needs to be managed by parent)
        // For now, we will just call the update function with the specific change
        // The parent (AdminDashboard) should maintain the full state of all sliders
        onUpdateImpact(sliderId, newValue);
    };

    return (
        <div className="bottleneck-explorer glass-card">
            <h3 className="section-title">Bottleneck Explorer (Interactive)</h3>
            <div className="sliders-container">
                {sliders.map(slider => (
                    <div key={slider.id} className="slider-item">
                        <div className="slider-header">
                            <label>{slider.label}</label>
                            <span className="slider-value">
                                {slider.currentValue} {slider.unit}
                            </span>
                        </div>
                        <input
                            type="range"
                            min={slider.min}
                            max={slider.max}
                            value={slider.currentValue}
                            onChange={(e) => handleSliderChange(e, slider.id)}
                            className="explorer-slider"
                        />
                        <div className="risk-impact-indicator">
                            Impact: {slider.currentValue < slider.defaultValue ? "High Risk" : "Stable"}
                        </div>
                    </div>
                ))}
            </div>
            <div className="explorer-actions">
                <button className="btn btn-secondary">Reset Sliders</button>
                <button className="btn btn-primary">Save Scenario</button>
            </div>
        </div>
    );
}

export default BottleneckExplorer;
