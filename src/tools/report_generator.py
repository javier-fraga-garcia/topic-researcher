from datetime import datetime

def generate_report(text: str) -> None:
    """
    Save a string as a Markdown report with a timestamped filename.

    Args:
        text (str): The content to write into the Markdown file.
    """
    filename = f'{datetime.now().strftime("%y%m%d%H%M%S")}_report.md'
    with open(filename, 'w+') as f:
        f.write(text)
