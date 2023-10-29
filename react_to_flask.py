import re
import sys

def transform_html(content):
    # Replace favicon, manifest, icons, etc.
    replacements = {
        r'href="/(favicon.ico)"': r'href="{{ url_for("static", filename="\1") }}"',
        r'href="/(logo[\w\d]+\.png)"': r'href="{{ url_for("static", filename="\1") }}"',
        r'href="/(manifest.json)"': r'href="{{ url_for("static", filename="\1") }}"',
        r'src="/static/js/(main\.[a-zA-Z0-9]+\.js)"': r'src="{{ url_for("static", filename="static/js/\1") }}"',
        r'href="/static/css/(main\.[a-zA-Z0-9]+\.css)"': r'href="{{ url_for("static", filename="static/css/\1") }}"',
        r'src="/static/media/(.*?\.[a-zA-Z0-9]+\.svg)"': r'src="{{ url_for("static", filename="static/media/\1") }}"',
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
