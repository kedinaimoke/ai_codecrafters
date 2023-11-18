import openai
from tqdm import tqdm
import os
from dotenv import load_dotenv
import subprocess
import sys
from openai import OpenAI

load_dotenv()

api_key = os.getenv("API_KEY")

client = OpenAI(
    api_key=api_key,
)


def run_python_code(code):
    """
    Executes the provided Python code and returns the output or error message.

    Args:
        code (str): The Python code to execute.

    Returns:
        tuple: A tuple containing a boolean indicating success and the corresponding output or error message.
    """
    try:
        # Execute the code using subprocess
        output = subprocess.check_output(["python3", "-c", code], stderr=subprocess.STDOUT, text=True)

        return True, output
    except subprocess.CalledProcessError as e:
        # Capture the error output
        error_output = e.output

        return False, error_output
    except Exception as e:
        # Handle unexpected exceptions
        error_output = str(e)

        return False, error_output


def fix_python_code(code, error_output):
    """
    Utilizes OpenAI's gpt 3.5 turbo engine to generate suggestions for fixing the provided Python code.

    Args:
        code (str): The Python code to fix.
        error_output (str): The error message associated with the code execution.

    Returns:
        str: The suggested fix for the code or an error message if no valid response is received from the model.
    """
    prompt = (
        "Here is Python code and an error message in Terminal:\n\n"
        f"{code}\n\n{error_output}\n\nPlease fix the code."
    )

    try:
        response = client.chat.completions.create(
            messages=[
                        {
                            "role": "user",
                            "content": f"Take a look at the error {error_output} and debug the code {code}",
                        },
                        # {
                        #     "role": "assistant",
                        #     "content": comment,
                        # }
                    ],
                    model="gpt-3.5-turbo",
                    )

        if "choices" in response and response["choices"]:
            return response["choices"][0]["text"]
        else:
            return "Unable to get a valid response from the model."

    except Exception as e:
        return f"An error occurred: {str(e)}"


def auto_debug_python():
    """
    Continuously prompts the user for Python code, executes it, and provides suggested fixes for any errors encountered.
    """
    max_attempts = 5

    while True:
        # Accept Python code snippet as user input
        code = input("Enter Python code:\n")

        for attempt in range(1, max_attempts + 1):
            success, output = run_python_code(code)

            if success:
                print("The Python script ran successfully!")
                break
            else:
                print(f"Attempt {attempt}: Error encountered while running the script:")
                print(output)

                # Generate a suggested fix
                fixed_code = fix_python_code(code, output)
                print(f"GPT-3.5 turbo suggested fix:\n{fixed_code}\n")

                # Prompt the user to apply the suggested fix
                apply_fix = input("Do you want to apply the suggested fix? (y/n): ")
                if apply_fix.lower() == "y":
                    code = fixed_code

        if not success:
            print("Maximum number of attempts reached. Please try fixing the script manually or run AutoDebug again.")


if __name__ == "__main__":
    auto_debug_python()
