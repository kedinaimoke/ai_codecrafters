from code_review.code_review import (add_code_tags, generate_comment, create_html_output, get_diff_changes_from_pipeline, main as code_review_main,)
from code_test_case.code_test_case import code_test_case
from code_debug.code_debug import run_python_code, fix_python_code, auto_debug_python

def get_developer_input():
    """
    Retrieves the developer's input code from manual input.

    Returns:
        str: The code entered by the developer.

    """
    import re
    developer_input = input("Please enter your code:")
    matches = re.finditer(r"`(.+?)`", developer_input)

    updated_chunks = []
    last_end = 0
    for match in matches:
        updated_chunks.append(developer_input[last_end : match.start()])
        updated_chunks.append("<b>`{}`<\b>".format(match.group(1)))
        last_end = match.end()
    updated_chunks.append(developer_input[last_end:])
    return "".join(updated_chunks)


def generate_diff(base_code, developer_input):
    """
    Generates a unified diff between two code snippets.

    Args:
        base_code (str): The original code.
        developer_input (str): The code entered by the developer.

    Returns:
        str: The unified diff.
    """
    from difflib import unified_diff

    base_lines = base_code.splitlines(keepends=True)
    developer_lines = developer_input.splitlines(keepends=True)

    diff = unified_diff(base_lines, developer_lines, lineterm="")
    return "".join(diff)


def main():
    # Replace these lines with your actual code
    base_code = """ 
    # Your base code goes here
    def example_function():
        return "Hello, World!"
    """

    developer_input = get_developer_input()

    diff = generate_diff(base_code, developer_input)

    # Code Mentor AI working ...
    comment, chatbot_context = generate_comment(diff, [])

    # Debugging
    success, output = run_python_code(developer_input)
    fixed_code = None

    if not success:
        fixed_code = fix_python_code(developer_input, output)
        print(f"Suggested fix:\n{fixed_code}")

    # Test case generation
    gpt_client = code_test_case(developer_input)

    print("Code Review Comment:", comment)
    print("Suggested Fix:", fixed_code)
    print("Test Cases:", gpt_client)

    # Optionally, create an HTML output file with the code review comments
    create_html_output("Code Review", "Reviewing recent changes", [{"diff": diff}], "Code review prompt")


if __name__ == "__main__":
    main()

