import re

replacements = [
    (r"Cristiano Ronaldo and Lionel Messi", "Lionel Messi and Cristiano Ronaldo"),
    (r"Lionel Messi and Cristiano Ronaldo", "Lionel Messi and Cristiano Ronaldo"), # No change but keeps order
    (r"Cristiano vs\.? Messi", "Messi vs Cristiano"),
    (r"Ronaldo vs\.? Messi", "Messi vs Ronaldo"),
    (r"Messi vs\.? Ronaldo", "Messi vs Ronaldo"),
    (r"UR Cristiano FC", "Lionel Messi FC"),
    (r"Cristiano Ronaldo", "Lionel Messi"),
    (r"Cristiano's", "Messi's"),
    (r"Ronaldo's", "Messi's"),
    (r"Cristiano", "Lionel Messi"),
    (r"Ronaldo", "Messi"),
    (r"CR7", "LM10"),
    (r"ur-cristiano", "messi-lionel"),
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
        print(f"Updated {filename}")
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error updating {filename}: {e}")
