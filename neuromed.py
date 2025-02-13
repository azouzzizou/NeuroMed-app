import streamlit as st
import time
import pandas as pd
import json
from PIL import Image

# Set up the page
st.set_page_config(
    page_title="Medical Research Assistant",
    page_icon="🔬",
    layout="wide"
)

# Custom CSS styling
st.markdown("""
<style>
    /* Main search styling */
    .main-search {
        font-size: 20px !important;
        padding: 15px !important;
        margin-top: 2rem !important;
    }
    
    /* Talan sidebar styling */
    .talan-header {
        padding: 1.5rem;
        background: linear-gradient(135deg, #2e86c1, #1b4f72);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .talan-logo {
        max-width: 180px;
        margin-bottom: 1rem;
    }
    .sidebar-link {
        color: #2e86c1 !important;
        text-decoration: none;
        font-weight: 500;
    }
    .sidebar-link:hover {
        text-decoration: underline;
    }
    .sidebar-section {
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None
if "show_qa" not in st.session_state:
    st.session_state.show_qa = False
if "selected_url" not in st.session_state:
    st.session_state.selected_url = None
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# Mock data
MOCK_DATA = {
    "topic": "Diabetes Treatment",
    "summary": "Recent advancements in diabetes treatment include GLP-1 receptor agonists and SGLT2 inhibitors which improve glycemic control and reduce cardiovascular risks.",
    "urls": {
        "Study 1 (2023)": {
            "url": "https://example.com/diabetes-study1",
            "details": "A 2023 clinical trial on GLP-1 receptor agonists involving 5,000 patients."
        },
        "Clinical Trial Report": {
            "url": "https://example.com/diabetes-trial2023",
            "details": "Phase 3 trial comparing SGLT2 inhibitors with placebo across 20 countries."
        }
    },
    "qa": {
        "What are GLP-1 receptor agonists?": "GLP-1 receptor agonists are a class of medications that enhance insulin secretion and promote weight loss.",
        "What are common side effects?": "Most common side effects include nausea (30%), vomiting (15%), and diarrhea (12%).",
        "Long-term safety profile?": "Studies show good safety profile for up to 4 years of continuous use with proper monitoring."
    }
}

# --------------------------------------------
# Sidebar - Talan Information (Always visible)
# --------------------------------------------
with st.sidebar:
    # Talan Logo
    try:
        talan_logo = Image.open("talan-logo.png")
        st.image("talan-logo.png", use_container_width=True)

    except FileNotFoundError:
        st.warning("Talan logo image not found")

    # Talan Header
    st.markdown("""
    <div class='talan-header'>
        <h2>TAVAN</h2>
        <h4>Positive Innovation</h4>
    </div>
    """, unsafe_allow_html=True)

    # About Section
    st.markdown("""
    ### About Talan
    **Talan Consulting** - Global leader in technology innovation:
    - 🚀 Digital Transformation Experts
    - 🤖 AI & Advanced Analytics
    - 🌍 Sustainable Tech Solutions
    - 🔒 Cybersecurity Specialists
    
    **2023 Achievements:**
    - 📈 €600M Annual Revenue
    - 🌐 5,000+ Professionals
    - 🏆 22 Industry Awards
    
    [🌐 Official Website](https://www.talan.com)
    """)

    # Researcher Section
    st.markdown("""
    ### Research Collaboration
    Partner with Talan Innovation Lab:
    - 🔍 Cutting-edge Tools Access
    - 🤝 Collaborative Projects
    - 📚 Research Grants
    - 📊 Big Data Infrastructure
    
    ✉️ [Contact Research Team](mailto:research@talan.com)
    """)

# --------------------------------------------
# Main Content Area
# --------------------------------------------
if not st.session_state.analysis_data:
    # Landing Page
    st.title("Medical Research Intelligence Platform")
    st.markdown("""
    **AI-Powered Insights for Healthcare Professionals**  
    Start by searching any medical term below
    """)
    
    # Main Search Bar
    search_query = st.text_input(
        "🔍 Search medical topics (e.g., 'Diabetes Treatment', 'Cancer Immunotherapy')",
        key="landing_search",
        label_visibility="collapsed",
        placeholder="Enter medical term or concept..."
    )
    
    if search_query:
        st.session_state.search_query = search_query
        with st.spinner(f"Analyzing research for '{search_query}'..."):
            time.sleep(2)
            st.session_state.analysis_data = MOCK_DATA
        st.rerun()

else:
    # Analysis Page (unless in Q&A)
    if not st.session_state.show_qa:
        # Persistent Search Bar
        new_search = st.text_input(
            "🔍 Search new term or refine query",
            value=st.session_state.search_query,
            key="analysis_search",
            label_visibility="collapsed"
        )
        
        if new_search != st.session_state.search_query:
            st.session_state.search_query = new_search
            st.session_state.analysis_data = None
            st.rerun()
        
        # Analysis Content
        st.header(f"Analysis for '{st.session_state.analysis_data['topic']}'")
        
        # Summary Section
        st.subheader("Executive Summary")
        st.write(st.session_state.analysis_data["summary"])
        
        # Research Papers
        st.subheader("Key Research Papers")
        for name, data in st.session_state.analysis_data["urls"].items():
            with st.expander(f"📄 {name}"):
                st.write(data["details"])
                if st.button(f"Ask Questions about {name}", key=f"btn_{name}"):
                    st.session_state.selected_url = data["url"]
                    st.session_state.show_qa = True
                    st.rerun()

# --------------------------------------------
# Q&A Interface
# --------------------------------------------
if st.session_state.show_qa:
    # Q&A Page
    st.header(f"Research Q&A: {st.session_state.analysis_data['topic']}")
    st.caption(f"Analyzing: {st.session_state.selected_url}")
    
    # Back Navigation
    if st.button("← Back to Analysis"):
        st.session_state.show_qa = False
        st.session_state.messages = []
        st.rerun()
    
    # Chat Interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about this research..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Generate Response
        ai_response = st.session_state.analysis_data["qa"].get(
            prompt, 
            "I couldn't find a specific answer in this research. Please try rephrasing your question."
        )
        
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        st.rerun()