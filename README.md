# Student Assistant AI Agent 🎓

An intelligent student assistant agent built using the **Google Agent Development Kit (ADK)** and powered by **Google Gemini**. The agent helps students answer study questions, explore study notes, create and manage study files, and push code directly to GitHub.

---

## 🌟 Features

- **Document Analysis & Q&A**: Read and extract facts from study documents (e.g., `earth.txt`, `moon.txt`, `sun.txt`).
- **File Management**:
  - Discover and view all `.txt` documents in any folder with `list_txt_files`.
  - Create and overwrite files with `write_file`.
  - Append notes or content with `append_file`.
  - Rename or relocate files with `rename_file`.
  - Inspect file contents safely with `view_file`.
  - Remove files with `delete_file`.
- **GitHub Integration**: Initialize Git repositories, stage changes, commit, and push project updates directly to GitHub with `push_to_github`.

---

## 📁 Project Structure

```text
agent/
├── .env                  # Environment variables (API Keys) - excluded from git
├── .env.example          # Example environment configuration template
├── .gitignore            # Git exclusion rules
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── earth.txt             # Sample study material (Earth facts)
├── moon.txt              # Sample study material (Moon facts)
├── sun.txt               # Sample study material (Sun facts)
└── my_agent/             # Agent core module
    ├── __init__.py
    ├── agent.py          # Root Agent definition & instructions
    ├── config.py         # Configuration settings
    ├── prompts.py        # System prompt templates
    └── tools.py          # Custom agent tools (Git and file I/O)
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **Git** installed on your system

### 2. Setup Virtual Environment
```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and insert your Gemini API Key:
```bash
# Windows PowerShell
Copy-Item .env.example .env
```
Inside `.env`:
```env
GOOGLE_API_KEY="your_actual_gemini_api_key_here"
```

---

## 🛠️ Available Agent Tools

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| `list_txt_files` | `directory: str` | Discovers and views all `.txt` files in a folder with sizes & line counts. |
| `view_file` | `filepath: str, max_chars: int` | Reads and returns the content of a local file safely. |
| `write_file` | `filename: str, content: str` | Creates or overwrites a text file with given content. |
| `append_file` | `filepath: str, content: str` | Appends text content to the end of an existing file. |
| `rename_file` | `old_path: str, new_path: str` | Renames or moves a file to a new name/path. |
| `delete_file` | `filepath: str` | Deletes a specified file from the disk. |
| `push_to_github` | `repo_url: str, commit_message: str, branch: str` | Initializes Git, commits changes, and pushes repository to GitHub. |

---

## 💻 Running the Agent

You can launch and test the agent using the Google ADK CLI:

```bash
# Run web UI / playground
adk run my_agent
```

Or interact via Python:

```python
from my_agent.agent import root_agent

# Run query through the agent
response = root_agent.run("What .txt study files do we have in the folder?")
print(response)
```

---

## 📄 License

MIT License. Feel free to use and customize for your academic or personal projects.
