import re
import sys

def transform_html(content):
    # Replace favicon, manifest, icons, etc.
    replacements = {
        r'href="/favicon.ico"': r'href="{{ url_for("static", filename="favicon.ico") }}"',
        r'href="/logo192.png"': r'href="{{ url_for("static", filename="logo192.png") }}"',
        r'href="/manifest.json"': r'href="{{ url_for("static", filename="manifest.json") }}"',
        r'src="/static/js/main.([a-zA-Z0-9]+).js"': r'src="{{ url_for("static", filename="static/js/main.\1.js") }}"',
        r'href="/static/css/main.([a-zA-Z0-9]+).css"': r'href="{{ url_for("static", filename="static/css/main.\1.css") }}"'
    }

    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)

    return content

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <source_file> <output_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as source_file:
        content = source_file.read()

    transformed_content = transform_html(content)

    with open(sys.argv[2], 'w') as output_file:
        output_file.write(transformed_content)
