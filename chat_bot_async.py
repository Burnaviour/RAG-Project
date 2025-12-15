from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from dotenv import load_dotenv
import sqlite3
import requests
import os
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
load_dotenv()

client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio",
            "command": "python3",
            "args": ["/home/burnaviour/LANGRAG/mcp_server_main.py"],
        },
        # "expense": {
        #     "transport": "streamable_http",  # if this fails, try "sse"
        #     "url": "https://splendid-gold-dingo.fastmcp.app/mcp"
        # }
    }
)


# -------------------
# 1. LLM
# -------------------

# LLM Configuration - DeepSeek R1 Distill Qwen 7B
LLAMA_STUDIO_API_BASE = os.getenv("LLAMA_STUDIO_API_BASE", "http://localhost:1234/v1")
LLAMA_STUDIO_API_KEY = os.getenv("LLAMA_STUDIO_API_KEY", "lm-studio")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "deepseek-r1-distill-qwen-7b")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "2048"))
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))  # Timeout in seconds
LLM_MAX_RETRIES = int(os.getenv("LLM_MAX_RETRIES", "2"))  # Number of retries

llm = ChatOpenAI(
    base_url=LLAMA_STUDIO_API_BASE,
    api_key=LLAMA_STUDIO_API_KEY,
    model=LLM_MODEL_NAME,
    temperature=LLM_TEMPERATURE,
    max_tokens=LLM_MAX_TOKENS,
    timeout=LLM_TIMEOUT,
    max_retries=LLM_MAX_RETRIES,
)


# -------------------
# 2. Tools
# -------------------
# Tools
search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}

        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}




@tool
def get_stock_price(symbol: str) -> dict:
    """
    Fetch latest stock price for a given symbol (e.g. 'AAPL', 'TSLA')
    using Alpha Vantage with API key in the URL.
    """
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=LJ3BBKRVAVOYKXE2"
    r = requests.get(url)
    return r.json()





class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]



async def build_graph():

    tools = await client.get_tools()
    print(tools)
    llm_with_tools = llm.bind_tools(tools)
    chatbot = ''
    async def chat_node(state: ChatState):
        """LLM node that may answer or request a tool call."""
        messages = state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        return {"messages": [response]}

    tool_node = ToolNode(tools)

    graph = StateGraph(ChatState)
    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "chat_node")

    graph.add_conditional_edges("chat_node",tools_condition)
    graph.add_edge('tools', 'chat_node')

    chatbot = graph.compile()
    return chatbot

async def main():
    chat_bot = await build_graph()
    res =await chat_bot.ainvoke({"messages":[HumanMessage(content="Find the modulus of 5 and 23 and give answer like a cricket commentator.")]})

    print(res['messages'][-1].content)

if __name__ == '__main__':
    asyncio.run(main())

