import os
import sys
import re

LAYOUT_FILE = "_layouts/default.html"

def verify_layout():
    if not os.path.exists(LAYOUT_FILE):
        print(f"Error: {LAYOUT_FILE} not found.")
        return False

    with open(LAYOUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []

    # Check for leading spaces in Liquid tags starting with /assets/css
    # Example: {{ " /assets/css/..." | ... }}
    space_pattern = r'\{\{\s*"\s+/[^"]+"'
    matches = re.finditer(space_pattern, content)
    for match in matches:
        errors.append(f"Found leading space in path: '{match.group()}' at position {match.start()}")

    # Specifically check the theme.css and custom.css lines
    theme_pattern = r'href="\{\{\s*"/assets/css/theme.css"'
    custom_pattern = r'href="\{\{\s*"/assets/css/custom.css"'

    if not re.search(theme_pattern, content):
        errors.append("Critical: theme.css path is missing or incorrectly formatted (check for missing leading slash or extra spaces).")
    
    if not re.search(custom_pattern, content):
        errors.append("Critical: custom.css path is missing or incorrectly formatted (check for missing leading slash or extra spaces).")

    if errors:
        print("Verification FAILED:")
        for error in errors:
            print(f"- {error}")
        return False
    
    print("Verification PASSED: Layout CSS paths are correctly formatted.")
    return True

if __name__ == "__main__":
    if verify_layout():
        sys.exit(0)
    else:
        sys.exit(1)
