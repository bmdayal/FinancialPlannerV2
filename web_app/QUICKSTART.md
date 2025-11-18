# Quick Start Guide# Quick Start Guide - Financial Planner Web Application



## Setup (5 Minutes)## 🚀 Get Started in 5 Minutes



1. **Get API Key**: https://platform.openai.com/api-keys### Prerequisites

2. **Install**: `cd web_app && pip install -r requirements.txt`- Python 3.8 or higher

3. **Configure**: Create `.env` file with `OPENAI_API_KEY=your-key-here`- OpenAI API key (get one free at https://platform.openai.com)

4. **Run**: `python app.py`

5. **Open**: http://localhost:5000### Step 1: Get Your API Key

1. Go to https://platform.openai.com/api-keys

## How to Use2. Click "Create new secret key"

3. Copy the key (starts with `sk-`)

1. **Select Plans**: Choose from 6 AI agents (Retirement, Insurance, Estate, Wealth, Education, Tax)4. Keep this safe - you'll need it in the next step

2. **Fill Form**: Enter your financial details (form adapts to selected plans)

3. **Generate Plan**: AI agents create personalized recommendations### Step 2: Automated Setup (Recommended)

4. **Review Results**: Interactive charts, detailed summaries, and executive overview

5. **Ask Questions**: Chat with AI advisor about your plan#### On Windows (PowerShell or Command Prompt):

6. **Export**: Download as JSON```powershell

cd web_app

## Featurespython setup.py

# Follow the prompts and paste your API key when asked

🤖 **6 AI Agents** - Specialized expertise for each planning area```

📊 **Interactive Charts** - Visual projections and breakdowns  

💬 **AI Chat** - Context-aware follow-up questions#### On macOS/Linux:

📄 **Export** - JSON download for sharing with advisors```bash

cd web_app

## Troubleshootingpython3 setup.py

# Follow the prompts and paste your API key when asked

- **"API Key not set"** → Check `.env` file exists with correct key```

- **"Module not found"** → Run `pip install -r requirements.txt`

- **Port in use** → Change `APP_PORT=5001` in `.env`### Step 3: Run the Application

- **Charts not showing** → Check browser console (F12) for errors

#### Windows (PowerShell):

## Tips```powershell

cd web_app

- Select multiple plans for integrated recommendations.\run.ps1

- Ask specific questions like "What if I retire at 62?"```

- Export plans to share with financial advisors

- AI responses take 10-30 seconds (normal)#### Windows (Command Prompt):

```cmd

⚖️ **Disclaimer**: Educational tool only. Consult qualified financial professionals for investment decisions.cd web_app
run.bat
```

#### macOS/Linux:
```bash
cd web_app
./run.sh
```

### Step 4: Open in Browser
Visit: **http://localhost:5000**

---

## 📋 Manual Setup (If Automated Setup Fails)

### Step 1: Install Dependencies
```bash
cd web_app
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Copy template
cp .env.example .env  # On Windows: copy .env.example .env

# Edit .env and add your API key
# OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Run Flask App
```bash
python app.py
```

### Step 4: Open Browser
Visit: **http://localhost:5000**

---

## 🎯 Using the Application

### Landing Page (Step 1: Select Plans)
- ✅ Check the planning services you need (Retirement, Insurance, Estate, Wealth, Education, Tax Planning)
- 📝 Selected form fields will appear automatically

### User Information (Step 2: Fill Out Form)
- Fill in your financial details
- Additional fields appear based on selected plans
- Click "Generate My Financial Plan"

### Results Page
- 📊 View interactive charts and visualizations
- 📋 Read detailed plan summaries
- 💬 Ask follow-up questions in the chat interface
- 📥 Download your complete plan as JSON

### Chat Interface
- Ask any questions about your plan
- The AI advisor has full context of your situation
- Get personalized explanations and insights

---

## ❓ Troubleshooting

### Issue: "OPENAI_API_KEY not set"
**Solution**: 
1. Check that `.env` file exists in the `web_app` directory
2. Verify you've added your API key: `OPENAI_API_KEY=sk-...`
3. Save the file and restart the app

### Issue: "ModuleNotFoundError" or "Import Error"
**Solution**:
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Port 5000 Already in Use
**Solution**: Edit `.env` and change:
```
APP_PORT=5001
```
Then restart the app

### Issue: Slow Initial Load
**Solution**: 
- First run takes longer (AI agents are processing)
- Subsequent loads are faster
- Chat responses take 10-30 seconds (normal for AI)

### Issue: Charts Not Displaying
**Solution**:
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Clear browser cache
4. Try a different browser

---

## 💡 Tips & Tricks

### Select Multiple Plans
- You can select 2, 3, or all 6 planning areas at once
- Form adapts to show only relevant fields
- Executive summary integrates all recommendations

### Ask Detailed Questions
Examples of good follow-up questions:
- "What if I retire at 62 instead?"
- "How much should I save monthly?"
- "What are the tax implications?"
- "Can you explain the asset allocation?"
- "How does this affect my insurance needs?"

### Export Your Plan
- Click "Download Plan" button
- Saves as JSON file
- Share with your financial advisor
- Contains all summaries and your profile

### Create Multiple Plans
- Click "New Plan" to go back
- Change answers and generate a new plan
- Compare different scenarios

---

## 📚 Features Overview

### Retirement Planning
- Calculates how much you need for retirement
- Projects savings with different contribution levels
- Recommends asset allocation
- Shows withdrawal strategy

### Insurance Planning
- Determines life insurance needs (10x income + debts)
- Adjusts for number of dependents
- Includes disability and long-term care recommendations
- Estimates monthly premiums

### Estate Planning
- Calculates estate taxes
- Determines education funding needs for children
- Recommends wills and trusts
- Tax minimization strategies

### Wealth Management
- Personalized investment allocation
- Risk-adjusted recommendations
- Diversification guidelines
- Portfolio rebalancing schedule

### Education Planning
- 529 plan analysis and projections
- Scholarship opportunity identification
- Educational loan strategy development
- Timeline-based funding approaches

### Tax Planning
- Year-round tax optimization strategies
- Deduction identification and maximization
- Tax-efficient investment planning
- Integration across all planning areas

---

## 🔗 Important Links

- **OpenAI Platform**: https://platform.openai.com
- **Get API Key**: https://platform.openai.com/api-keys
- **LangChain Docs**: https://python.langchain.com
- **Flask Documentation**: https://flask.palletsprojects.com

---

## ⚖️ Important Disclaimer

This application provides educational and informational financial planning insights powered by AI. It is NOT:
- A substitute for professional financial advice
- Investment advice or recommendations
- Tax advice
- Legal advice

**Always consult with qualified financial professionals before making financial decisions.**

---

## 📞 Getting Help

1. **Check README.md** for comprehensive documentation
2. **Review server logs** when app is running
3. **Check browser console** (F12) for client-side errors
4. **Verify .env configuration** is correct
5. **Ensure API key is valid** at https://platform.openai.com

---

## 🎓 Next Steps After Setup

1. Try generating a sample plan
2. Explore different plan combinations
3. Use the chat interface to ask questions
4. Export and review your financial plan
5. Share with your financial advisor

**Enjoy using the Financial Planner! 🎉**
