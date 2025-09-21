import os
from datetime import datetime
from agents import function_tool


@function_tool
def generate_report(text: str) -> None:
    """
    Save a string as a Markdown report with a timestamped filename.

    Args:
        text (str): The content to write into the Markdown file.
    """
    os.makedirs("./reports", exist_ok=True)
    filename = f"./reports/{datetime.now().strftime('%y%m%d%H%M%S')}_report.md"
    with open(filename, "w+", encoding="utf-8") as f:
        f.write(text)
