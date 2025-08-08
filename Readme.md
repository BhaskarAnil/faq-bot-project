# FAQ Bot Project

## Introduction

This is a simple FAQ bot designed to answer farming-related questions. It uses a local CSV dataset of frequently asked questions and answers, vector search, and a conversational graph to provide relevant responses. The bot can be run interactively in the terminal or via a modern Streamlit web interface.

---

## Folder Structure

```
faq_bot_project/
├── app.py                   # Main entry point (Streamlit app)
├── chains/
│   ├── load_faqs.py         # Loads FAQ data from CSV
│   └── qa_pipeline.py       # Defines the QA chain logic
├── data/
│   └── faqs.csv             # FAQ dataset (questions and answers)
├── database/
│   └── chroma_db/           # Chroma vector database files
│       └── 74a840e5.../     # Internal Chroma DB files
│       └── chroma.sqlite3   # Chroma DB SQLite file
├── graph/
│   └── conversation_graph.py # Conversation graph logic
├── langsmith_config.py      # LangSmith tracing and graph invocation
├── requirements.txt         # Python dependencies
├── .gitignore               # Files/folders to ignore in git
├── Readme.md                # This documentation
└── venv/                    # Python virtual environment (not tracked)
```

---

## How to Run

### 1. Install Dependencies

First, create and activate a Python virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

Then install all required packages:

```bash
pip install -r requirements.txt
```

### 2. Prepare Environment Variables

If you want to use Google Generative AI (Gemini), create a `.env` file in the project root and add your API key:

```
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Run the Bot

#### Option 1: Streamlit Web App

```bash
streamlit run app.py
```

- Open your browser and go to `http://localhost:8501`
- Type your farming question in the chat interface

#### Option 2: Terminal (Interactive)

Uncomment the terminal code in `app.py` to use the CLI version. Then run:

```bash
python app.py
```

Type your question and get answers directly in the terminal.

---

## How to View the Output Locally

- **Streamlit Web App:** Visit `http://localhost:8501` in your browser after running `streamlit run app.py`.
- **Terminal:** Answers are printed directly in your terminal window.

---

## Data

- The bot uses `data/faqs.csv` as its knowledge base. You can add more Q&A pairs to this file.
- The vector database is stored in `database/chroma_db/` and is automatically managed.

---

## Customization

- To add new questions/answers, edit `data/faqs.csv`.
- To change the conversational logic, modify `graph/conversation_graph.py`.
- To use a different LLM or embedding model, update the relevant code in `chains/qa_pipeline.py` and `graph/conversation_graph.py`.

---

## Requirements

See `requirements.txt` for all dependencies. Key packages include:
- `streamlit`
- `langchain`
- `langgraph`
- `sentence-transformers`
- `chromadb`
- `scikit-learn`
- `google-generativeai` (for Gemini)

---

## LangSmith Tracing

This project supports tracing with [LangSmith](https://smith.langchain.com/) for monitoring and debugging your bot's execution and chains.

### How to Enable LangSmith Tracing

1. **Set up your LangSmith account** at https://smith.langchain.com/ and get your API key.
2. **Update your `.env` file** in the project root with the following variables:

```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key_here
LANGCHAIN_PROJECT=faq-bot-project
```

3. **Load environment variables** automatically by using `load_dotenv()` in `langsmith_config.py` (already included).

LangSmith will automatically trace and log your bot's runs when you use the Streamlit app or CLI.

---
