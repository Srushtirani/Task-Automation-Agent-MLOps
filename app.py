
import logging
import streamlit as st

from agent import research_topic

logger = logging.getLogger("task_agent")

st.set_page_config(
    page_title="Task Automation Agent",
    page_icon="🔎",
    layout="centered",
)

st.title("🔎 Task-Automation Research Agent")
st.write(
    "Enter a topic to search the web and generate a "
    "three-point research brief."
)

topic = st.text_input(
    "Research topic",
    placeholder="Example: Recent developments in AI",
    max_chars=200,
)

if st.button("Research Topic", type="primary"):
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        try:
            with st.spinner(
                "Searching the web and preparing your brief..."
            ):
                brief, elapsed = research_topic(topic)

            st.subheader("Research Brief")
            st.markdown(brief)
            st.caption(f"Request completed in {elapsed:.2f} seconds.")

        except Exception:
            st.error(
                "The request failed. Check the application "
                "configuration and logs, then try again."
            )

st.divider()
st.caption("Powered by LangChain, DuckDuckGo and OpenAI.")
