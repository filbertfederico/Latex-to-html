import ply.lex as lex
import ply.yacc as yacc
import re

tokens = (
    'DOCUMENTCLASS',
    'IEEEOVERRIDE',
    'USEPACKAGE',
    'DEF',
    'BEGIN_DOCUMENT',
    'TITLE',
    'THANKS',
    'AUTHOR',
    'IEEEAUTHORBLOCKN',
    'IEEEAUTHORBLOCKA',
    'MAKETITLE',
    'BEGIN_ABSTRACT',
    'END_ABSTRACT',
    'BEGIN_IEEEKEYWORDS',
    'END_IEEEKEYWORDS',
    'SECTION',
    'SUBSECTION',
    'BEGIN_ITEMIZE',
    'END_ITEMIZE',
    'ITEM',
    'TEXT',
)

t_DOCUMENTCLASS = r'\\\\documentclass\[[^\]]*\]\{[^}]*\}'
t_IEEEOVERRIDE = r'\\\\IEEEoverridecommandlockouts'
t_USEPACKAGE = r'\\\\usepackage\{[^}]*\}'
t_DEF = r'\\\\def\{[^}]*\}'
t_BEGIN_DOCUMENT = r'\\\\begin\{document\}'
t_TITLE = r'\\\\title\{[^}]*\}'
t_THANKS = r'\\\\thanks\{[^}]*\}'
t_AUTHOR = r'\\\\author\{[^}]*\}'
t_IEEEAUTHORBLOCKN = r'\\\\IEEEauthorblockN\{[^}]*\}'
t_IEEEAUTHORBLOCKA = r'\\\\IEEEauthorblockA\{[^}]*\}'
t_MAKETITLE = r'\\\\maketitle'
t_BEGIN_ABSTRACT = r'\\\\begin\{abstract\}'
t_END_ABSTRACT = r'\\\\end\{abstract\}'
t_BEGIN_IEEEKEYWORDS = r'\\\\begin\{IEEEkeywords\}'
t_END_IEEEKEYWORDS = r'\\\\end\{IEEEkeywords\}'
t_SECTION = r'\\\\section\{[^}]*\}'
t_SUBSECTION = r'\\\\subsection\{[^}]*\}'
t_BEGIN_ITEMIZE = r'\\\\begin\{itemize\}'
t_END_ITEMIZE = r'\\\\end\{itemize\}'
t_ITEM = r'\\\\item'
t_TEXT = r'[^\n]+'

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()

def p_document(p):
    'document : element document'
    p[0] = p[1] + p[2]

def p_document_empty(p):
    'document : '
    p[0] = ''

def p_element(p):
    '''element : DOCUMENTCLASS
               | IEEEOVERRIDE
               | USEPACKAGE
               | DEF
               | BEGIN_DOCUMENT
               | TITLE
               | THANKS
               | AUTHOR
               | IEEEAUTHORBLOCKN
               | IEEEAUTHORBLOCKA
               | MAKETITLE
               | BEGIN_ABSTRACT
               | END_ABSTRACT
               | BEGIN_IEEEKEYWORDS
               | END_IEEEKEYWORDS
               | SECTION
               | SUBSECTION
               | BEGIN_ITEMIZE
               | END_ITEMIZE
               | ITEM
               | TEXT'''
    p[0] = latex_commands[p[1]]

def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

def latex_to_html(data, latex_commands):
    # First, use the lexer and parser to handle bold and italic text
    parsed_data = parser.parse(data, lexer=lexer)
    # Then, use the dictionary to handle the other LaTeX commands
    for latex, html in latex_commands.items():
        parsed_data = re.sub(latex, html, parsed_data)
    return parsed_data

latex_commands = {
    r'\\\\documentclass\[[^\]]*\]\{[^}]*\}': r'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body>',
    r'\\\\title\{[^}]*\}': r'<h1>Title</h1>',
    r'\\\\section\{[^}]*\}': r'<h2>Section</h2>',
    r'\\\\subsection\{[^}]*\}': r'<h3>Subsection</h3>',
    r'\\\\begin\{itemize\}': r'<ul>',
    r'\\\\end\{itemize\}': r'</ul>',
    r'\\\\item': r'<li>',
    r'\\\\cite\{[^}]*\}': r'<a href="#">Citation</a>',
}

data = r"\\\\documentclass{article} \\\\title{My Title} \\\\section{Introduction} \\\\textbf{Hello}, \\\\textit{world}!"
print(latex_to_html(data, latex_commands))

