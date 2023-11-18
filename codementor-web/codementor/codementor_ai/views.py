from django.shortcuts import render
from .models import CodeReview, TestCase, CodeDebug
from dotenv import load_dotenv
import os
from codementor_ai.code_review.code_review import generate_comment
from codementor_ai.code_debug.code_debug import fix_python_code
from codementor_ai.code_test_case.code_test_case import GPTClient


load_dotenv()

api_key = os.getenv("API_KEY")

client = GPTClient()

def code_mentor(request):
    """Handles incoming HTTP requests, processes user input, and renders the corresponding response.

    This function serves as the main entry point for handling user requests and providing the appropriate code review, code debugging, or test case generation services. It processes the incoming HTTP request, validates user input, and interacts with the corresponding AI models to generate the requested results.

    Args:
    request (HttpRequest): The incoming HTTP request object containing the user's input data.

    Returns:
    HttpResponse: The rendered HTML response with the appropriate code review, code debug, or test case results."""

    if request.method == 'POST':
        if 'code_input' in request.POST:
            # Code Review Logic
            code_input = request.POST['code_input']
            chatbot_context = [{"role": "user", "content": f"Start code review for: {code_input}"}]
            try:
                code_review, chatbot_context = generate_comment(code_input, chatbot_context)
                CodeReview.objects.create(code_input=code_input, code_review=code_review)
                return render(request, 'index.html', {'code_review': code_review})
            except Exception as e:
                print(f"Error generating test case: {e}")
                return render(request, 'index.html', {'code_review': None, 'error_message': str(e)})

        elif 'debug_input' in request.POST:
            # Code Debug Logic
            debug_input = request.POST['debug_input']
            error_output = ""
            try:
                code_debug = fix_python_code(debug_input, error_output=error_output)
                print(code_debug)
                CodeDebug.objects.create(code_input=debug_input, code_debug=code_debug)
                return render(request, 'index.html', {'code_debug': code_debug})
            except Exception as e:
                print(f"Error generating test case: {e}")
                return render(request, 'index.html', {'code_debug': None, 'error_message': str(e)})

        elif 'test_case_input' in request.POST:
            # Test Case Generation Logic
            test_case_input = request.POST['test_case_input']
            problem_statement = test_case_input
            try:
                test_case = client.parse_test_cases(problem_statement)
                print("Test Case:", test_case)
                TestCase.objects.create(code_input=test_case_input, test_case=test_case)
                return render(request, 'index.html', {'test_case': test_case})
            except Exception as e:
                print(f"Error generating test case: {e}")
                return render(request, 'index.html', {'test_case': None, 'error_message': str(e)})
    else:
        return render(request, 'index.html')

    return render(request, 'index.html')
