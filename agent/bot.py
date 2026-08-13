import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from tools.weather import get_weather
from tools.notion_notes import get_notes, add_note
from tools.notion_calendar import get_calendar_events, add_calendar_events
from utils.logger import get_logger

logger = get_logger(__name__) ##agent.bot

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("groq api key not set")
        raise ValueError("groq api key not set")
    
    return ChatGroq(
        model = "openai/gpt-oss-120b",
        api_key = api_key
    )

def create_react_agent_custom():
    logger.info("Initialising agent")
    llm = get_llm()

    tools = [get_weather, get_notes, add_note, get_calendar_events, add_calendar_events]

    try:
        agent = create_agent(model=llm,tools=tools)
        logger.info("Agent Initialised")
        return agent
    except TypeError as e:
        logger.error(f"failed to create agent: {e}")
        raise e
