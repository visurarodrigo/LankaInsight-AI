import streamlit as st
import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

# --- 1. APP CONFIGURATION & API SETUP ---
st.set_page_config(
    page_title="LankaInsight | Business Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
load_dotenv()

# Custom CSS for a modern editorial intelligence dashboard
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #17313b;
        --muted: #52666b;
        --paper: #f8faf9;
        --surface: #ffffff;
        --line: #dce5e1;
        --teal: #0f766e;
        --teal-dark: #0b5f59;
        --coral: #ef6a5b;
        --coral-soft: #fff0ed;
    }

    /* Main App Background */
    .stApp {
        background: var(--paper);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stAppViewContainer"] > .main {
        background: var(--paper);
    }

    .block-container {
        max-width: 1200px;
        padding: 2rem 2.5rem 2.5rem !important;
        margin-top: 0 !important;
    }

    h1, h2, h3, h4 {
        color: var(--ink) !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }

    h2 {
        font-size: 1.4rem !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.8rem !important;
    }

    p, label, .stCaption {
        color: var(--muted);
    }

    /* Compact spacing */
    .stMarkdown, .stText, .stHtml {
        margin-bottom: 0.5rem !important;
    }

    /* Header - More compact */
    .main-header {
        color: var(--ink) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.8rem !important;
        line-height: 1 !important;
        margin: 0 0 0.3rem 0 !important;
        font-weight: 700 !important;
    }

    .main-header::after {
        background: var(--coral);
        border-radius: 99px;
        content: '';
        display: inline-block;
        height: 0.5rem;
        margin-left: 0.4rem;
        width: 0.5rem;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted);
        font-size: 0.85rem;
        margin-top: 0 !important;
        margin-bottom: 1rem !important;
    }

    hr {
        border: 0;
        border-top: 1px solid var(--line);
        margin: 1rem 0;
    }

    /* Surface styling - tighter padding */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--surface);
        border: 1px solid var(--line) !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(23, 49, 59, 0.06) !important;
        padding: 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Inputs - compact */
    .stTextArea, .stTextInput, .stNumberInput {
        margin-bottom: 0.5rem !important;
    }
    
    .stTextArea textarea, .stTextInput input, .stNumberInput input {
        background: var(--surface) !important;
        border: 1px solid var(--line) !important;
        border-radius: 6px !important;
        color: var(--ink) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* Primary Button */
    div.stButton > button[kind="primary"] {
        background: var(--teal) !important;
        border: 1px solid var(--teal) !important;
        border-radius: 6px !important;
        color: white !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        min-height: 2.4rem;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="primary"] *,
    div.stButton > button[kind="primary"] p {
        color: #ffffff !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background: var(--teal-dark) !important;
        box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25) !important;
        transform: translateY(-1px) !important;
    }

    /* Tabs - compact */
    .stTabs {
        margin-top: 0.5rem !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: #eef3f1;
        border-radius: 8px;
        gap: 0.2rem !important;
        padding: 0.2rem;
        margin-bottom: 1rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: var(--muted) !important;
        height: 38px !important;
        white-space: nowrap !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        padding: 0 0.9rem !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: var(--surface) !important;
        box-shadow: 0 2px 6px rgba(23, 49, 59, 0.08);
        color: var(--teal) !important;
    }

    /* Metrics - compact */
    div[data-testid="stMetric"] {
        background: #f0f5f3;
        border-left: 3px solid var(--coral);
        border-radius: 5px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.5rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: var(--ink) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
    }

    /* Sidebar - Dark and modern */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2830 0%, #17313b 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    section[data-testid="stSidebar"] * {
        color: #e8f1ee !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-top-color: rgba(234, 242, 239, 0.2);
        margin: 1rem 0;
    }
    section[data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 6px;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #c5d5d0 !important;
        line-height: 1.6;
        font-size: 0.85rem;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #e8f1ee !important;
        font-weight: 600 !important;
        font-size: 0.8rem;
    }
    section[data-testid="stSidebar"] [data-testid="stSlider"] div[role="slider"] {
        background: var(--coral) !important;
    }

    /* Info boxes - compact */
    [data-testid="stAlert"] {
        border: 1px solid #f7c9c2;
        border-radius: 6px;
        padding: 0.6rem 0.9rem !important;
        margin: 0.5rem 0 !important;
    }
    [data-testid="stAlert"] p {
        color: #31515c !important;
        font-weight: 500;
        font-size: 0.85rem;
        margin: 0 !important;
    }

    /* Columns spacing */
    .stColumn {
        padding: 0.3rem !important;
    }

    /* Remove excessive margins from widgets */
    .stTextInput, .stTextArea, .stButton, .stMarkdown {
        margin-bottom: 0.4rem !important;
    }

    @media (max-width: 800px) {
        .block-container {
            padding: 1.5rem 1rem 2rem !important;
        }
        .main-header {
            font-size: 2.2rem !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.74rem !important;
            padding: 0 0.6rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Load API Key: Checks local .env first, then Streamlit Secrets (for cloud deployment)
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        pass

if not api_key:
    st.error("❌ Groq API Key not found. Please set it in your .env file or Streamlit Secrets.")
    st.stop()

# Initialize Groq Client
MODEL_NAME = "openai/gpt-oss-20b" 

@st.cache_resource
def get_groq_client():
    return Groq(api_key=api_key)

def call_groq(prompt, temperature=None, max_tokens=None):
    """Sends prompt to Groq and returns the text response."""
    client = get_groq_client()

    # Use sidebar settings if specific values aren't provided
    temp = temperature if temperature is not None else st.session_state.get('temperature', 0.2)
    tokens = max_tokens if max_tokens is not None else st.session_state.get('max_tokens', 2000)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=temp,
            max_tokens=tokens,
            top_p=0.8
        )
        content = response.choices[0].message.content
        # Handle cases where the model returns empty or whitespace
        if not content or not content.strip():
            return "⚠️ Model returned an empty response. Please try again."
        return content
    except Exception as e:
        return f"⚠️ System Error: {str(e)}"

# --- 2. HELPER: ROBUST JSON PARSER ---
def parse_json_response(raw_text):
    """Extracts JSON from LLM output, ignoring conversational filler or markdown."""
    if not raw_text or "empty response" in raw_text.lower():
        return None, raw_text
        
    # Find the first '{' and the last '}' to isolate the JSON object
    start_idx = raw_text.find('{')
    end_idx = raw_text.rfind('}')

    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_str = raw_text[start_idx:end_idx+1]
        try:
            # Remove possible trailing commas or common LLM JSON artifacts
            return json.loads(json_str), None
        except json.JSONDecodeError:
            # Try a slightly more aggressive cleanup for common LLM errors
            try:
                # Remove common markdown-like artifacts if any
                cleaned_str = re.sub(r'^```json\s*|\s*```$', '', json_str.strip(), flags=re.IGNORECASE | re.MULTILINE)
                return json.loads(cleaned_str), None
            except:
                return None, json_str
    return None, raw_text

# --- 3. UI HEADER ---
st.markdown('<h1 class="main-header">LankaInsight</h1>', unsafe_allow_html=True)
st.caption("AI-Powered Business Intelligence for the Sri Lankan Market")
st.divider()

# --- 4. SIDEBAR (Control Center) ---
with st.sidebar:
    st.header("About LankaInsight")
    st.markdown("""
    LankaInsight is a practical business intelligence tool designed for Sri Lankan analysts, product managers, and recruiters.
    It transforms unstructured local business data into actionable, structured insights in seconds.
    """)

    st.divider()

    # Model Tuning Section
    with st.expander("⚙️ Model Tuning", expanded=True):
        st.caption("Adjust the AI's behavior for different tasks.")
        st.session_state.temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05, help="Higher values make output more creative, lower values more deterministic.")
        st.session_state.max_tokens = st.number_input("Max Tokens", min_value=100, max_value=32000, value=2000, step=100, help="Limits the length of the AI response.")

    st.divider()

    st.subheader("How it Works")
    st.markdown("""
    Under the hood, this application leverages advanced Large Language Model (LLM) architectures and prompt engineering techniques to ensure high accuracy and reliability:

    * **Zero-Shot Generation:** Used in the News Briefer to synthesize complex economic data without prior examples.
    * **Few-Shot Classification:** Powers the Review Analyzer by providing the model with contextual examples to ensure strict adherence to local business categories.
    * **Chain-of-Thought Reasoning:** The Impact Analyzer forces the model to reason step-by-step internally before generating strategic recommendations, significantly reducing hallucinations.
    * **Structured Output Parsing:** The Job Intelligence feature enforces strict JSON schemas, allowing seamless integration with downstream HR databases.
    """)

    st.divider()
    st.caption("Built by Visura Rodrigo | Data Science & Business Analytics")

# --- 5. MAIN TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📰 News Briefer", 
    "⭐ Review Analyzer", 
    "📉 Impact Analyzer", 
    "💼 Job Intelligence"
])

# ==========================================
# FEATURE 1: ECONOMIC NEWS BRIEFER
# ==========================================
with tab1:
    st.header("Economic News Briefer")
    st.markdown("Transform raw economic updates into concise, executive-ready summaries.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        default_news = """The Central Bank of Sri Lanka reported that inflation eased to 4.5% in August, down from 5.1% in July, driven by lower food and energy prices. However, the bank warned that global supply chain disruptions could cause minor fluctuations in the coming quarter. The rupee has remained relatively stable against the US dollar, and foreign reserves have increased to $3.2 billion."""
        
        news_text = st.text_area("Paste Economic News or Headlines:", value=default_news, height=150)
        
        if st.button("Generate Brief", type="primary", use_container_width=True):
            prompt = f"""You are a Senior Business Analyst for a top-tier consulting firm in Sri Lanka.
Summarize the following economic news text into exactly 3 concise, high-impact bullet points tailored for C-suite executives.
Focus on financial implications, market trends, and strategic takeaways. Do not include introductory or concluding text.

Text:
\"\"\"
{news_text}
\"\"\"
"""
            with st.spinner("Synthesizing market data..."):
                result = call_groq(prompt, temperature=0.2, max_tokens=8000)
            
            st.subheader("Executive Summary")
            st.write(result)

    with col2:
        st.info("💡 **Best for:** Daily market monitoring, investor updates, and quick strategic alignment.")

# ==========================================
# FEATURE 2: CUSTOMER REVIEW ANALYZER
# ==========================================
with tab2:
    st.header("Customer Review Analyzer")
    st.markdown("Instantly categorize, score, and generate action plans for customer feedback.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        default_review = "I waited 45 minutes at the Commercial Bank branch in Nugegoda just to deposit a cheque, and the teller was incredibly rude when I asked about the delay. The app also crashed twice while I was trying to check my balance beforehand."
        
        review_text = st.text_area("Paste Customer Review:", value=default_review, height=120)
        
        if st.button("Analyze Feedback", type="primary", use_container_width=True):
            # FIX: Removed "ONLY the JSON object" constraint which caused empty responses
            prompt = f"""You are a Customer Experience (CX) Analyst for Sri Lankan businesses.
Analyze the customer review below and output a JSON object with the following keys:
"category", "sentiment", "severity", "recommended_action".

Examples:
Review: "The kottu was cold and the chicken was undercooked."
Output: {{"category": "Food", "sentiment": "Negative", "severity": "High", "recommended_action": "Audit kitchen plating times and chicken preparation protocols."}}

Review: "The PickMe app crashed right when I was about to pay, very frustrating."
Output: {{"category": "App", "sentiment": "Negative", "severity": "Medium", "recommended_action": "Investigate payment gateway stability and add a retry mechanism."}}

Now analyze this review and output the JSON:
Review: "{review_text}"
Output:
"""
            with st.spinner("Processing customer feedback..."):
                raw_result = call_groq(prompt, temperature=0.1, max_tokens=8000)
            
            parsed_data, error = parse_json_response(raw_result)
            
            if parsed_data:
                st.subheader("Analysis Results")
                c1, c2, c3 = st.columns(3)
                c1.metric("Category", parsed_data.get("category", "N/A"))
                
                sentiment = parsed_data.get("sentiment", "N/A")
                if sentiment == "Positive": c2.metric("Sentiment", sentiment, delta="😊")
                elif sentiment == "Negative": c2.metric("Sentiment", sentiment, delta="😠")
                else: c2.metric("Sentiment", sentiment, delta="😐")
                
                severity = parsed_data.get("severity", "N/A")
                c3.metric("Severity", severity)
                
                st.divider()
                st.write("**Recommended Action:**")
                st.success(parsed_data.get("recommended_action", "N/A"))
            else:
                st.error("⚠️ Failed to parse analysis. Please try again.")
                with st.expander("View Raw Output for Debugging"):
                    st.code(error)

    with col2:
        st.info("💡 **Best for:** QA teams, branch managers, and app developers monitoring user sentiment.")

# ==========================================
# FEATURE 3: BUSINESS IMPACT ANALYZER
# ==========================================
with tab3:
    st.header("Business Impact Analyzer")
    st.markdown("Evaluate strategic risks and operational impacts of local economic events.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        default_scenario = "The Sri Lankan government introduces a new 15% digital services tax on all foreign SaaS platforms (like AWS, Slack, and Adobe) starting next quarter."
        
        scenario_text = st.text_area("Describe Business Scenario or Economic Event:", value=default_scenario, height=120)
        
        if st.button("Run Impact Analysis", type="primary", use_container_width=True):
            # FIX: Switched from XML tags to Markdown headers, which this model prefers
            prompt = f"""You are a Strategic Risk Consultant for the Sri Lankan corporate sector.
Analyze the business scenario below.

Instructions:
1. First, think step-by-step about the direct and indirect effects, risk factors, and strategic implications. Put this reasoning inside a section titled '### Reasoning Process ###'.
2. Then, provide your final structured analysis inside a section titled '### Strategic Assessment ###' using the following exact format:

**Direct Impact:** [1-2 sentences on immediate operational/financial effects]
**Indirect Impact:** [1-2 sentences on secondary market or supply chain effects]
**Risk Level:** [Low / Medium / High / Critical]
**Executive Recommendation:** [Exactly 2 sentences advising the C-suite]

Scenario:
{scenario_text}
"""
            with st.spinner("Running strategic risk simulation..."):
                raw_output = call_groq(prompt, temperature=0.5, max_tokens=8000)
            
            # FIX: Parse using Markdown headers, with a fallback if the model ignores them
            assessment_match = re.search(r'### Strategic Assessment ###\s*(.*)', raw_output, re.IGNORECASE | re.DOTALL)
            thinking_match = re.search(r'### Reasoning Process ###\s*(.*?)(?=### Strategic Assessment ###|$)', raw_output, re.IGNORECASE | re.DOTALL)
            
            if assessment_match:
                clean_output = assessment_match.group(1).strip()
            else:
                # Fallback: If the model ignored the headers, just use the whole output
                clean_output = raw_output.strip()
            
            st.subheader("Strategic Assessment")
            st.markdown(clean_output)
            
            if thinking_match:
                with st.expander("🧠 View Analyst's Reasoning Process"):
                    st.markdown("*The following is the internal step-by-step logic used to generate the assessment:*")
                    st.text(thinking_match.group(1).strip())

    with col2:
        st.info("💡 **Best for:** Strategy teams, policy analysts, and board-level risk assessments.")

# ==========================================
# FEATURE 4: JOB POST INTELLIGENCE
# ==========================================
with tab4:
    st.header("Job Post Intelligence")
    st.markdown("Extract structured data and evaluate role alignment with Data Science profiles.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        default_job = """Wanted: Junior Data Analyst at TechLanka Solutions. 
Location: Hybrid (Colombo 03 / Remote). 
Requirements: Python, SQL, PowerBI, basic Excel macros. 
Salary: LKR 120,000 - 150,000 per month. 
Contact: careers@techlanka.lk"""
        
        job_text = st.text_area("Paste Job Posting:", value=default_job, height=150)
        
        if st.button("Extract & Evaluate", type="primary", use_container_width=True):
            prompt = f"""You are a Technical Recruiter specializing in Data Science and Analytics roles in Sri Lanka.
Extract information from the job posting below into a strict JSON object.

Additionally, calculate a "match_score" (0-100) representing how well this role matches a standard "Data Scientist" profile (which heavily weights Machine Learning, Python, SQL, and Statistical Modeling).

Output the JSON object.
JSON Schema:
{{
  "company_name": "string",
  "role": "string",
  "location": "string",
  "salary_range": "string",
  "required_skills": ["string"],
  "match_score": integer
}}

Job Posting:
\"\"\"
{job_text}
\"\"\"
"""
            with st.spinner("Parsing job requirements..."):
                raw_result = call_groq(prompt, temperature=0.0, max_tokens=8000)
            
            parsed_data, error = parse_json_response(raw_result)
            
            if parsed_data:
                st.subheader("Role Intelligence")
                
                # Top row: Company and Role
                c1, c2 = st.columns(2)
                c1.markdown(f"**Company:** {parsed_data.get('company_name', 'N/A')}")
                c2.markdown(f"**Role:** {parsed_data.get('role', 'N/A')}")
                
                # Middle row: Location and Salary
                c3, c4 = st.columns(2)
                c3.markdown(f"**Location:** {parsed_data.get('location', 'N/A')}")
                c4.markdown(f"**Salary:** {parsed_data.get('salary_range', 'N/A')}")
                
                st.divider()
                
                # Bottom row: Skills and Match Score
                c5, c6 = st.columns([2, 1])
                c5.markdown("**Required Skills:**")
                skills = parsed_data.get("required_skills", [])
                if skills:
                    st.write(", ".join([f"`{skill}`" for skill in skills]))
                else:
                    st.write("N/A")
                
                match_score = parsed_data.get("match_score", 0)
                c6.metric("Data Scientist Match", f"{match_score}%")
                
            else:
                st.error("⚠️ Failed to parse job data. Please try again.")
                with st.expander("View Raw Output for Debugging"):
                    st.code(error)

    with col2:
        st.info("💡 **Best for:** HR teams, talent acquisition, and candidates evaluating role fit.")