class MarkdownParser:
    def __init__(self):
        self.tokens = []
        self.html_output = []

    def tokenize(self, markdown_text):
        self.tokens = markdown_text.split('\n')  # Split by lines

    def parse_tokens_to_html(self):
        in_blockquote = False
        in_list = False
        in_strikethrough = False  # Track strikethrough text
        for line in self.tokens:
            if line.startswith("#"):
                # Determine header level based on the number of # symbols
                header_level = min(6, line.count("#"))  # Cap the header level at h6
                header_text = line.replace("#", "").strip()
                self.html_output.append(f"<h{header_level}>{header_text}</h{header_level}>")
            elif line.startswith(">"):
                # Blockquote parsing
                if not in_blockquote:
                    self.html_output.append("<blockquote>")
                    in_blockquote = True
                blockquote_line = line.replace(">", "").strip()
                self.html_output.append(f"<p>{blockquote_line}</p>")
            elif "~~" in line:
                # Handling strikethrough (~~strikethrough~~)
                parsed_line = ""
                index = 0
                while index < len(line):
                    if line[index:index + 2] == "~~":
                        if not in_strikethrough:
                            parsed_line += "<del>"
                            in_strikethrough = True
                            index += 2
                        else:
                            parsed_line += "</del>"
                            in_strikethrough = False
                            index += 2
                    else:
                        parsed_line += line[index]
                        index += 1
                self.html_output.append(f"<p>{parsed_line}</p>")
            elif "**" in line:
                # Handling incomplete bold syntax (**bold**)
                if line.count("**") % 2 != 0:
                    raise ValueError("Incomplete bold syntax: '**' not properly closed")
            elif "_" in line:
                # Handling incomplete italic syntax (_italic_)
                if line.count("_") % 2 != 0:
                    raise ValueError("Incomplete italic syntax: '_' not properly closed")
            elif "~" in line:
                # Handling incomplete strikethrough syntax (~~strikethrough~~)
                if line.count("~") % 2 != 0:
                    raise ValueError("Incomplete strikethrough syntax: '~' not properly closed")
            elif "[" in line and "]" in line and "(" in line and ")" in line:
                # Handling incomplete link syntax ([text](url))
                if (line.count("[") != line.count("]") or line.count("(") != line.count(")")) or \
                        (line.find("[") > line.find("]") or line.find("(") > line.find(")")):
                    raise ValueError("Incomplete link syntax: '[', ']', '(', or ')' issue")
            elif line.startswith("- "):
                # List parsing
                if not in_list:
                    self.html_output.append("<ul>")
                    in_list = True
                list_item = line[2:]  # Remove the "- "
                self.html_output.append(f"<li>{list_item}</li>")
            else:
                # Handling normal paragraphs
                if in_blockquote:
                    self.html_output.append("</blockquote>")
                    in_blockquote = False
                if in_list:
                    self.html_output.append("</ul>")
                    in_list = False
                self.html_output.append(f"<p>{line}</p>")

        return ''.join(self.html_output)


def read_markdown_file(file_name):
    with open(file_name, 'r') as file:
        return file.read()


# File name containing Markdown content
file_name = 'Latex-to-html/input.md'

# Read Markdown content from the file
markdown_text = read_markdown_file(file_name)

# Create a parser instance and process the Markdown content
parser = MarkdownParser()
parser.tokenize(markdown_text)

try:
    html_output = parser.parse_tokens_to_html()
    print(html_output)
except ValueError as e:
    print(f"Error: {e}")
