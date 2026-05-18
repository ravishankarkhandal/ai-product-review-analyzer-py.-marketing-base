import streamlit as st
from collectors import collect_all_reviews
from analyzer import generate_final_review

st.set_page_config(page_title="AI Product Review Analyzer", page_icon="🔍", layout="wide")

st.title("🔍 AI Product Review Analyzer")
st.markdown("Analyze product reviews from **Google, YouTube, and Amazon** using **Gemini & Groq AI**.")

product = st.text_input("Enter product name (e.g., iPhone 15, Sony WH-1000XM5):")

if st.button("Analyze Product"):
    if not product.strip():
        st.error("⚠️ Product name cannot be empty!")
    else:
        # Step 1: Data Collection
        with st.spinner(f"🔍 Collecting reviews for '{product}'..."):
            reviews = collect_all_reviews(product)
        
        # Step 2: AI Analysis
        with st.spinner("🤖 AI Analysis in progress..."):
            result = generate_final_review(product, reviews)
        
        # Step 3: Show Output
        if "error" in result:
            st.error(f"❌ {result['error']}")
        else:
            st.success(f"✅ Analyzed {result['total_reviews_analyzed']} reviews from {', '.join(result['sources'])}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("✨ Gemini AI Analysis")
                st.markdown(result["gemini_analysis"])
                
            with col2:
                st.subheader("⚡ Groq AI Analysis")
                st.markdown(result["groq_analysis"])
            
            st.divider()
            st.header("🚀 STEP 4 — MARKETING OUTPUT")
            st.markdown(result["marketing_content"])

            if result.get("links"):
                st.divider()
                st.subheader("🔗 Source Links")
                for idx, link in enumerate(result["links"], 1):
                    st.markdown(f"{idx}. [{link}]({link})")