import argparse
import os
import random
import string
import sys
import webbrowser
from openai import OpenAI
from tqdm import tqdm

client = OpenAI(
    api_key="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",
)

PROMPT_TEMPLATE = f"""Thorough code reviews should examine the change in detail and consider its integration within the codebase. 
                    Assess the clarity of the title, description, and rationale for the change. Evaluate the code's correctness, 
                    test coverage, and functionality modifications. Verify adherence to coding standards and best practices. 
                    Provide a comprehensive code review of the provided diffs, suggesting improvements and refactorings based on 
                    SOLID principles when applicable. Please refrain from further responses until the diffs are presented for review."""

def add_code_tags(text):
    """Adds code tags (<b><code></code>) around inline code blocks in the given text."""
    import re
    matches = re.finditer(r"`(.+?)`", text)

    updated_chunks = []
    last_end = 0
    for match in matches:
        updated_chunks.append(text[last_end : match.start()])
        updated_chunks.append("<b>`{}`<\b>".format(match.group(1)))
        last_end = match.end()
    updated_chunks.append(text[last_end:])
    return "".join(updated_chunks)

def generate_comment(diff, chatbot_context):
    """Generates a code review comment using the OpenAI API."""
    chatbot_context.append({
        "role": "user",
        "content": f"Make a code review of the changes made in this diff: {diff}",
    })

    retries = 3
    comment = ""

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                messages=[
                        {
                            "role": "user",
                            "content": f"Make a code review of the changes made in this diff: {diff}",
                        },
                        {
                            "role": "assistant",
                            "content": comment,
                        }
                    ],
                    model="gpt-3.5-turbo",
                        )
            
            comment = response.choices[0].message.content

        except Exception as e:
            if attempt == retries - 1:
                print(f"attempt: {attempt}, retries: {retries}")
                raise e
            else:
                print("OpenAI error occurred. Retrying...")
                continue

    chatbot_context = [
        {"role": "user", "content": f"Make a code review of the changes made in this diff: {diff}"},
        {"role": "assistant", "content": comment},
    ]
    return comment, chatbot_context


def create_html_output(title: str, description: str, changes: list, prompt: str):
    """Generates an HTML output file containing code review comments."""
    random_string = "".join(random.choices(string.ascii_letters, k=5))
    output_file_name = random_string + "-output.html"

    title_text = f"\nTitle: {title}" if title else ""
    description_text = f"\nDescription: {description}" if description else ""
    chatbot_context = [
        {"role": "user", "content": f"{prompt}{title_text}{description_text}"},
    ]

    html_output = "<html>\n<head>\n<style>\n"
    html_output += "body {\n    font-family: Roboto, Ubuntu, Cantarell, Helvetica Neue, sans-serif;\n    margin: 0;\n    padding: 0;\n}\n"
    html_output += "pre {\n    white-space: pre-wrap;\n    background-color: #f6f8fa;\n    border-radius: 3px;\n    font-size: 85%;\n    line-height: 1.45;\n    overflow: auto;\n    padding: 16px;\n}\n"
    html_output += "</style>\n"
    html_output += '<link rel="stylesheet"\n href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/default.min.css">\n <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>\n'
    html_output += "<script>hljs.highlightAll();</script>\n"
    html_output += "</head>\n<body>\n"
    html_output += "<div style='background-color: #333; color: #fff; padding: 20px;'>"
    html_output += "<h1 style='margin: 0;'>AI code review</h1>"
    html_output += f"<h3>Diff to review: {title}</h3>" if title else ""
    html_output += "</div>"

    with tqdm(total=len(changes), desc="Making code review", unit="diff") as pbar:
        for i, change in enumerate(changes):
            diff = change["diff"]
            comment, chatbot_context = generate_comment(diff, chatbot_context)
            pbar.update(1)
            html_output += f"<h3>Diff</h3>\n<pre><code>{diff}</code></pre>\n"
            html_output += f"<h3>Comment</h3>\n<pre>{add_code_tags(comment)}</pre>\n"
    html_output += "</body>\n</html>"

    with open(output_file_name, "w") as f:
        f.write(html_output)

    return output_file_name

def get_diff_changes_from_pipeline():
    """Reads diff changes from the standard input pipeline."""
    # Simulated code change for review
    simulated_code_change = """
    diff --git a/example.py b/example.py
    index abcdef1..1234567 100644
    --- a/example.py
    +++ b/example.py
    @@ -1,5 +1,5 @@
    def add(a, b):
    -    return a + b
    +    return a * b
    """

    diff_list = [{"diff": simulated_code_change}]
    return diff_list

def main():
    """Entry point for the AI code review script."""
    title, description, prompt = None, None, None
    changes = get_diff_changes_from_pipeline()
    parser = argparse.ArgumentParser(description="AI code review script")
    parser.add_argument("--title", type=str, help="Title of the diff")
    parser.add_argument("--description", type=str, help="Description of the diff")
    parser.add_argument("--prompt", type=str, help="Custom prompt for the AI")
    args = parser.parse_args()
    title = args.title if args.title else title
    description = args.description if args.description else description
    prompt = args.prompt if args.prompt else PROMPT_TEMPLATE
    output_file = create_html_output(title, description, changes, prompt)
    try:
        webbrowser.open(output_file)
    except Exception:
        print(f"Error running the web browser, you can try to open the output file: {output_file} manually")

if __name__ == "__main__":
    main()
