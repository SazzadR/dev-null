from dotenv import load_dotenv
from ollama import ChatResponse, chat

load_dotenv()

MAX_RETRIES = 10
MODEL = "qwen3:4b"


def get_product_price(product: str) -> float:
    """Look up the price of a product in the catalog.

    Args:
          product (str): The name of the product.

    Returns:
        float: The price of the product.
    """
    print(f"    >>> Executing get_product_price(product='{product}')")
    prices = {"laptop": 1299.99, "headphones": 149.95, "keyboard": 89.50}
    return prices.get(product, 0)


def apply_discount(price: float, discount_tier: str) -> float:
    """Apply a discount tier to a price and return the final price. Available tiers: bronze, silver, gold.

    Args:
        price (float): The price of the product.
        discount_tier (str): The discount tier.

    Returns:
        float: The final price after applying the discount tier.
    """
    print(f"    >>> Executing apply_discount(price={price}, tier={discount_tier})")
    discount_percentage = {"bronze": 5, "silver": 10, "gold": 15}
    discount = discount_percentage.get(discount_tier, 0)
    return round((price * (100 - discount) / 100), 2)


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Look up the price of a product in the catalog.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "The product name, e.g. 'laptop', 'headphones', 'keyboard'",
                    },
                },
                "required": ["product"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "apply_discount",
            "description": "Apply a discount tier to a price and return the final price. Available tiers: bronze, silver, gold.",
            "parameters": {
                "type": "object",
                "properties": {
                    "price": {"type": "number", "description": "The original price"},
                    "discount_tier": {
                        "type": "string",
                        "description": "The discount tier: 'bronze', 'silver', or 'gold'",
                    },
                },
                "required": ["price", "discount_tier"],
            },
        },
    },
]


def run_agent(question: str):
    tools_dict = {
        "get_product_price": get_product_price,
        "apply_discount": apply_discount,
    }

    print(f"Question: {question}")
    print("=" * 50)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful shopping assistant. "
                "You have access to a product catalog tool "
                "and a discount tool.\n\n"
                "STRICT RULES - you must follow these exactly:\n"
                "1. NEVER guess or assume any product price. "
                "You MUST call get_product_price first to get the real price.\n"
                "2. Only call apply_discount AFTER you have received "
                "a price from get_product_price. Pass the exact price "
                "returned by get_product_price - do NOT pass a made-up number.\n"
                "3. NEVER calculate discounts yourself using math. "
                "Always use the apply_discount tool.\n"
                "4. If the user does not specify a discount tier, "
                "ask them which tier to use - do NOT assume one."
            ),
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    for iteration in range(1, MAX_RETRIES + 1):
        print(f"\n--- Iteration {iteration} ---")

        response: ChatResponse = chat(model=MODEL, messages=messages, tools=tools)
        ai_message = response.message
        tool_calls = ai_message.tool_calls

        if not tool_calls:
            print(f"\nFinal Answer: {ai_message.content}")
            return ai_message.content

        tool_call = tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = tool_call.function.arguments
        print(f"    [Tool Selected] {tool_name} with args: {tool_args}")

        tool_to_use = tools_dict.get(tool_name)
        if not tool_to_use:
            raise ValueError(f"Tool '{tool_name}' not found.")

        observation = tool_to_use(**tool_args)
        print(f"    [Tool Result] {observation}")

        messages.append(ai_message)
        messages.append(
            {"role": "tool", "tool_name": tool_name, "content": str(observation)}
        )

    print("ERROR: Max iterations reached without a final answer")
    return None
