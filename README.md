# 🎓 Theory2Practice AI Bridge

**Bridging the Gap Between Academic Theory and Real-World Industry Applications**

A Streamlit-powered application that helps professors and educators demonstrate how academic concepts are applied in real-world industry settings. Using AI (Google Gemini), it generates contextual, engaging use cases tailored to different student levels.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31%2B-red.svg)

---

## 🌟 Features

### Core Functionality
- **AI-Powered Use Case Generation**: Leverages Google Gemini to create authentic, industry-relevant examples
- **Adaptive Difficulty Levels**: Content automatically adjusts from Freshman to Graduate level
- **Multi-Field Support**: Covers 14+ academic fields from Computer Science to Economics
- **Structured Output**: Each use case includes:
  - Real-world problem statement
  - Theory application explanation
  - Industry context
  - Relevant job roles
  - Example companies
  - Business/societal impact

### Advanced Features
- **🆓 Free Trial System**: 3 free generations per device with usage tracking
- **📊 Related Skills**: Suggests complementary topics students should learn
- **🛤️ Learning Path**: Provides next-step recommendations
- **📥 Export Options**: Download as Markdown, JSON, or PDF
- **📜 Generation History**: Track previously generated topics
- **🎨 Beautiful UI**: Custom-styled components with visual hierarchy

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd contextual-learning
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API Key**
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

5. **Run the application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📖 Usage Guide

### For Professors/Educators

1. **Enter Your Topic**  
   Type the academic concept you're teaching (e.g., "Binary Search Trees", "Reinforcement Learning", "Game Theory")

2. **Select the Field**  
   Choose from 14 academic disciplines including Computer Science, Finance, Engineering, etc.

3. **Adjust Difficulty**  
   Use the slider to match your students' level - explanations automatically adapt in complexity

4. **Generate Use Cases**  
   Click "Generate Use Cases" to receive 3-5 real-world applications

5. **Share with Students**  
   Export as Markdown for handouts or JSON for integration with LMS systems

### Example Use Case

**Topic**: Hash Tables  
**Field**: Computer Science  
**Level**: Junior

**Generated Output** might include:
- Use Case 1: Database Indexing at MongoDB
- Use Case 2: Content Delivery Networks (CDNs) at Cloudflare
- Use Case 3: Cache Management in Redis

Each with detailed explanations, job roles (Backend Engineer, Database Administrator), and learning paths.

---

## 🆓 Free Trial & Usage Limits

The application includes a **3 free generations per device** limit to manage API costs. After using your free trials:

- You'll see a contact page with options for extended access
- Usage is tracked per session/device
- For unlimited access, institutional licenses, or custom deployments, contact:
  - **Email**: raj20032003@gmail.com
  - **Phone**: +92 342 8181914

See [RATE_LIMITING.md](RATE_LIMITING.md) for technical details.

---

## 🛠️ Technical Architecture

```
┌─────────────────────────────────────────┐
│         Streamlit UI Layer              │
│  (Input Forms, Display Components)      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│       Business Logic Layer              │
│  • generate_use_cases()                 │
│  • export_to_markdown()                 │
│  • display_use_case()                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Google Gemini API Layer            │
│  • Prompt Engineering                   │
│  • JSON Response Parsing                │
│  • Error Handling                       │
└─────────────────────────────────────────┘
```

### Key Technologies
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | Streamlit | Interactive UI with Python |
| AI Engine | Google Gemini 1.5 Pro | Use case generation |
| Config Management | python-dotenv | Secure API key handling |
| Export | Markdown/JSON | Content distribution |

---

## 🎨 Customization

### Adding New Fields
Edit the `field` selectbox in `app.py`:
```python
field = st.selectbox(
    "Select the Academic Field",
    [
        "Your New Field",  # Add here
        "Computer Science",
        # ... existing fields
    ]
)
```

### Adjusting Prompt Engineering
Modify the `generate_use_cases()` function's prompt template to:
- Change the number of use cases
- Add new output fields
- Adjust complexity descriptions
- Include industry-specific requirements

### Styling
Update the CSS in the `st.markdown()` section at the top of `app.py` to modify:
- Card colors
- Badge styles
- Button appearances
- Typography

---

## 📦 Project Structure

```
contextual-learning/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variable template
├── .env                   # Your API keys (not in git)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

---

## 🔧 Advanced Configuration

### Using Different AI Models

To switch from Gemini to GPT-4:
```python
# Replace the genai calls with:
import openai
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

### Deploying to Production

**Streamlit Cloud** (Recommended):
1. Push to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Add `GEMINI_API_KEY` to Secrets

**Docker**:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## 🐛 Troubleshooting

### Common Issues

**"API Key Missing" Error**
- Ensure `.env` file exists and contains `GEMINI_API_KEY=your_key`
- Verify the key is valid at [Google AI Studio](https://makersuite.google.com/)

**JSON Parsing Errors**
- The AI occasionally returns malformed JSON
- The app includes automatic cleanup of markdown code blocks
- If persistent, check the prompt formatting

**Slow Response Times**
- Gemini 1.5 Pro provides excellent performance
- For faster responses, reduce `num_cases`
- Consider caching responses for common topics

---

## 🗺️ Feature Roadmap

### Coming Soon
- [ ] PDF Export with custom styling
- [ ] Multi-language support (Spanish, French, etc.)
- [ ] Student feedback integration
- [ ] Classroom mode with batch topic generation
- [ ] LMS integration (Canvas, Blackboard)
- [ ] Analytics dashboard for usage tracking

### Future Enhancements
- [ ] Visual diagrams for complex concepts
- [ ] Video resource recommendations
- [ ] Industry expert interviews integration
- [ ] Student project idea generator

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **Google Gemini** for powerful, accessible AI capabilities
- **Streamlit** for making Python web apps effortless
- **Educators worldwide** who inspired this tool

---

## 📧 Contact & Support

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Email**: [Your contact email]

---

## 📊 Example Output

Here's what a generated use case looks like:

```markdown
### Use Case 1: High-Frequency Trading System Architecture

**Industry:** Financial Technology (FinTech)

**Problem Statement:**
Major investment firms like Jane Street and Citadel Securities process 
millions of trades per second, requiring microsecond-level response times. 
Traditional data structures create bottlenecks that cost millions in 
lost opportunities.

**How Theory Applies:**
Linked Lists enable efficient order book management where buy/sell orders 
are constantly inserted and removed. Unlike arrays, linked lists provide 
O(1) insertion/deletion when you have a reference to the node, crucial 
for maintaining time-price priority in trading queues.

**Impact:**
Optimized linked list implementations reduce trade execution latency by 
40-60%, translating to millions in additional revenue for trading firms.

**Job Roles:**
• Quantitative Developer
• High-Frequency Trading Engineer
• Financial Systems Architect

**Example Companies:**
• Jane Street Capital
• Citadel Securities
• Two Sigma
```

---

<div align="center">
  <strong>Built with ❤️ for educators who inspire the next generation</strong>
</div>
