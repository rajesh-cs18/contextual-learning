"""
Theory2Practice AI Bridge
A Streamlit application that bridges the gap between academic theory and real-world industry applications.
"""

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import hashlib
from pathlib import Path

# Import PDF export module
try:
    from pdf_export import create_pdf_export, get_pdf_filename
    PDF_EXPORT_AVAILABLE = True
except ImportError:
    PDF_EXPORT_AVAILABLE = False

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configuration
MAX_FREE_CALLS = 3
USAGE_FILE = Path("usage_tracking.json")
CONTACT_EMAIL = "raj20032003@gmail.com"
CONTACT_PHONE = "+92 342 8181914"

# Page configuration
st.set_page_config(
    page_title="Theory2Practice AI Bridge",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .use-case-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #1f77b4;
    }
    .industry-badge {
        background-color: #1f77b4;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 0.9em;
        display: inline-block;
        margin: 5px 5px 5px 0;
    }
    .job-role-badge {
        background-color: #ff7f0e;
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 0.9em;
        display: inline-block;
        margin: 5px 5px 5px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
    }
    .limit-reached-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .contact-info {
        background-color: rgba(255, 255, 255, 0.2);
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Rate Limiting Functions
def get_user_identifier() -> str:
    """
    Generate a unique identifier for the user based on session.
    In Streamlit Cloud, we use session ID as IP is not reliably available.
    """
    # Try to get session info, fall back to a persistent session ID
    if 'user_identifier' not in st.session_state:
        # Create a semi-persistent identifier
        try:
            # Try to access request headers for IP (may not work in all deployments)
            headers = st.context.headers
            ip = headers.get("X-Forwarded-For", headers.get("Remote-Addr", "unknown"))
            identifier = hashlib.md5(ip.encode()).hexdigest()
        except:
            # Fallback: use session-based ID that persists across runs
            import uuid
            identifier = str(uuid.uuid4())
        
        st.session_state.user_identifier = identifier
    
    return st.session_state.user_identifier

def load_usage_data() -> dict:
    """Load usage tracking data from file"""
    if USAGE_FILE.exists():
        try:
            with open(USAGE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_usage_data(data: dict):
    """Save usage tracking data to file"""
    try:
        with open(USAGE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving usage data: {e}")

def get_usage_count(identifier: str) -> int:
    """Get the current usage count for a user"""
    usage_data = load_usage_data()
    return usage_data.get(identifier, {}).get('count', 0)

def increment_usage(identifier: str):
    """Increment usage count for a user"""
    usage_data = load_usage_data()
    
    if identifier not in usage_data:
        usage_data[identifier] = {
            'count': 0,
            'first_used': datetime.now().isoformat(),
            'last_used': datetime.now().isoformat()
        }
    
    usage_data[identifier]['count'] += 1
    usage_data[identifier]['last_used'] = datetime.now().isoformat()
    
    save_usage_data(usage_data)
    return usage_data[identifier]['count']

def check_usage_limit() -> tuple[bool, int]:
    """
    Check if user has reached the usage limit.
    Returns: (can_use, remaining_calls)
    """
    identifier = get_user_identifier()
    current_count = get_usage_count(identifier)
    remaining = MAX_FREE_CALLS - current_count
    can_use = current_count < MAX_FREE_CALLS
    return can_use, max(0, remaining)

def display_limit_reached():
    """Display message when usage limit is reached"""
    st.markdown(f"""
    <div class="limit-reached-box">
        <h2>🎓 Free Trial Limit Reached</h2>
        <p style="font-size: 1.2em; margin: 20px 0;">
            You've used all <strong>{MAX_FREE_CALLS} free generations</strong>!<br>
            Thank you for trying Theory2Practice AI Bridge.
        </p>
        <div class="contact-info">
            <h3>📞 Want More Access?</h3>
            <p style="font-size: 1.1em; margin: 10px 0;">
                Contact us for unlimited access or custom solutions:
            </p>
            <p style="font-size: 1.3em; font-weight: bold; margin: 15px 0;">
                📧 {CONTACT_EMAIL}
            </p>
            <p style="font-size: 1.3em; font-weight: bold; margin: 15px 0;">
                📱 {CONTACT_PHONE}
            </p>
            <p style="font-size: 0.9em; margin-top: 20px; opacity: 0.9;">
                We offer institutional licenses, bulk access, and custom integrations.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Tip:** Clear your browser cache and use a different browser/device for additional free trials, or contact us for permanent access!")

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None
if 'history' not in st.session_state:
    st.session_state.history = []

def generate_use_cases(topic: str, field: str, difficulty_level: str, num_cases: int = 3) -> dict:
    """
    Generate real-world use cases using Gemini API
    
    Args:
        topic: The academic topic to contextualize
        field: The academic/industry field
        difficulty_level: Target audience level (Freshman/Sophomore/Junior/Senior/Graduate)
        num_cases: Number of use cases to generate
        
    Returns:
        Dictionary containing use cases and metadata
    """
    
    # Adjust complexity based on difficulty level
    complexity_guide = {
        "Freshman": "introductory level with simple explanations",
        "Sophomore": "intermediate level with some technical depth",
        "Junior": "advanced level with industry-standard terminology",
        "Senior": "expert level with complex real-world scenarios",
        "Graduate": "research-level with cutting-edge applications"
    }
    
    prompt = f"""You are an expert professor and industry consultant with deep knowledge of both academia and real-world applications.

Topic: "{topic}"
Field: "{field}"
Target Audience: {difficulty_level} ({complexity_guide[difficulty_level]})

Generate {num_cases} distinct, compelling real-world use cases that demonstrate how this topic is actually used in industry. For EACH use case, provide:

1. **Use Case Title**: A catchy, specific name for this application
2. **Industry**: The specific industry sector(s) where this is used
3. **Problem Statement**: The real-world problem being solved (2-3 sentences)
4. **How Theory Applies**: Explain specifically why "{topic}" is essential to solving this problem (2-3 sentences)
5. **Impact**: The tangible business or societal impact (1-2 sentences)
6. **Job Roles**: 2-3 specific job titles that work with this application
7. **Companies/Examples**: 2-3 real companies or organizations using this

Additionally, provide:
- **Key Takeaway**: A one-sentence insight for students
- **Related Skills**: 3-4 complementary topics students should learn to master this use case
- **Learning Path**: Suggested next steps for students interested in this application area

Format your response as valid JSON with this structure:
{{
    "use_cases": [
        {{
            "title": "...",
            "industry": "...",
            "problem": "...",
            "theory_application": "...",
            "impact": "...",
            "job_roles": ["...", "...", "..."],
            "companies": ["...", "...", "..."]
        }}
    ],
    "key_takeaway": "...",
    "related_skills": ["...", "...", "...", "..."],
    "learning_path": "..."
}}

Ensure the examples are current, relevant to {difficulty_level} students, and demonstrate clear connections between theory and practice."""

    try:
        model = genai.GenerativeModel('gemini-3-flash-preview')
        response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse JSON
        result = json.loads(response_text)
        result['topic'] = topic
        result['field'] = field
        result['difficulty_level'] = difficulty_level
        result['generated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return result
        
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse AI response. Error: {e}")
        return None
    except Exception as e:
        st.error(f"Error generating use cases: {e}")
        return None

def display_use_case(use_case: dict, index: int):
    """Display a single use case in a styled card"""
    
    with st.container():
        st.markdown(f"""
        <div class="use-case-card">
            <h3>🎯 Use Case {index + 1}: {use_case['title']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**🏭 Industry**")
            st.markdown(f'<span class="industry-badge">{use_case["industry"]}</span>', unsafe_allow_html=True)
            
            st.markdown("**❓ Problem Statement**")
            st.info(use_case['problem'])
            
            st.markdown("**🔬 How Theory Applies**")
            st.success(use_case['theory_application'])
            
            st.markdown("**💡 Impact**")
            st.write(use_case['impact'])
        
        with col2:
            st.markdown("**👔 Relevant Job Roles**")
            for role in use_case['job_roles']:
                st.markdown(f'<span class="job-role-badge">{role}</span>', unsafe_allow_html=True)
            
            st.markdown("**🏢 Example Companies**")
            for company in use_case['companies']:
                st.write(f"• {company}")
        
        st.markdown("---")

def export_to_markdown(content: dict) -> str:
    """Convert generated content to markdown format for export"""
    
    md = f"""# Theory2Practice: {content['topic']}
    
**Field:** {content['field']}  
**Difficulty Level:** {content['difficulty_level']}  
**Generated:** {content['generated_at']}

---

## Real-World Use Cases

"""
    
    for i, use_case in enumerate(content['use_cases'], 1):
        md += f"""### {i}. {use_case['title']}

**Industry:** {use_case['industry']}

**Problem Statement:**  
{use_case['problem']}

**How Theory Applies:**  
{use_case['theory_application']}

**Impact:**  
{use_case['impact']}

**Relevant Job Roles:**  
{', '.join(use_case['job_roles'])}

**Example Companies:**  
{', '.join(use_case['companies'])}

---

"""
    
    md += f"""## Key Takeaway
    
{content['key_takeaway']}

## Related Skills to Learn

{', '.join(content['related_skills'])}

## Suggested Learning Path

{content['learning_path']}

---
*Generated by Theory2Practice AI Bridge*
"""
    
    return md

# Main App UI
st.title("🎓 Theory2Practice AI Bridge")
st.markdown("*Connecting Academic Concepts to Real-World Industry Applications*")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.markdown("### 📚 Topic Details")
    topic = st.text_input(
        "What topic are you teaching?",
        placeholder="e.g., Linked Lists, Neural Networks, Supply Chain Optimization",
        help="Enter the specific academic topic or concept you want to contextualize"
    )
    
    field = st.selectbox(
        "Select the Academic Field",
        [
            "Computer Science",
            "Data Science",
            "Cybersecurity",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Finance",
            "Economics",
            "Business Analytics",
            "Mathematics",
            "Statistics",
            "Artificial Intelligence",
            "Software Engineering",
            "Information Systems",
            "Operations Research"
        ],
        help="Choose the primary field of study"
    )
    
    st.markdown("### 🎯 Audience Settings")
    difficulty_level = st.select_slider(
        "Student Level",
        options=["Freshman", "Sophomore", "Junior", "Senior", "Graduate"],
        value="Junior",
        help="Adjust the complexity and depth of the use cases"
    )
    
    num_cases = st.slider(
        "Number of Use Cases",
        min_value=1,
        max_value=5,
        value=3,
        help="How many distinct use cases to generate"
    )
    
    st.markdown("---")
    
    # Check usage limit and display info
    can_use, remaining_calls = check_usage_limit()
    
    if can_use:
        if remaining_calls > 0:
            st.info(f"🆓 Free trials remaining: **{remaining_calls}/{MAX_FREE_CALLS}**")
    
    generate_button = st.button("🚀 Generate Use Cases", type="primary", disabled=not can_use)
    
    # API Key Status
    st.markdown("---")
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        st.success("✅ API Key Configured")
    else:
        st.error("❌ API Key Missing")
        st.info("Set GEMINI_API_KEY in your .env file")

# Main Content Area
if not check_usage_limit()[0]:
    # Display limit reached message
    display_limit_reached()
elif generate_button:
    if not topic:
        st.warning("⚠️ Please enter a topic to generate use cases.")
    elif not api_key:
        st.error("❌ Gemini API key is not configured. Please add it to your .env file.")
    else:
        with st.spinner(f"🤖 Generating real-world use cases for '{topic}'..."):
            content = generate_use_cases(topic, field, difficulty_level, num_cases)
            
            if content:
                # Increment usage count on successful generation
                identifier = get_user_identifier()
                new_count = increment_usage(identifier)
                
                st.session_state.generated_content = content
                st.session_state.history.append({
                    'topic': topic,
                    'field': field,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("✅ Use cases generated successfully!")
                
                # Show updated remaining count
                remaining = MAX_FREE_CALLS - new_count
                if remaining > 0:
                    st.info(f"🎯 You have **{remaining}** free generation{'s' if remaining != 1 else ''} remaining!")
                else:
                    st.warning(f"⚠️ This was your last free generation! Contact {CONTACT_EMAIL} for more access.")

# Display generated content
if st.session_state.generated_content:
    content = st.session_state.generated_content
    
    # Header
    st.markdown(f"## 🌟 Real-World Applications of: **{content['topic']}**")
    st.markdown(f"*in the context of {content['field']} • {content['difficulty_level']} Level*")
    st.markdown("---")
    
    # Display use cases
    for i, use_case in enumerate(content['use_cases']):
        display_use_case(use_case, i)
    
    # Key Insights Section
    st.markdown("## 🔑 Key Insights for Students")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💡 Main Takeaway")
        st.info(content['key_takeaway'])
        
        st.markdown("### 📖 Related Skills to Master")
        for skill in content['related_skills']:
            st.write(f"• {skill}")
    
    with col2:
        st.markdown("### 🛤️ Suggested Learning Path")
        st.success(content['learning_path'])
    
    # Export Options
    st.markdown("---")
    st.markdown("## 📥 Export Options")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        markdown_export = export_to_markdown(content)
        st.download_button(
            label="📄 Markdown",
            data=markdown_export,
            file_name=f"theory2practice_{content['topic'].replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    with col2:
        json_export = json.dumps(content, indent=2)
        st.download_button(
            label="📊 JSON",
            data=json_export,
            file_name=f"theory2practice_{content['topic'].replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col3:
        if PDF_EXPORT_AVAILABLE:
            try:
                pdf_buffer = create_pdf_export(content)
                st.download_button(
                    label="📑 PDF",
                    data=pdf_buffer,
                    file_name=get_pdf_filename(content['topic']),
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.button("📑 PDF", disabled=True, use_container_width=True)
                st.caption(f"PDF export error: {str(e)[:30]}...")
        else:
            st.button("📑 PDF", disabled=True, use_container_width=True)
            st.caption("Install reportlab")
    
    with col4:
        if st.button("🔄 New Version", use_container_width=True):
            st.session_state.generated_content = None
            st.rerun()

# History Section (collapsible)
if st.session_state.history:
    with st.expander("📜 Generation History"):
        for i, item in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.write(f"{i}. **{item['topic']}** ({item['field']}) - {item['timestamp']}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p>Theory2Practice AI Bridge | Powered by Google Gemini | Built with Streamlit</p>
    <p>💡 Tip: Try different difficulty levels to see how explanations adapt to student knowledge!</p>
</div>
""", unsafe_allow_html=True)
