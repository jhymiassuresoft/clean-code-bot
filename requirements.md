As a software engineer specializing in Python CLI tools and LLM integration.

## Task

Build a Python CLI tool called **"The Clean Code Bot"** that accepts a source code file as argument and returns a refactored, documented version of that code.

## The code will commit the next 

- Accept a file path as args (using `click` or `argparse`)
- Send the code to **Groq Cloud's API** for LLM inference
- Return refactored code that:
  - will use OOP and follow the **SOLID principles**
  - includes comprehensive technical documentation (Docstrings for Python, JSDoc for JavaScript, etc.)
  - return the code indented well 
-  Implement input validation and sanitization to prevent Prompt Injection attacks (e.g., ensuring the user cannot inject malicious commands through the input code).
- It will contain a readme indicating the instructions to run the script. This includes
  - the dependencies or libraries needed
  - configuration needed like groq access key
- include a .gitignore


  
## Constraints

- Language: **Python**
- LLM Provider: **Groq Cloud** (free tier)
- CLI Library: `click` or `argparse`
- The CoT prompt template must be implemented as a reusable, clearly defined component in the code