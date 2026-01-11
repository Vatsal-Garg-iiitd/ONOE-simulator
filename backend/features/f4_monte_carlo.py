"""
Feature 4: Monte Carlo Confidence Simulation
Runs probabilistic simulations to estimate risk with confidence intervals
"""
import numpy as np
from typing import Dict

class MonteCarloSimulator:
    def __init__(self):
        self.default_trials = 1000
    
    def run_simulation(self, article_number: int, trials: int = None) -> Dict:
        """
        Run Monte Carlo simulation for the article
        Varies: court challenge probability, state disruption, political support
        Returns: mean, std_dev, 95% confidence interval
        """
        if trials is None:
            trials = self.default_trials
        
        np.random.seed(42)  # For reproducibility
        
        # Define simulation parameters based on article
        if article_number == 356:
            # Article 356: High uncertainty due to President's Rule complexity
            base_risk = 35.0
            court_challenge_prob = np.random.uniform(0.70, 0.90, trials)
            state_disruption = np.random.poisson(1.7, trials)  # Avg 1.7 President's Rule per year
            political_support = np.random.uniform(0.55, 0.75, trials)
            
            # Risk formula for 356
            simulated_risks = (
                base_risk + 
                court_challenge_prob * 40 +  # Court challenge impact
                np.minimum(state_disruption * 3, 15) +  # State disruption capped
                (1 - political_support) * 25  # Political opposition
            )
            
        elif article_number == 83:
            # Article 83: Moderate uncertainty (co-terminus provision)
            base_risk = 20.0
            court_challenge_prob = np.random.uniform(0.50, 0.90, trials)
            federalism_concern = np.random.beta(3, 2, trials)  # Skewed toward higher concern
            
            simulated_risks = (
                base_risk +
                court_challenge_prob * 25 +
                federalism_concern * 20
            )
            
        elif article_number == 172:
            # Article 172: Similar to 83 but with state autonomy emphasis
            base_risk = 25.0
            court_challenge_prob = np.random.uniform(0.55, 0.85, trials)
            state_autonomy_concern = np.random.beta(3.5, 2, trials)
            
            simulated_risks = (
                base_risk +
                court_challenge_prob * 25 +
                state_autonomy_concern * 22
            )
            
        else:
            # Default simulation for other articles
            base_risk = 15.0
            uncertainty = np.random.normal(0, 5, trials)
            simulated_risks = base_risk + uncertainty
        
        # Calculate statistics
        mean = np.mean(simulated_risks)
        std_dev = np.std(simulated_risks)
        ci_95 = [
            np.percentile(simulated_risks, 2.5),
            np.percentile(simulated_risks, 97.5)
        ]
        
        # Risk contribution is now purely informational (0.0 impact)
        risk_contribution = 0.0
        
        # Generate specific graph data based on article criteria
        graph_data = self._generate_graph_data(article_number, simulated_risks, trials)
        
        return {
            "mean": round(mean, 2),
            "std_dev": round(std_dev, 2),
            "confidence_interval_95": [round(ci_95[0], 2), round(ci_95[1], 2)],
            "trials": trials,
            "risk_contribution": 0.0,
            "graph_data": graph_data
        }

    def _generate_graph_data(self, article_number: int, simulated_risks: np.ndarray, trials: int) -> Dict:
        """Generate article-specific visualization data"""
        
        if article_number == 356:
            # Type: Distribution (Histogram)
            # Visualize the spread of risk outcomes
            counts, bins = np.histogram(simulated_risks, bins=10, range=(0, 100))
            return {
                "type": "distribution",
                "title": "Risk Probability Distribution",
                "x_label": "Risk Score",
                "y_label": "Frequency",
                "data": [
                    {"range": f"{int(bins[i])}-{int(bins[i+1])}", "frequency": int(c)} 
                    for i, c in enumerate(counts)
                ]
            }
            
        elif article_number in [83, 172]:
            # Type: Timeline (Line Chart)
            # Visualize stability/survival probability over 5 years
            years = [2029, 2030, 2031, 2032, 2033]
            decay_rate = 0.05 if article_number == 83 else 0.08 # State assemblies are more volatile
            stability = []
            current_prob = 1.0
            
            for year in years:
                # Slight randomness in decay
                decay = np.random.normal(decay_rate, 0.01)
                current_prob *= (1 - max(0, decay))
                stability.append({
                    "year": year, 
                    "stability_prob": round(current_prob * 100, 1)
                })
                
            return {
                "type": "timeline",
                "title": "Projected Stability over 5 Years",
                "x_label": "Year",
                "y_label": "Stability Probability (%)",
                "data": stability
            }
            
        elif article_number == 82:
            # Type: Scatter
            # Visualize Population Variance vs Seat Impact
            scatter_data = []
            for _ in range(50): # 50 points
                pop_var = np.random.uniform(-10, 10)
                seat_impact = pop_var * 1.5 + np.random.normal(0, 2)
                scatter_data.append({
                    "x": round(pop_var, 2),
                    "y": round(seat_impact, 2)
                })
                
            return {
                "type": "scatter",
                "title": "Population Change vs Seat Reallocation",
                "x_label": "Population Variance (%)",
                "y_label": "Seat Impact",
                "data": scatter_data
            }
            
        else:
            # Default: Bar chart of Confidence Interval
            mean = np.mean(simulated_risks)
            return {
                "type": "bar",
                "title": "Risk Confidence Interval",
                "data": [
                    {"label": "Lower 95%", "value": round(np.percentile(simulated_risks, 2.5), 2)},
                    {"label": "Mean", "value": round(mean, 2)},
                    {"label": "Upper 95%", "value": round(np.percentile(simulated_risks, 97.5), 2)}
                ]
            }

# Singleton instance
monte_carlo_simulator = MonteCarloSimulator()
