from fastapi import FastAPI
from dotenv import load_dotenv
import os
import openai
import json
import math

# Load environment variables
load_dotenv()

app = FastAPI()

# Define a simple tool to calculate the square root
def calculate_square_root(number: float) -> float:
    if number < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return math.sqrt(number)

@app.get("/")
async def root():
    # Initialize the OpenAI client
    client = openai.OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.environ.get('GROK_API')
    )

    # Define the function as a tool for the model to use
    function_definition = {
        "name": "calculate_square_root",
        "description": "Calculate the square root of a number.",
        "parameters": {
            "type": "object",
            "properties": {
                "number": {
                    "type": "number",
                    "description": "The number to calculate the square root of."
                }
            },
            "required": ["number"]
        }
    }

    # Create a system prompt to instruct the model
    system_prompt = {
        "role": "system",
        "content": (
            "You are an AI assistant that can perform various tasks, including mathematical calculations. "
            "If a user asks for the square root of a number, use the 'calculate_square_root' function."
        )
    }

    # Example user message
    user_message = {"role": "user", "content": "What is the square root of 16?"}

    # Call the OpenAI API with the tool and prompt
    chat_completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[system_prompt, user_message],
        functions=[function_definition],
        function_call="auto"  # Let the model decide when to call the function
    )

    # Get the response
    response = chat_completion.choices[0]

    if response.finish_reason == 'function_call':
        function_call = response.message.function_call
        return {"message": "Hello World", "content": function_call}

    # # Check if the model wants to call a function
    # if response['function_call']:
    #     function_name = response['function_call']['name']
    #     function_arguments = json.loads(response['function_call']['arguments'])

    #     # Call the appropriate function
    #     if function_name == "calculate_square_root":
    #         number = function_arguments.get("number", 0)
    #         result = calculate_square_root(number)
    #         return {"message": f"The square root of {number} is {result}"}

    # If no function is called, return the model's message
    return {"message": "Hello World", "content": response}
