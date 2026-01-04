# Constitutional Engine for ONOE - Setup Instructions

## 🔑 API Key Configuration

### Step 1: Get Your Hugging Face API Key

1. Go to [Hugging Face](https://huggingface.co/)
2. Sign up or log in
3. Go to Settings → Access Tokens
4. Create a new token with "Read" permissions
5. Copy the token

### Step 2: Configure Environment Variables

1. Open the `.env` file in the `backend` folder:
   ```bash
   cd backend
   nano .env  # or use any text editor
   ```

2. Add your Hugging Face API key:
   ```
   HUGGINGFACE_API_KEY=hf_your_actual_api_key_here
   ```

3. Save the file

### Step 3: Install New Dependencies

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

This will install:
- `langgraph` - Multi-agent workflow framework
- `langchain` - LLM orchestration
- `langchain-huggingface` - Hugging Face integration
- `huggingface-hub` - API client

### Step 4: Restart Backend

Stop the current backend (Ctrl+C) and restart:

```bash
python main.py
```

## 🎯 What's New

### Enhanced F1: AI Debate Agent

**LangGraph Workflow:**
1. **Government Node** - Presents pro-ONOE arguments
2. **Court Node** - Presents constitutional challenges
3. **Assessment Node** - Calculates vulnerability score
4. **Mitigation Node** - Suggests risk reduction strategies

**DeepSeek Integration:**
- Uses `deepseek-ai/deepseek-llm-7b-chat` via Hugging Face
- Fallback to predefined responses if API unavailable
- Maintains same risk calculation logic

**Frontend Enhancements:**
- Full debate transcript display
- Mitigation strategies shown
- Expandable transcript viewer
- Color-coded debate points

## 🔄 Fallback Mode

If you don't have a Hugging Face API key, the system will:
- Use predefined constitutional arguments
- Maintain accurate risk scores
- Show full debate structure
- Work perfectly for demo purposes

## 🚀 Quick Start

**With API Key:**
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
# Add HUGGINGFACE_API_KEY to .env
python main.py

# Frontend (separate terminal)
cd frontend
npm run dev
```

**Without API Key (Demo Mode):**
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
# Leave .env empty
python main.py

# Frontend
cd frontend
npm run dev
```

## 📊 Testing the Enhanced Debate

1. Open http://localhost:5173
2. Click on Article 83, 172, or 356
3. Scroll to "Constitutional Debate Analysis"
4. See:
   - Government position
   - Court counter-argument
   - Vulnerability assessment
   - Mitigation strategies
   - Full transcript (expandable)

## 🎨 Visual Improvements

- **LangGraph badge** on debate title
- **Transcript viewer** with color-coded entries
- **Mitigation cards** with green highlights
- **Assessment section** with probability display

Enjoy your championship-winning Constitutional Engine! 🏆
