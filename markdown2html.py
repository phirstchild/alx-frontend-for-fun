#!/usr/bin/python3
import sys
import os
import re
import hashlib

def convert_markdown_to_html(markdown_file, output_file):
    # Check if the number of arguments is correct
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: ./markdown2html.py <input_file> <output_file>\n")
        sys.exit(1)

    # Check if the Markdown file exists
    if not os.path.isfile(markdown_file):
        sys.stderr.write(f"Missing {markdown_file}\n")
        sys.exit(1)

    # Read the Markdown file
    with open(markdown_file, 'r') as f:
        markdown_content = f.read()

    # Markdown to HTML conversion logic
    html_content = parse_markdown_to_html(markdown_content)

    # Write HTML content to the output file
    with open(output_file, 'w') as output:
        output.write(html_content)

    sys.exit(0)

def parse_markdown_to_html(markdown_content):
    # Bold parsing
    markdown_content = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', markdown_content)

    # Emphasized parsing
    markdown_content = re.sub(r'__(.*?)__', r'<em>\1</em>', markdown_content)

    # MD5 hashing parsing
    markdown_content = re.sub(r'\[\[(.*?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), markdown_content)

    # Remove all occurrences of 'c' parsing
    markdown_content = re.sub(r'\(\((.*?)\)\)', lambda match: match.group(1).replace('c', ''), markdown_content, flags=re.IGNORECASE)

    # Split the content by lines
    lines = markdown_content.split('\n')

    # Initialize variables
    html_output = ''
    in_unordered_list = False
    in_ordered_list = False
    in_paragraph = False

    # Parse Markdown to HTML
    for line in lines:
        if line.startswith('* '):
            # Start of an unordered list
            if not in_unordered_list:
                if in_ordered_list:
                    html_output += '</ol>\n'
                    in_ordered_list = False
                html_output += '<ul>\n'
                in_unordered_list = True
                if in_paragraph:
                    html_output += '</p>\n'
                    in_paragraph = False

            # Extract list item content and add to HTML output
            item_content = line[2:]
            html_output += f'    <li>{item_content}</li>\n'

        elif line.startswith('1. '):
            # Start of an ordered list
            if not in_ordered_list:
                if in_unordered_list:
                    html_output += '</ul>\n'
                    in_unordered_list = False
                html_output += '<ol>\n'
                in_ordered_list = True
                if in_paragraph:
                    html_output += '</p>\n'
                    in_paragraph = False

            # Extract list item content and add to HTML output
            item_content = line[3:]
            html_output += f'    <li>{item_content}</li>\n'

        elif line.strip():  # Non-empty line (considered as a paragraph)
            if not in_paragraph:
                if in_unordered_list:
                    html_output += '</ul>\n'
                    in_unordered_list = False
                elif in_ordered_list:
                    html_output += '</ol>\n'
                    in_ordered_list = False
                html_output += '<p>\n'
                in_paragraph = True

            # Add content to the paragraph
            html_output += f'    {line}\n'

        else:  # Empty line
            if in_paragraph:
                html_output += '</p>\n'
                in_paragraph = False

    # Check if any list or paragraph was left open
    if in_unordered_list:
        html_output += '</ul>\n'
    elif in_ordered_list:
        html_output += '</ol>\n'
    elif in_paragraph:
        html_output += '</p>\n'

    return html_output

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py <input_file> <output_file>\n")
        sys.exit(1)
    
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]
    convert_markdown_to_html(markdown_file, output_file)

