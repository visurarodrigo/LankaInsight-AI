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

def call_groq(prompt, temperature, max_tokens):
    """Sends prompt to Groq and returns the text response."""
    client = get_groq_client()
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
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
            return json.loads(json_str), None
        except json.JSONDecodeError:
            return None, json_str
    return None, raw_text

# --- Custom Fonts ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700&display=swap');

/* Main application font */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* LankaInsight AI title */
.lanka-title {
    font-family: 'DM Serif Display', serif;
    font-size: 4.2rem;
    font-weight: 400;
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 0;
}

/* Subtitle */
.lanka-caption {
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    font-weight: 400;
    margin-top: 4px;
    margin-bottom: 24px;
    opacity: 0.7;
}
</style>
""", unsafe_allow_html=True)


# --- 3. UI HEADER ---
st.markdown(
    '<div class="lanka-title">LankaInsight AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="lanka-caption">AI-Powered Business Intelligence for the Sri Lankan Market</div>',
    unsafe_allow_html=True
)

# --- Sidebar Font Styling ---
st.markdown("""
<style>
/* Sidebar body text */
[data-testid="stSidebar"] p {
    font-size: 0.85rem;
}

/* Sidebar headings */
[data-testid="stSidebar"] h1 {
    font-size: 1.5rem;
}

[data-testid="stSidebar"] h2 {
    font-size: 1.2rem;
}

[data-testid="stSidebar"] h3 {
    font-size: 1rem;
}

/* Sidebar list items */
[data-testid="stSidebar"] li {
    font-size: 0.82rem;
}
</style>
""", unsafe_allow_html=True)


# --- 4. SIDEBAR (Portfolio Context) ---
with st.sidebar:
    st.header("About LankaInsight")

    st.markdown("""
    LankaInsight is a practical business intelligence tool designed for Sri Lankan analysts, product managers, and recruiters. 
    It transforms unstructured local business data into actionable, structured insights in seconds.
    """)

    st.subheader("⚙️ How it Works")

    st.markdown("""
    Under the hood, this application leverages advanced Large Language Model (LLM) architectures and prompt engineering techniques to ensure high accuracy and reliability:
    
    * **Zero-Shot Generation:** Used in the News Briefer to synthesize complex economic data without prior examples.
    * **Few-Shot Classification:** Powers the Review Analyzer by providing the model with contextual examples to ensure strict adherence to local business categories.
    * **Chain-of-Thought Reasoning:** The Impact Analyzer forces the model to reason step-by-step internally before generating strategic recommendations, significantly reducing hallucinations.
    * **Structured Output Parsing:** The Job Intelligence feature enforces strict JSON schemas, allowing seamless integration with downstream HR databases.
    """)

    st.caption("Built by Visura Rodrigo")

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

    # Header + Info Box
    header_col, info_col = st.columns([1, 1])

    with header_col:
        st.header("Economic News Briefer")
        st.markdown(
            "Transform raw economic updates into concise, executive-ready summaries."
        )

    with info_col:
        st.info(
            "💡 **Best for:** Daily market monitoring, "
            "investor updates, and quick strategic alignment."
        )

    # News Input
    default_news = """The Central Bank of Sri Lanka reported that inflation eased to 4.5% in August, down from 5.1% in July, driven by lower food and energy prices. However, the bank warned that global supply chain disruptions could cause minor fluctuations in the coming quarter. The rupee has remained relatively stable against the US dollar, and foreign reserves have increased to $3.2 billion."""

    news_text = st.text_area(
        "Paste Economic News or Headlines:",
        value=default_news,
        height=140,
        width="stretch" 
    )

    if st.button(
        "Generate Brief",
        type="primary",
        use_container_width=True
    ):

        prompt = f"""You are a Senior Business Analyst for a top-tier consulting firm in Sri Lanka.

Summarize the following economic news text into exactly 3 concise, high-impact bullet points tailored for C-suite executives.

Focus on financial implications, market trends, and strategic takeaways. Do not include introductory or concluding text.

Text:

\"\"\"
{news_text}
\"\"\"
"""

        with st.spinner("Synthesizing market data..."):
            result = call_groq(
                prompt,
                temperature=0.2,
                max_tokens=8000
            )

        st.subheader("Executive Summary")
        st.write(result)

# ==========================================
# FEATURE 2: CUSTOMER REVIEW ANALYZER
# ==========================================
with tab2:
    header_col, info_col = st.columns([1, 1])

    with header_col:
        st.header("Customer Review Analyzer")
        st.markdown("Instantly categorize, score, and generate action plans for customer feedback.")

    with info_col:
        st.info("💡 **Best for:** QA teams, branch managers, and app developers monitoring user sentiment.")
    
    col1 = st.container()
    
    with col1:
        default_review = "I waited 45 minutes at the Commercial Bank branch in Nugegoda just to deposit a cheque, and the teller was incredibly rude when I asked about the delay. The app also crashed twice while I was trying to check my balance beforehand."
        
        review_text = st.text_area("Paste Customer Review:", value=default_review, height=140, width="stretch")
        
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

# ==========================================
# FEATURE 3: BUSINESS IMPACT ANALYZER
# ==========================================
with tab3:
    header_col, info_col = st.columns([1, 1])

    with header_col:
        st.header("Business Impact Analyzer")
        st.markdown("Evaluate strategic risks and operational impacts of local economic events.")

    with info_col:
        st.info("💡 **Best for:** Strategy teams, policy analysts, and board-level risk assessments.")
    
    col1 = st.container()
    
    with col1:
        default_scenario = "The Sri Lankan government introduces a new 15% digital services tax on all foreign SaaS platforms (like AWS, Slack, and Adobe) starting next quarter."
        
        scenario_text = st.text_area("Describe Business Scenario or Economic Event:", value=default_scenario, height=120, width="stretch"     )        
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

# ==========================================
# FEATURE 4: JOB POST INTELLIGENCE
# ==========================================

with tab4:

    # Header + Info Box
    header_col, info_col = st.columns([1, 1])

    with header_col:
        st.header("Job Post Intelligence")
        st.markdown(
            "Extract structured information and evaluate overall role alignment from job postings."
        )

    with info_col:
        st.info(
            "💡 **Best for:** HR teams, talent acquisition, "
            "and candidates evaluating job opportunities."
        )

    # Job Posting Input
    default_job = """Wanted: Junior Data Analyst at TechLanka Solutions.
Location: Hybrid (Colombo 03 / Remote).
Requirements: Python, SQL, PowerBI, basic Excel macros.
Salary: LKR 120,000 - 150,000 per month.
Contact: careers@techlanka.lk"""

    job_text = st.text_area(
        "Paste Job Posting:",
        value=default_job,
        height=150,
        width="stretch"
    )

    if st.button(
        "Extract & Evaluate",
        type="primary",
        use_container_width=True
    ):

        prompt = f"""You are a Technical Recruiter and Job Market Analyst.

Analyze the job posting below and extract the key information into a strict JSON object.

The analysis should be role-independent and suitable for different types of jobs, including Data Science, Analytics, Software Engineering, Business, IT, Marketing, Finance, and other professional roles.

Calculate a "match_score" (0-100) representing the overall alignment of the job opportunity with the requirements, skills, experience, and qualifications stated in the job posting.

Do not assume the role is a Data Scientist or any other specific profession.

Output the JSON object.

JSON Schema:

{{
  "company_name": "string",
  "role": "string",
  "location": "string",
  "employment_type": "string",
  "salary_range": "string",
  "required_skills": ["string"],
  "experience_required": "string",
  "education_required": "string",
  "match_score": integer
}}

Job Posting:

\"\"\"
{job_text}
\"\"\"
"""

        with st.spinner("Parsing job requirements..."):

            raw_result = call_groq(
                prompt,
                temperature=0.0,
                max_tokens=8000
            )

        parsed_data, error = parse_json_response(raw_result)

        if parsed_data:

            st.subheader("Role Intelligence")

            # ------------------------------------------
            # Company and Role
            # ------------------------------------------

            c1, c2 = st.columns(2)

            with c1:
                st.markdown(
                    f"**Company:** "
                    f"{parsed_data.get('company_name', 'N/A')}"
                )

            with c2:
                st.markdown(
                    f"**Role:** "
                    f"{parsed_data.get('role', 'N/A')}"
                )

            # ------------------------------------------
            # Location and Employment Type
            # ------------------------------------------

            c3, c4 = st.columns(2)

            with c3:
                st.markdown(
                    f"**Location:** "
                    f"{parsed_data.get('location', 'N/A')}"
                )

            with c4:
                st.markdown(
                    f"**Employment Type:** "
                    f"{parsed_data.get('employment_type', 'N/A')}"
                )

            # ------------------------------------------
            # Salary and Experience
            # ------------------------------------------

            c5, c6 = st.columns(2)

            with c5:
                st.markdown(
                    f"**Salary:** "
                    f"{parsed_data.get('salary_range', 'N/A')}"
                )

            with c6:
                st.markdown(
                    f"**Experience Required:** "
                    f"{parsed_data.get('experience_required', 'N/A')}"
                )

            # ------------------------------------------
            # Education + Match Score
            # ------------------------------------------

            c7, c8 = st.columns([2, 1])

            with c7:
                st.markdown("**Education Required:**")

                st.write(
                    parsed_data.get(
                        "education_required",
                        "N/A"
                    )
                )

            with c8:
                match_score = parsed_data.get(
                    "match_score",
                    0
                )

                st.metric(
                    "Role Match",
                    f"{match_score}%"
                )

            # ------------------------------------------
            # Required Skills
            # ------------------------------------------

            st.markdown("**Required Skills:**")

            skills = parsed_data.get(
                "required_skills",
                []
            )

            if skills:
                st.write(
                    " • ".join(
                        [f"`{skill}`" for skill in skills]
                    )
                )
            else:
                st.write("N/A")

        else:

            st.error(
                "⚠️ Failed to parse job data. Please try again."
            )

            with st.expander(
                "View Raw Output for Debugging"
            ):
                st.code(error)