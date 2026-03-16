import re

replacements = [
    (r"Lionel Messi vs\.? Lionel Messi", "Messi vs Ronaldo"),
    (r"Messi vs\.? Messi", "Messi vs Ronaldo"),
    (r"Lionel Messi-Messi", "Messi-Ronaldo"),
    (r"Lionel Messi vs Messi", "Messi vs Ronaldo"),
]

files_to_update = [
    "internal_link_updates.json",
    "new_descriptions.json",
    "new_titles.json",
    "titles.txt"
]

def update_content(content):
    new_content = content
    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
    return new_content

for filename in files_to_update:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = update_content(content)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Refined {filename}")
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error refining {filename}: {e}")
