
import logging
import os
import time

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("task_agent")

search_tool = DuckDuckGoSearchRun()

PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a research assistant. Use the supplied web results "
        "to write exactly three concise bullet points. Do not invent "
        "facts. Mention source names or URLs when available. "
        "If evidence is insufficient, state that limitation."
    ),
    (
        "human",
        "Research topic: {topic}\n\n"
        "Search results:\n{results}\n\n"
        "Return exactly three bullet points."
    ),
])


def validate_topic(topic):
    if not isinstance(topic, str):
        raise ValueError("Topic must be text.")

    topic = topic.strip()

    if not topic:
        raise ValueError("Please enter a research topic.")

    if len(topic) > 200:
        raise ValueError("Topic must be 200 characters or fewer.")

    return topic


def build_prompt(topic, results):
    return PROMPT.format_messages(topic=topic, results=results)


def research_topic(topic):
    topic = validate_topic(topic)
    start_time = time.perf_counter()

    logger.info("Research request received: %s", topic)

    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not configured.")

        results = search_tool.invoke(topic)

        if not results or not str(results).strip():
            raise RuntimeError("The web search returned no results.")

        model_name = os.getenv(
            "GROQ_MODEL", "llama-3.3-70b-versatile"
        )

        llm = ChatGroq(
            model=model_name,
            temperature=0,
            timeout=45,
            max_retries=1,
            api_key=api_key,
        )

        response = llm.invoke(
            build_prompt(topic, str(results))
        )

        brief = response.content

        if not isinstance(brief, str) or not brief.strip():
            raise RuntimeError("The model returned an empty brief.")

        elapsed = time.perf_counter() - start_time
        logger.info(
            "Research request completed in %.2f seconds", elapsed
        )

        return brief.strip(), elapsed

    except Exception:
        elapsed = time.perf_counter() - start_time
        logger.exception(
            "Research request failed after %.2f seconds", elapsed
        )
        raise
