# 🚀 Quick Start Guide

Get the Theory2Practice AI Bridge running in **under 5 minutes**.

---

## Prerequisites

- **Python 3.10+** installed ([Download here](https://www.python.org/downloads/))
- **Gemini API Key** ([Get free key](https://makersuite.google.com/app/apikey))

---

## Installation Steps

### Option 1: Automated Setup (Recommended)

Run the setup script:

```bash
./start.sh
```

Follow the prompts to configure your API key.

---

### Option 2: Manual Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key**
   ```bash
   cp .env.example .env
   # Edit .env and add: GEMINI_API_KEY=your_key_here
   ```

3. **Run the app**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**  
   Navigate to: `http://localhost:8501`

---

### Option 3: Docker (Production)

```bash
# Set your API key in environment or .env file
docker-compose up -d
```

Open `http://localhost:8501`

---

## First Use

1. Enter a topic (e.g., "Hash Tables")
2. Select a field (e.g., "Computer Science")
3. Adjust difficulty level (try "Junior")
4. Click **"Generate Use Cases"**
5. Download results as Markdown, JSON, or PDF

---

## Example Topics to Try

- **Computer Science:** Recursion, Binary Trees, Dynamic Programming
- **Data Science:** Linear Regression, K-Means Clustering
- **Finance:** Time Series Analysis, Portfolio Optimization
- **Engineering:** PID Controllers, Fourier Transforms

---

## Troubleshooting

### "API Key Missing" Error
Make sure your `.env` file contains:
```
GEMINI_API_KEY=your_actual_key_from_google
```

### Port 8501 Already in Use
```bash
streamlit run app.py --server.port 8502
```

### PDF Export Not Working
```bash
pip install reportlab
```

---

## What's Next?

- Read [README.md](README.md) for full feature documentation
- Check [DEVELOPMENT.md](DEVELOPMENT.md) for customization guide
- See [examples/](examples/) for sample outputs

---

## Need Help?

- Check if your Python version is 3.10+: `python3 --version`
- Verify pip is updated: `pip install --upgrade pip`
- Open an issue on GitHub with error details

---

**Ready to bridge theory and practice! 🎓**
