from typing import List

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field

load_dotenv()


class Source(BaseModel):
    """Schema for a source used by the agent"""

    url: str = Field(description="The URL of the source.")


class AgentResponse(BaseModel):
    """Schema for agent response with answer and sources"""

    answer: str = Field(description="The agent's answer to the query.")
    source: List[Source] = Field(
        default_factory=list, description="List of sources used to generate the answer."
    )


def main() -> None:
    user_input = input("Enter your message (write \\q to quit): ")
    user_input = user_input.strip()
    if user_input == "\\q":
        exit(0)

    human_message = HumanMessage(user_input)

    llm = ChatOpenAI(model="gpt-6-luna")
    agent = create_agent(
        model=llm, tools=[TavilySearch()], response_format=AgentResponse
    )
    response = agent.invoke({"messages": [human_message]})
    result: AgentResponse = response["structured_response"]

    print("#" * 20)
    print(f"Result: {result.answer}")
    print("Source:")
    for source in result.source:
        print(source)
    print("#" * 20)
