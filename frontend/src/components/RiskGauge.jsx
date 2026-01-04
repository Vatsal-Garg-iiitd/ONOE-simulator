import { motion } from 'framer-motion'
import './RiskGauge.css'

function RiskGauge({ risk, size = 120 }) {
    const radius = size / 2 - 10
    const circumference = 2 * Math.PI * radius
    const offset = circumference - (risk / 100) * circumference

    // Determine color based on risk level
    let color, gradient
    if (risk >= 80) {
        color = '#ff0844'
        gradient = 'url(#gradient-critical)'
    } else if (risk >= 60) {
        color = '#f5576c'
        gradient = 'url(#gradient-high)'
    } else if (risk >= 30) {
        color = '#f5af19'
        gradient = 'url(#gradient-warning)'
    } else {
        color = '#38ef7d'
        gradient = 'url(#gradient-success)'
    }

    return (
        <div className="risk-gauge" style={{ width: size, height: size }}>
            <svg width={size} height={size}>
                <defs>
                    <linearGradient id="gradient-critical" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#ff0844" />
                        <stop offset="100%" stopColor="#ffb199" />
                    </linearGradient>
                    <linearGradient id="gradient-high" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#fa709a" />
                        <stop offset="100%" stopColor="#fee140" />
                    </linearGradient>
                    <linearGradient id="gradient-warning" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#f093fb" />
                        <stop offset="100%" stopColor="#f5576c" />
                    </linearGradient>
                    <linearGradient id="gradient-success" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#11998e" />
                        <stop offset="100%" stopColor="#38ef7d" />
                    </linearGradient>
                </defs>

                {/* Background circle */}
                <circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    fill="none"
                    stroke="rgba(255, 255, 255, 0.1)"
                    strokeWidth="8"
                />

                {/* Progress circle */}
                <motion.circle
                    cx={size / 2}
                    cy={size / 2}
                    r={radius}
                    fill="none"
                    stroke={gradient}
                    strokeWidth="8"
                    strokeLinecap="round"
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                    transform={`rotate(-90 ${size / 2} ${size / 2})`}
                    initial={{ strokeDashoffset: circumference }}
                    animate={{ strokeDashoffset: offset }}
                    transition={{ duration: 1.5, ease: "easeOut" }}
                />
            </svg>

            <div className="risk-gauge-value">
                <motion.span
                    className="risk-number"
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.5, duration: 0.5 }}
                >
                    {risk.toFixed(1)}
                </motion.span>
                <span className="risk-label">/100</span>
            </div>
        </div>
    )
}

export default RiskGauge
