# Theory2Practice AI Bridge - Development Guide

## For Developers

### Project Structure

```
contextual-learning/
├── app.py                      # Main Streamlit application
├── pdf_export.py               # PDF generation module
├── requirements.txt            # Python dependencies
├── .env                       # Environment variables (not in git)
├── .env.example               # Environment template
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── start.sh                   # Quick start script
├── Dockerfile                 # Container definition
├── docker-compose.yml         # Docker orchestration
├── LICENSE                    # MIT License
└── README.md                  # User documentation
```

### Development Setup

1. **Clone and setup**
```bash
git clone <repo-url>
cd contextual-learning
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

3. **Run in development mode**
```bash
streamlit run app.py --server.runOnSave true
```

### Key Components

#### 1. `generate_use_cases()` Function
- Core AI generation logic
- Prompt engineering for different difficulty levels
- JSON response parsing with error handling
- Returns structured dictionary with use cases

#### 2. `display_use_case()` Function
- Renders individual use case cards
- Uses custom CSS for styling
- Organizes information hierarchically

#### 3. `export_to_markdown()` Function
- Converts generated content to Markdown
- Used for downloadable handouts

#### 4. `create_pdf_export()` Function (in pdf_export.py)
- Generates professional PDF documents
- Uses ReportLab for layout
- Custom styling and formatting

### Adding New Features

#### Add a New Field
Edit the selectbox in `app.py`:
```python
field = st.selectbox(
    "Select the Academic Field",
    [
        "Your New Field",  # Add here
        # ... existing fields
    ]
)
```

#### Modify the AI Prompt
Update the prompt in `generate_use_cases()`:
```python
prompt = f"""Your custom prompt here...
Topic: {topic}
Field: {field}
...
"""
```

#### Add a New Export Format
1. Create export function:
```python
def export_to_your_format(content: dict) -> str:
    # Your conversion logic
    return formatted_content
```

2. Add download button:
```python
with col_name:
    export_data = export_to_your_format(content)
    st.download_button(
        label="Your Format",
        data=export_data,
        file_name=f"export.{extension}",
        mime="your/mime-type"
    )
```

### Testing

#### Manual Testing Checklist
- [ ] App loads without errors
- [ ] API key validation works
- [ ] Use cases generate correctly
- [ ] All difficulty levels work
- [ ] All fields work
- [ ] Markdown export works
- [ ] JSON export works
- [ ] PDF export works (if reportlab installed)
- [ ] History tracking works
- [ ] UI is responsive

#### Test with Sample Topics
- Simple: "Arrays"
- Medium: "Binary Search Trees"
- Complex: "Gradient Descent Optimization"

### Performance Optimization

#### Caching LLM Responses
Add caching to reduce API calls:
```python
@st.cache_data(ttl=3600)
def generate_use_cases_cached(topic, field, difficulty_level, num_cases):
    return generate_use_cases(topic, field, difficulty_level, num_cases)
```

#### Session State Management
Current session state keys:
- `generated_content`: Last generated use cases
- `history`: List of generation history

### Deployment

#### Streamlit Cloud
1. Push to GitHub
2. Connect at share.streamlit.io
3. Add secrets in dashboard:
   ```toml
   GEMINI_API_KEY = "your_key_here"
   ```

#### Docker Deployment
```bash
# Build image
docker build -t theory2practice .

# Run container
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key theory2practice

# Or use docker-compose
docker-compose up -d
```

#### Environment Variables
- `GEMINI_API_KEY`: Required for AI generation
- Optional: Add rate limiting, analytics keys, etc.

### Troubleshooting

#### Common Issues

**Import Error: No module named 'reportlab'**
```bash
pip install reportlab
```

**API Rate Limiting**
- Add retry logic with exponential backoff
- Implement request queuing
- Cache responses

**JSON Parsing Errors**
- The app handles markdown code blocks automatically
- Check prompt format if errors persist
- Validate JSON structure in response

### Code Style

- Follow PEP 8
- Use type hints where practical
- Document functions with docstrings
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and test thoroughly
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open Pull Request

### License

MIT License - see LICENSE file

---

**Need Help?**
- Open an issue on GitHub
- Check existing issues for similar problems
- Provide error logs and reproduction steps
