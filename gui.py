import tkinter as tk
from tkinter import filedialog
from markdowntohtml import MarkdownParser, read_markdown_file


def parse_markdown():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Markdown File", filetypes=(("Markdown files", "*.md"), ("All files", "*.*")))
    if file_path:
        markdown_text = read_markdown_file(file_path)
        parser = MarkdownParser()
        parser.tokenize(markdown_text)
        html_output = parser.parse_tokens_to_html()
        display_html(html_output)

def display_html(html_output):
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, html_output)

# Create GUI window
root = tk.Tk()
root.title("Markdown to HTML Parser")

# Create a button to select and parse Markdown file
parse_button = tk.Button(root, text="Parse Markdown", command=parse_markdown)
parse_button.pack(pady=10)

# Create a text area to display HTML output
output_text = tk.Text(root, height=20, width=80)
output_text.pack(padx=10, pady=5)

root.mainloop()

