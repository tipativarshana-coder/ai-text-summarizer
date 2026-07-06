import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

client = Groq(api_key=api_key)

st.set_page_config(page_title="AI Text Summarizer")
st.markdown("""
<style>

.main {
    background-color:#0E1117;
}

h1 {
    color:#4F8BF9;
    text-align:center;
}

.stButton>button {
    background:#4F8BF9;
    color:white;
    border-radius:12px;
    height:50px;
    width:100%;
    font-size:18px;
    border:none;
}

.stButton>button:hover{
    background:#2563EB;
}

textarea{
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    style = st.selectbox(
        "Choose Summary Style",
        [
            "Bullet Points",
            "Short Paragraph",
            "Detailed"
        ]
    )

    st.markdown("---")
    st.write("Made by Varshana ❤️")

# Title
st.markdown("""
<h1>🧠 SummarizeAI</h1>

<p style='text-align:center;font-size:20px;'>
AI Powered Text Summarizer
</p>

""",unsafe_allow_html=True)
st.markdown(
    "Generate quick, accurate summaries of articles, essays, reports, and notes using AI."
)

# Text input
text = st.text_area(
    "Paste your text below",
    placeholder="Paste an article, meeting notes, blog post, research paper...",
    height=250
)

# Word count
if text:
    st.info(f"📝 Word Count: {len(text.split())} words")

# Clear button
if st.button("🗑️ Clear"):
    st.rerun()

# Summarize button
if st.button("✨ Summarize"):

    if text.strip() == "":
        st.warning("Please enter some text.")

    else:

        prompt = f"""
        Summarize the following text in {style}.

        Text:
        {text}
        """

        with st.spinner("🤖 AI is reading your text..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI summarizer."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
            )

        summary = response.choices[0].message.content

        st.subheader("📄 Summary")
        st.success(summary)

        st.download_button(
            label="📥 Download Summary",
            data=summary,
            file_name="summary.txt",
            mime="text/plain"
        )
        uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)
from pypdf import PdfReader

reader = PdfReader(uploaded_file)

text = ""

for page in reader.pages:
    text += page.extract_text()