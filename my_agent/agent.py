from google.adk.agents import Agent

from .tools import (
    write_file,
    append_file,
    rename_file,
    view_file,
    delete_file,
    push_to_github,
)


root_agent = Agent(
    name="student_assistant",
    model="gemini-3.6-flash",
    description="A student assistant that can answer questions using study documents and manage/push project files to GitHub.",
    instruction="""
    You are a helpful student assistant.

    Help students with questions about their studies.

    When the user asks to create or overwrite a file, 
    use the write_file tool.

    When the user asks to append content to a file,
    use the append_file tool.

    When the user asks to rename or move a file,
    use the rename_file tool.

    When the user asks to view a file,
    use the view_file tool.

    When the user asks to delete a file,
    use the delete_file tool.

    When the user asks to push or upload the project to GitHub,
    use the push_to_github tool with the repository URL.

    Answer clearly and concisely.
    """,
    tools=[
        write_file,
        append_file,
        rename_file,
        view_file,
        delete_file,
        push_to_github,
    ],
)
