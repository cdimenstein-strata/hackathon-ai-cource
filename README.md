# Designing and Deploying Agentic AI Systems with Amazon Bedrock

Interactive course website for learning about AI agent systems built on AWS Bedrock.

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Build

```bash
# Generate the course website
python build_site.py

# Output: index.html (open in browser)
```

## Course Structure

- **Course Summary/** - Overview and course materials
- **Textbook Chapters/** - Core learning modules
- **Quizzes and Assessments/** - Practice exercises and evaluations

## Development

### Running the Build Script

```bash
python build_site.py
```

This generates `index.html` from the markdown source files.

### Course Files

The build script processes these files in order:
1. Course Overview
2. Module 1-7 (Foundations through Productionizing)
3. Answer Keys & Assessments
4. Capstone Project

## Project Status

- Initial version: Course content and build system
- Next steps: Add tests, refactor build script for maintainability
