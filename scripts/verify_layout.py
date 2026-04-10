import os
import sys
import re

LAYOUT_FILE = "_layouts/default.html"

def verify_layout():
    if not os.path.exists(LAYOUT_FILE):
        print(f"Error: {LAYOUT_FILE} not found.")
        return False

    with open(LAYOUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        content = "".join(lines)

    errors = []

    # 1. Check for line number corruption (e.g., "123: <html>")
    # This often happens when copy-pasting from a view with line numbers
    for i, line in enumerate(lines):
        if re.match(r'^\d+: ', line):
            errors.append(f"Corruption detected: Line {i+1} starts with a line number prefix.")

    # 2. Check for leading spaces in Liquid tags starting with /assets/css
    # Example: {{ " /assets/css/..." | ... }}
    space_pattern = r'\{\{\s*"\s+/[^"]+"'
    matches = re.finditer(space_pattern, content)
    for match in matches:
        errors.append(f"Found leading space in path: '{match.group()}' at position {match.start()}")

    # 3. Specifically check the theme.css and custom.css lines
    theme_pattern = r'href="\{\{\s*"/assets/css/theme.css"'
    custom_pattern = r'href="\{\{\s*"/assets/css/custom.css"'

    if not re.search(theme_pattern, content):
        errors.append("Critical: theme.css path is missing or incorrectly formatted.")
    
    if not re.search(custom_pattern, content):
        errors.append("Critical: custom.css path is missing or incorrectly formatted.")

    # 4. Check for unclosed Liquid tags or broken HTML structure in key areas
    if "<!-- Menu Navigation" not in content:
         errors.append("Warning: Menu navigation section start comment is missing.")
    if "<!-- Footer" not in content:
         errors.append("Warning: Footer section start comment is missing.")

    if errors:
        print("❌ Verification FAILED:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    print("✅ Verification PASSED: Layout integrity verified.")
    return True

if __name__ == "__main__":
    if verify_layout():
        sys.exit(0)
    else:
        sys.exit(1)
