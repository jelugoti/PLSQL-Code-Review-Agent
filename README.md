# Oracle PL/SQL Code Review Agent

An AI-powered proof-of-concept for reviewing Oracle PL/SQL code against coding standards provided through an external document.

## Overview

The application allows a developer to:

1. Upload a PL/SQL coding standards document.
2. Upload or paste PL/SQL source code.
3. Extract the coding standards.
4. Provide the standards and source code as context to an LLM.
5. Analyze the code against the supplied standards.
6. Display structured review findings.

## Key Design Principle

The coding policy is externalized from the application logic.

The PL/SQL standards are provided through an external document instead of being hardcoded into Python review rules.

Therefore, standards can change without changing the Python review logic.

For example:

    l_ prefix

can be changed to:

    lv_ prefix

in the standards document without modifying the Python application.

## Architecture

    Streamlit UI
          |
          v
    Standards Reader
          |
          v
    Rule Extraction
          |
          v
    Standards + PL/SQL
          |
          v
        LLM
          |
          v
    Structured JSON Findings
          |
          v
    Streamlit Results

## Project Structure

    PLSQL-Code-Review-Agent/
    |
    +-- app.py
    +-- models.py
    +-- standards_reader.py
    +-- rule_extractor.py
    +-- llm_reviewer.py
    +-- llm_client.py
    +-- reviewer.py
    +-- test_review.py
    |
    +-- standards/
    |   +-- PLSQL_Standards_Sample.docx
    |
    +-- sample_code/
    |   +-- good_employee_procedure.sql
    |   +-- bad_employee_procedure.sql
    |
    +-- .env.example
    +-- .gitignore
    +-- requirements.txt
    +-- README.md

## Technologies

- Python
- Streamlit
- Oracle PL/SQL
- Groq API
- Large Language Model
- python-docx

## Running the Application

### 1. Clone the repository

    git clone <repository-url>

### 2. Create a virtual environment

    python -m venv venv

### 3. Activate the environment

Windows:

    venv\Scripts\activate

### 4. Install dependencies

    pip install -r requirements.txt

### 5. Configure environment variables

Create a `.env` file:

    GROQ_API_KEY=your_api_key
    GROQ_MODEL=openai/gpt-oss-120b

### 6. Run the application

    streamlit run app.py

## Important

This repository contains only synthetic/sample PL/SQL code.

No company-specific source code or confidential standards are included.

## Future Enhancements

- Additional PL/SQL standards
- Review history and reporting
- Repository-level code review
- Private/self-hosted LLM


## Additional Notes:

File	              Responsibility
standards_reader.py	Read DOCX
rule_extractor.py	Extract standards
models.py	       Define structure of a standard
llm_reviewer.py	Build review prompt
llm_client.py	       Communicate with LLM
reviewer.py	       Orchestrate review
app.py	              Streamlit UI