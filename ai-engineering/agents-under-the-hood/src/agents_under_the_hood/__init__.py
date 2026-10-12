import argparse

from . import langchain_tool_calling


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--example",
        choices=["langchain-tool-calling"],
        default="langchain-tool-calling",
        help="Example ReAct loop.",
    )
    args = parser.parse_args()

    if args.example == "langchain-tool-calling":
        langchain_tool_calling.run_agent(
            "What is the price of a laptop after applying a gold discount?"
        )
