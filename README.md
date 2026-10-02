# 📊 LankaInsight AI
### AI-Powered Business Intelligence for the Sri Lankan Market

LankaInsight AI is a professional business intelligence tool designed to transform unstructured local business and economic data into actionable, structured insights. Built as a practical implementation of advanced LLM orchestration and prompt engineering, this tool helps analysts, product managers, and recruiters navigate the unique complexities of the Sri Lankan corporate landscape.

---

## 🖼️ Visual Preview

| News Briefer | Review Analyzer |
| :---: | :---: |
| ![News Briefer](ScreenShots/News%20Briefer.png) | ![Review Analyzer](ScreenShots/Review%20Analyzer.png) |
| **Zero-Shot Summarization** | **Few-Shot Classification** |
| | |
| **Impact Analyzer** | **Job Intelligence** |
| ![Impact](ScreenShots/Impact.png) | ![Job](ScreenShots/Job.png) |
| **Chain-of-Thought Reasoning** | **Structured JSON Extraction** |

---

## 🚀 Core Features

LankaInsight AI provides four specialized modules, each solving a distinct business problem using targeted AI patterns:

### 📰 Economic News Briefer
**The Problem:** High-volume economic news is often too dense for quick executive decision-making.
**The Solution:** Uses **Zero-Shot Generation** to synthesize raw market updates into three high-impact, executive-ready bullet points focusing on financial implications and strategic takeaways.

### ⭐ Customer Review Analyzer
**The Problem:** Customer feedback is unstructured and varies wildly in tone and category.
**The Solution:** Implements **Few-Shot Classification**. By providing the model with local context examples, it strictly categorizes feedback (e.g., Food, App, Service), assigns sentiment/severity, and generates a concrete recommended action.

### 📉 Business Impact Analyzer
**The Problem:** Economic policy changes (like new taxes) have complex ripple effects that are easy to overlook.
**The Solution:** Leverages **Chain-of-Thought (CoT) Reasoning**. The model is forced to generate an internal "Reasoning Process" before delivering a strategic assessment, significantly reducing hallucinations and increasing the logical depth of risk analysis.

### 💼 Job Post Intelligence
**The Problem:** Job descriptions are inconsistent, making it hard to quantitatively assess role alignment.
**The Solution:** Utilizes **Structured Output Parsing**. It enforces a strict JSON schema to extract company, role, and salary data, while calculating a `match_score` against a standard Data Science profile.

---

## 🛠️ Technical Implementation

This project was developed to practice and implement concepts from the **DeepLearning.AI** courses: *ChatGPT Prompt Engineering for Developers* and *Building Systems with the ChatGPT API*.

### Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io/) (for rapid UI deployment)
- **LLM Orchestration:** [Groq API](https://groq.com/) (utilizing ultra-fast inference)
- **Model:** `openai/gpt-oss-20b` (and Llama 3 variants during exploration)
- **Language:** Python 3.12

### Prompt Engineering Patterns
- **Zero-Shot:** Clear instructions with delimiters (`"""`) for immediate synthesis.
- **Few-Shot:** Providing `Input -> Output` pairs to steer tone and classification accuracy.
- **Chain-of-Thought:** Using "inner monologue" patterns to simulate expert strategic consulting.
- **Structured JSON:** Implementing strict schema enforcement for downstream data integration.

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.10+
- A Groq API Key ([Get one here](https://console.groq.com/))

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/LankaInsight-AI.git
   cd LankaInsight-AI
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment:**
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

### Running the Application
```bash
streamlit run app.py
```

---

## 👤 About the Author
**Visura Rodrigo**  
Passionate about bridging the gap between Large Language Models and real-world business applications in Sri Lanka.
