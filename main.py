from code_review.code_review import generate_comment
from code_test_case.code_test_case import code_test_case
from code_debug.code_debug import fix_python_code
import string
import random

def developer_input():
    """
    Function to get input from the developer, either as code or a file path.
    """
    input_type = input("Enter 'C' for code input or 'F' for file input: ").lower()

    if input_type == 'c':
        code = input("Please enter your Python code: ")
        return code
    elif input_type == 'f':
        file_path = input("Please enter the file path: ")
        try:
            with open(file_path, 'r') as file:
                code = file.read()
            return code
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    else:
        print("Invalid input type. Please enter 'C' or 'F'.")
        return None
    
def generate_random_filename():
    """Generates a random filename with the specified format."""
    random_numbers = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{random_numbers}-output.html"
    
def create_html_output(comment, test_cases, debug_suggestions):
    """
    Generates an HTML output file containing code review comments, test cases, and debug suggestions.
    """
    random_filename = generate_random_filename()

    html_output = "<html>\n<head>\n<title>CodeMentor AI: Review Report</title>\n</head>\n<body>\n"

    html_output += "<style>\nbody {\nfont-family: sans-serif;\nfont-size: 16px;\n}\n"
    html_output += "h1 {\nfont-size: 24px;\nfont-weight: bold;\nmargin-bottom: 10px;\n}\n"
    html_output += "p {\nmargin-bottom: 5px;\n}\n</style>\n</head>\n<body>\n"


    html_output += "<h1>Code Review Comment</h1>\n"
    html_output += f"<p>{comment}</p>\n"

    html_output += "<h1>Generated Test Cases</h1>\n"
    html_output += f"<p>{test_cases}</p>\n"

    html_output += "<h1>Debug Suggestions</h1>\n"
    html_output += f"<p>{debug_suggestions}</p>\n"

    html_output += "</body>\n</html>"

    with open(random_filename, "w") as f:
        f.write(html_output)
    
    print(f"CodeMentor AI has generated your report. File saved as {random_filename}")


def main():
    """
    The main function to coordinate the code review, test case generation, and code debugging.
    """
    # Get code input from the developer
    code = developer_input()

    if code is None:
        return  # Exit if input is invalid

    # Generate code review comment
    comment, _ = generate_comment(code, [])

    # Print code review comment
    print("Code Review Comment:")
    print(comment)
    print("-" * 50)

    # Generate test cases
    test_cases = code_test_case(code)

    # Print generated test cases
    print("Generated Test Cases:")
    print(test_cases)
    print("-" * 50)


    # Debug code
    debug_suggestions = fix_python_code(code)

    # Print debug suggestions
    print("Debug Suggestions:")
    print(debug_suggestions)

    create_html_output(comment, test_cases, debug_suggestions)

if __name__ == "__main__":
    main()
