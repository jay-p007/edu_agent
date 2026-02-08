import streamlit as st
from agents import GeneratorAgent, ReviewerAgent

st.set_page_config(page_title="Agent Assessment Demo", layout="wide")

st.title("Agent-Based Educational Content Generator")

st.header("Input")

grade = st.slider("Select grade", 1, 10, 7)
topic = st.text_input("Topic", "Types of angles")

if st.button("Run"):
    generator = GeneratorAgent()
    reviewer = ReviewerAgent()

    st.subheader("Generator output")
    gen_output = generator.generate(grade, topic)
    st.json(gen_output)

    st.subheader("Reviewer feedback")
    review_output = reviewer.review(gen_output, grade)
    st.json(review_output)

    if review_output["status"] == "fail":
        st.subheader("Refined output")
        refined_output = generator.generate(
            grade,
            topic,
            feedback=review_output["feedback"]
        )
        st.json(refined_output)
    else:
        st.success("Content passed review. No refinement needed.")
