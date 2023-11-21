import streamlit as st
from code_test_case.code_test_case import code_test_case
from code_debug.code_debug import fix_python_code
from code_review.code_review import generate_comment
import ast
import base64


def create_html_output(comment, test_cases, debug_suggestions):
    """
    Function to create an HTML representation of code review, test cases, and debug suggestions.
    """
    html_output = f"<h2>Code Review Comment:</h2><p>{comment}</p>"
    html_output += f"<h2>Generated Test Cases:</h2><pre>{test_cases}</pre>"
    html_output += f"<h2>Debug Suggestions:</h2><pre>{debug_suggestions}</pre>"

    return html_output

def developer_input():
    """
    Function to get input from the developer, either as code or a file path.
    """
    input_type = st.radio("Choose input type:", ['Code', 'File'])

    if input_type == 'Code':
        code = st.text_area("Enter your Python code here:", value="", height=300, help="Write your code here")
        return code
    elif input_type == 'File':
        file_path = st.file_uploader("Upload a file with Python code", type=["py"])
        if file_path is not None:
            code = file_path.read().decode('utf-8')
            return code
    return None

def is_valid_python_code(code: str) -> bool:
    """
    Function to check if the entered code is valid Python code.
    """
    try:
        if isinstance(code, str):
            code = code.encode('utf-8')
        elif not isinstance(code, bytes):
            raise ValueError('Invalid code type')

        parsed_code = ast.parse(code)

        return True
    except Exception as e:
        print(f"Error parsing code: {e}")
        return False

def main():
    """
    The main function to coordinate the code review, test case generation, and code debugging.
    """
    st.set_page_config(page_title="Code Review App", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

    st.markdown(
        "<style>body {background-color: #f5f5f5; background-image: url(''); background-size: cover;}</style>",
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align: center; color: #87CEEB;'>Code Review and Debugging App</h1>", unsafe_allow_html=True)

    code = developer_input()

    try:
        if not is_valid_python_code(code) and developer_input == None:
            st.warning("You have to give the AI some python code to work with.")
            return

        comment, _ = generate_comment(code, [])

        with st.expander("Code Review Comment"):
            st.write(comment)

        test_cases = code_test_case(code)

        with st.expander("Generated Test Cases"):
            st.code(test_cases, language='python')

        debug_suggestions = fix_python_code(code)

        with st.expander("Debug Suggestions"):
            st.code(debug_suggestions, language='python')

        html_output = create_html_output(comment, test_cases, debug_suggestions)
        st.markdown("---")
        st.markdown("*Download HTML Output:*")
        st.markdown(
            f'<a href="data:text/html;base64,{base64.b64encode(html_output.encode("utf-8")).decode()} " download="output.html">Download HTML</a>',
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()