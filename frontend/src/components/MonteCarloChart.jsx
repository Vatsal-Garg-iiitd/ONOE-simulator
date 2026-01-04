import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import './MonteCarloChart.css'

function MonteCarloChart({ monteCarloData }) {
    if (!monteCarloData) return null

    const { mean, std_dev, confidence_interval_95 } = monteCarloData

    // Generate distribution data for visualization
    const generateDistribution = () => {
        const data = []
        const points = 50
        const min = confidence_interval_95[0]
        const max = confidence_interval_95[1]
        const step = (max - min) / points

        for (let i = 0; i <= points; i++) {
            const x = min + (i * step)
            // Approximate normal distribution
            const z = (x - mean) / std_dev
            const y = Math.exp(-0.5 * z * z) / (std_dev * Math.sqrt(2 * Math.PI))
            data.push({ risk: x.toFixed(1), probability: y * 100 })
        }
        return data
    }

    const data = generateDistribution()

    return (
        <div className="monte-carlo-chart">
            <h4 className="chart-title">📊 Monte Carlo Confidence Analysis</h4>

            <div className="chart-stats">
                <div className="stat-item">
                    <span className="stat-label">Mean Risk</span>
                    <span className="stat-value">{mean.toFixed(2)}</span>
                </div>
                <div className="stat-item">
                    <span className="stat-label">Std Deviation</span>
                    <span className="stat-value">±{std_dev.toFixed(2)}</span>
                </div>
                <div className="stat-item">
                    <span className="stat-label">95% CI</span>
                    <span className="stat-value">
                        [{confidence_interval_95[0].toFixed(1)}, {confidence_interval_95[1].toFixed(1)}]
                    </span>
                </div>
            </div>

            <div className="chart-container">
                <ResponsiveContainer width="100%" height={250}>
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorProbability" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#667eea" stopOpacity={0.8} />
                                <stop offset="95%" stopColor="#764ba2" stopOpacity={0.1} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                        <XAxis
                            dataKey="risk"
                            stroke="#a0aec0"
                            label={{ value: 'Risk Score', position: 'insideBottom', offset: -5, fill: '#a0aec0' }}
                        />
                        <YAxis
                            stroke="#a0aec0"
                            label={{ value: 'Probability Density', angle: -90, position: 'insideLeft', fill: '#a0aec0' }}
                        />
                        <Tooltip
                            contentStyle={{
                                background: 'rgba(26, 32, 48, 0.95)',
                                border: '1px solid rgba(255,255,255,0.1)',
                                borderRadius: '8px'
                            }}
                        />
                        <Area
                            type="monotone"
                            dataKey="probability"
                            stroke="#667eea"
                            strokeWidth={2}
                            fillOpacity={1}
                            fill="url(#colorProbability)"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            <p className="chart-description">
                Based on {monteCarloData.trials.toLocaleString()} simulations varying court challenge probability,
                state disruption, and political support factors.
            </p>
        </div>
    )
}

export default MonteCarloChart
