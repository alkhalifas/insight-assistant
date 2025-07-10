# agent.py
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import pandas as pd

def ppt_search(query, ppt_text):
    if query.lower() in ppt_text.lower():
        return "✅ Found relevant info in PowerPoint slides."
    return "⚠️ No relevant information found in PowerPoint."

def dataframe_query(query, df):
    try:
        result = df.query(query)
        if not result.empty:
            return f"✅ Found matching data:\n{result.to_string(index=False)}"
        else:
            return "⚠️ No matching data found in DataFrame."
    except Exception:
        return "⚠️ Could not process your query. Please check your syntax."

def dataframe_eval(query, df):
    try:
        # Evaluate the query in a restricted environment
        result = eval(query, {"__builtins__": {}}, {"df": df, "pd": pd})
        if result is not None:
            return str(result)
        else:
            return "⚠️ Query returned no result."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def make_tools(ppt_text, df):
    return [
        Tool(
            name="PowerPointSearch",
            func=lambda q: ppt_search(q, ppt_text),
            description="Searches the PowerPoint slides for keywords or phrases."
        ),
        Tool(
            name="DataFrameEval",
            func=lambda q: dataframe_eval(q, df),
            description="Run Python expressions on the DataFrame (use variable `df`)."
        )
    ]


def build_agent(ppt_text, df):
    tools = make_tools(ppt_text, df)
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
    return agent
