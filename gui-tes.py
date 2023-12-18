import tkinter as tk
import re
from markdown2html import MarkdownParser

def convert_markdown_to_html():
    markdown_text = markdown_input.get("1.0", "end-1c")
    parser = MarkdownParser()
    parser.tokenize(markdown_text)
    html_output = parser.parse_tokens_to_html()
    display_html(html_output)
    display_errors(parser)

def display_html(html_output):
    html_output_text.config(state=tk.NORMAL)
    html_output_text.delete(1.0, tk.END)
    html_output_text.insert(tk.END, html_output)
    html_output_text.config(state=tk.DISABLED)

def display_errors(parser):
    error_text.config(state=tk.NORMAL)
    error_text.delete(1.0, tk.END)

    errors_found = False

    # Checking for bold syntax errors
    bold_pattern = re.compile(r'\*\*(.*?)\*\*')
    bold_matches = bold_pattern.findall(' '.join(parser.tokens))
    if bold_matches:
        error_text.insert(tk.END, "ERROR: Incomplete or incorrect bold syntax (Use '**' to indicate bold text).\n")
        errors_found = True

    # Checking for italic syntax errors
    italic_pattern = re.compile(r'\b_([^_]+)_\b|\*\*([^*]+)\*\*')
    italic_matches = italic_pattern.findall(' '.join(parser.tokens))
    if italic_matches:
        error_text.insert(tk.END, "ERROR: Incomplete or incorrect italic syntax (Use '_' to indicate italic text).\n")
        errors_found = True

    # Checking for strikethrough syntax errors
    strikethrough_pattern = re.compile(r'(?<!~)~~(?! )(.+?)(?<! )~~(?!~)')
    strikethrough_matches = strikethrough_pattern.findall(' '.join(parser.tokens))
    if strikethrough_matches:
        error_text.insert(tk.END, "ERROR: Incomplete or incorrect strikethrough syntax (Use '~~' to indicate strikethrough text).\n")
        errors_found = True

    if not errors_found:
        error_text.insert(tk.END, "No errors found.")

    error_text.config(state=tk.DISABLED)


# Create GUI window
root = tk.Tk()
root.title("Markdown to HTML Converter")

# Create a paned window to split the window into two sections
pane = tk.PanedWindow(orient="horizontal", sashrelief=tk.RAISED, sashwidth=5)
pane.pack(fill="both", expand=True)

# Left pane for markdown input
markdown_input = tk.Text(pane, height=20, width=40)
pane.add(markdown_input)

# Right pane for HTML output and error messages
output_pane = tk.PanedWindow(pane, orient="vertical", sashrelief=tk.RAISED, sashwidth=5)
pane.add(output_pane)

# HTML output display area
html_output_text = tk.Text(output_pane, height=20, width=40)
output_pane.add(html_output_text)

# Error messages display area
error_text = tk.Text(output_pane, height=5, width=40, bg="black", fg="red")
output_pane.add(error_text)

# Button to convert Markdown to HTML
convert_button = tk.Button(root, text="Convert Markdown to HTML", command=convert_markdown_to_html)
convert_button.pack(pady=10)

root.mainloop()