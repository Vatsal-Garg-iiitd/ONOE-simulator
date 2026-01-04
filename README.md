# 🏆 Constitutional Engine for ONOE

A championship-winning application that analyzes the legal feasibility of **One Nation One Election (ONOE)** in India using advanced AI-powered constitutional analysis.

## 🎯 Features

### 8 Advanced Technical Features

1. **F1: AI Debate Agent** - Simulates Government vs Supreme Court constitutional arguments
2. **F2: RAG System** - Retrieves evidence from Constitution and Kovind Committee Report
3. **F3: Precedent Analysis** - Analyzes relevant Supreme Court cases
4. **F4: Monte Carlo Simulation** - Probabilistic risk modeling with confidence intervals
5. **F5: Real-time Explorer** - Interactive toggles for "what-if" scenarios
6. **F6: Political Support Tracker** - Tracks parliamentary majority requirements
7. **F7: Timeline Feasibility** - Assesses amendment completion timelines
8. **F8: Priority Ranking** - Ranks articles by risk and impact

### 7 Constitutional Articles Analyzed

- **Article 82**: Readjustment After Census
- **Article 83**: Duration of Lok Sabha
- **Article 85**: Presidential Dissolution
- **Article 172**: Duration of State Legislatures
- **Article 174**: Governor Dissolution Powers
- **Article 356**: President's Rule ⚠️ **CRITICAL BLOCKER**

## 🚀 Quick Start

### Backend (Python/FastAPI)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend will run on `http://localhost:8000`

### Frontend (React/Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on `http://localhost:5173`

## 📊 Key Findings

### Article 356: The Critical Blocker

**Risk Score**: 91.3/100 (CRITICAL)

**The Problem**: NO PROCEDURE DEFINED for conducting elections in states under President's Rule during synchronized national elections.

**Evidence**: 
- Kovind Report (Page 42): "No procedure has been defined for President's Rule scenarios during ONOE"
- 73% probability of at least one state under President's Rule during any 5-year cycle
- Constitution is completely silent on this scenario

**All 8 Features Applied**:
- F1 Debate: +34.0 pts (vulnerability score: 0.85)
- F2 RAG: Documentary evidence from Kovind Report
- F3 Precedent: +15.0 pts (S.R. Bommai, Kesavananda Bharati, State of Rajasthan)
- F4 Monte Carlo: +18.3 pts (mean: 79.2, 95% CI: [71.5, 87.9])
- F5 Explorer: +15.0 pts (procedure not defined)
- F6 Political: +8.75 pts (65% support vs 67% required)
- F7 Timeline: 0 pts (feasible by 2027)
- F8 Priority: Rank #1 CRITICAL

## 🎨 Design Highlights

- **Dark Mode** with vibrant gradients
- **Glassmorphism** effects
- **Framer Motion** animations
- **Recharts** visualizations
- **Google Fonts**: Inter (body), Outfit (headings)
- **Responsive** design

## 📁 Project Structure

```
Hackethon/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic data models
│   ├── risk_engine.py       # Core risk calculation
│   ├── features/            # 8 advanced features
│   │   ├── f1_debate_agent.py
│   │   ├── f2_rag_system.py
│   │   ├── f3_precedent_analysis.py
│   │   ├── f4_monte_carlo.py
│   │   ├── f5_explorer.py
│   │   ├── f6_political_tracker.py
│   │   ├── f7_timeline.py
│   │   └── f8_prioritizer.py
│   ├── routes/              # API endpoints
│   │   ├── articles.py
│   │   └── analysis.py
│   └── data/                # Constitution & Kovind Report excerpts
│       ├── constitution_excerpts.json
│       ├── kovind_report_excerpts.json
│       └── precedents.json
└── frontend/
    ├── src/
    │   ├── components/      # React components
    │   │   ├── RiskGauge.jsx
    │   │   ├── ArticleCard.jsx
    │   │   ├── DebateVisualization.jsx
    │   │   ├── ExplorerToggles.jsx
    │   │   ├── MonteCarloChart.jsx
    │   │   └── CriticalBlocker.jsx
    │   ├── pages/
    │   │   └── Dashboard.jsx
    │   ├── App.jsx
    │   └── index.css        # Design system
    └── package.json
```

## 🔌 API Endpoints

- `GET /api/articles/` - Get all articles with risk scores
- `GET /api/articles/{article_number}` - Get detailed analysis
- `POST /api/articles/{article_number}/toggle` - Apply explorer toggle
- `GET /api/articles/356/critical` - Special Article 356 endpoint
- `GET /api/analysis/overall` - Overall feasibility analysis
- `GET /api/analysis/priorities` - Ranked priorities
- `GET /api/analysis/recommendations` - Evidence-based recommendations

## 🏅 Championship Features

✅ 7 Constitutional Articles analyzed  
✅ 8 Advanced technical features implemented  
✅ Article 356 identified as CRITICAL BLOCKER (91.3/100 risk)  
✅ All features applied to Article 356  
✅ Transparent, evidence-based recommendations  
✅ Stunning modern UI with animations  
✅ Real-time interactive toggles  
✅ Monte Carlo confidence intervals  
✅ Supreme Court precedent analysis  
✅ RAG-powered evidence retrieval  

## 📝 License

MIT License - Built for Hackathon 2026

## 👨‍💻 Author

Built with ❤️ using FastAPI, React, and cutting-edge AI techniques
