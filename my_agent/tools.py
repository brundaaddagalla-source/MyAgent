from pathlib import Path
import subprocess


def write_file(filename: str, content: str) -> str:
    """Creates a new file or overwrites an existing file with the specified content.

    Args:
        filename: The path or name of the file to create.
        content: The text content to write inside the file.

    Returns:
        A confirmation message indicating success or failure.
    """
    try:
        path = Path(filename)
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(content, encoding="utf-8")
        return f"Successfully written to {filename} ({len(content)} characters)."
    except Exception as e:
        return f"Error writing file {filename}: {str(e)}"


def append_file(filepath: str, content: str) -> str:
    """Appends text content to the end of a specified file.

    Args:
        filepath: The path or name of the file to append to.
        content: The text content to append.

    Returns:
        A confirmation message indicating success or failure.
    """
    try:
        path = Path(filepath)
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("a", encoding="utf-8") as f:
            f.write(content)

        return f"Successfully appended {len(content)} characters to '{filepath}'."
    except Exception as e:
        return f"Error appending to file '{filepath}': {str(e)}"


def rename_file(old_path: str, new_path: str) -> str:
    """Renames or moves a file to a new location or name.

    Args:
        old_path: The current path or name of the file to rename.
        new_path: The new path or name for the file.

    Returns:
        A confirmation message indicating success or failure.
    """
    try:
        src = Path(old_path)
        dst = Path(new_path)

        if not src.exists():
            return f"Error: Source file '{old_path}' does not exist."

        if dst.exists():
            return f"Error: Destination '{new_path}' already exists. Please specify a non-existing destination path."

        # Create parent directories for destination if needed
        dst.parent.mkdir(parents=True, exist_ok=True)

        src.rename(dst)
        return f"Successfully renamed '{old_path}' to '{new_path}'."
    except Exception as e:
        return f"Error renaming '{old_path}' to '{new_path}': {str(e)}"


def list_txt_files(directory: str = ".") -> str:
    """Finds and lists all .txt files in a specified folder with their file sizes and line counts.

    Args:
        directory: The directory path to search for .txt files. Default is '.' (current folder).

    Returns:
        A formatted list of all .txt files found in the folder.
    """
    try:
        path = Path(directory).resolve()
        if not path.exists():
            return f"Error: Directory '{directory}' does not exist."
        if not path.is_dir():
            return f"Error: '{directory}' is not a directory."

        txt_files = sorted(path.glob("*.txt"))
        if not txt_files:
            return f"No .txt files found in '{directory}'."

        lines = [f"Found {len(txt_files)} .txt file(s) in '{directory}':"]
        for f in txt_files:
            size_kb = f.stat().st_size / 1024
            try:
                line_count = len(f.read_text(encoding="utf-8").splitlines())
                lines.append(f"- {f.name} ({size_kb:.2f} KB, {line_count} lines)")
            except Exception:
                lines.append(f"- {f.name} ({size_kb:.2f} KB)")

        return "\n".join(lines)
    except Exception as e:
        return f"Error listing .txt files in '{directory}': {str(e)}"


def view_file(filepath: str, max_chars: int = 10000) -> str:
    """Reads and returns the content of a file.

    Args:
        filepath: The path or name of the file to view.
        max_chars: Optional maximum number of characters to read to avoid token overflow.

    Returns:
        The content of the file as a string, or an error message if reading fails.
    """
    try:
        path = Path(filepath)

        if not path.exists():
            return f"Error: File '{filepath}' does not exist."

        if not path.is_file():
            return f"Error: '{filepath}' is a directory, not a file."

        content = path.read_text(encoding="utf-8")

        if len(content) > max_chars:
            truncated = content[:max_chars]
            return f"{truncated}\n\n[Output truncated: Showing first {max_chars} characters of {len(content)} total]"

        return content

    except UnicodeDecodeError:
        return f"Error: File '{filepath}' is not a valid UTF-8 text file (binary file)."
    except Exception as e:
        return f"Error reading file '{filepath}': {str(e)}"


def delete_file(filepath: str) -> str:
    """Deletes a specified file from the disk."""
    try:
        path = Path(filepath)
        if not path.exists():
            return f"Error: File '{filepath}' does not exist."
        if not path.is_file():
            return f"Error: '{filepath}' is a directory, not a file."
        path.unlink()
        return f"Successfully deleted '{filepath}'."
    except Exception as e:
        return f"Error deleting file: {str(e)}"


def push_to_github(
    repo_url: str,
    commit_message: str = "Update agent codebase",
    branch: str = "main",
    directory: str = "."
) -> str:
    """Initializes git (if needed), stages all files, commits, and pushes to a remote GitHub repository.

    Args:
        repo_url: The remote GitHub repository URL (e.g., 'https://github.com/username/repo.git').
        commit_message: Commit message describing the changes. Default is 'Update agent codebase'.
        branch: Target branch name. Default is 'main'.
        directory: Directory path of the repository to push. Default is '.' (current folder).

    Returns:
        A detailed status message of the git operations.
    """
    target_path = Path(directory).resolve()
    if not target_path.exists() or not target_path.is_dir():
        return f"Error: Target directory '{directory}' does not exist or is not a directory."

    def run_git(args: list[str]) -> tuple[int, str, str]:
        result = subprocess.run(
            ["git"] + args,
            cwd=str(target_path),
            capture_output=True,
            text=True
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    try:
        # 1. Check if git is available
        code, out, err = run_git(["--version"])
        if code != 0:
            return f"Error: Git is not available in PATH ({err or out})."

        # 2. Check/Initialize local git repo in the project folder
        git_dir = target_path / ".git"
        if not git_dir.exists():
            code, out, err = run_git(["init"])
            if code != 0:
                return f"Error initializing git: {err or out}"

        # 3. Set branch name
        run_git(["branch", "-M", branch])

        # 4. Stage files
        code, out, err = run_git(["add", "."])
        if code != 0:
            return f"Error staging files: {err or out}"

        # 5. Check if there are changes to commit
        code, status_out, _ = run_git(["status", "--porcelain"])
        if status_out:
            code, out, err = run_git(["commit", "-m", commit_message])
            if code != 0:
                return f"Error creating commit: {err or out}"
            commit_msg_status = f"Committed changes: '{commit_message}'"
        else:
            commit_msg_status = "No unstaged changes to commit (clean working tree)."

        # 6. Configure remote repository
        code, remotes_out, _ = run_git(["remote"])
        remotes = remotes_out.split()
        if "origin" in remotes:
            code, out, err = run_git(["remote", "set-url", "origin", repo_url])
        else:
            code, out, err = run_git(["remote", "add", "origin", repo_url])

        if code != 0:
            return f"Error setting remote origin: {err or out}"

        # 7. Push to GitHub
        code, out, err = run_git(["push", "-u", "origin", branch])
        if code != 0:
            combined_err = f"{out}\n{err}".strip()
            return (
                f"Push failed (exit code {code}):\n{combined_err}\n\n"
                "Note: Please ensure the GitHub repository exists, you have write permissions, "
                "and your Git credentials (e.g. GitHub CLI, Personal Access Token, or SSH key) are configured."
            )

        return f"Successfully pushed project to {repo_url} on branch '{branch}'.\n{commit_msg_status}"

    except Exception as e:
        return f"Unexpected exception during GitHub push: {str(e)}"
