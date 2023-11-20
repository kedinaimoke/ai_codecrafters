# DEVELOPER GUIDE

## Introduction

Welcome to the DEVELOPER GUIDE for our project. This guide aims to provide developers with a comprehensive understanding of the project's structure, development process, and contribution guidelines. Whether you're a seasoned Python developer or a newcomer to the project, this guide will equip you with the necessary knowledge to contribute effectively.

## Project Structure

The project's structure is organized to facilitate collaboration and maintainability. The main directories are:

* `codementor`: Contains the core code for the project's functionalities, including code review and test case generation.

* `codementor_ai`: Contains the AI-related components, such as the GPTClient class for interacting with the OpenAI API.

* `tests`: Houses the unit tests for the project's code, ensuring its correctness and reliability.

* `docs`: Includes documentation files, such as this developer guide and the user guide.

## Development Environment Setup

To set up the development environment, follow these steps:

1. **Install Python 3.11:** Ensure you have Python 3.11 installed on your system. You can download and install Python from https://www.python.org/downloads/.

2. **Create a Virtual Environment:** Creating a virtual environment isolates project dependencies from your global Python environment. Use the following command to create a virtual environment named `codecrafter`:

```
python -m venv codecrafter
```

3. **Activate the Virtual Environment:** Activate the virtual environment to use its isolated Python environment:

```
codecrafter/Scripts/activate
```

4. **Install Project Requirements:** Install the project's required dependencies using the following command:

```
pip install -r requirements.txt
```

## Development Process

The development process involves the following steps:

1. **Code Changes:** Make the desired changes to the project's code. Ensure the code follows the project's coding style guidelines.

2. **Unit Tests:** Run the unit tests using the following command to ensure the changes haven't introduced any regressions:

```
python -m pytest tests
```

3. **Code Review:** Conduct a thorough code review of your changes to ensure they meet the project's quality standards.

4. **Commit Changes:** Commit your changes to the version control system (VCS), such as Git, with a clear commit message describing the changes made.

5. **Create Pull Requests:** Create pull requests on the project's repository to propose your changes for review and merging into the main codebase.

## Contribution Guidelines

We welcome contributions from the community and encourage you to participate in the project's development. Please follow these guidelines when contributing:

* **Readability and Maintainability:** Strive to write clear, readable, and maintainable code that adheres to the project's coding style guidelines.

* **Tests:** Ensure your changes are accompanied by relevant unit tests that verify the correctness of the new code.

* **Documentation:** Update documentation, such as this developer guide, if your changes affect the project's usage or functionality.

* **Code Review:** Engage in code review discussions to provide feedback and ensure the quality of contributions.

* **Communication:** Communicate effectively with other developers through pull request comments, issue tracker discussions, and community forums.

We appreciate your willingness to contribute to our project and look forward to your valuable contributions.
