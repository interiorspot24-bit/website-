import os
import re

directory = 'g:/interio'
count_modified = 0

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Check if this is a PDP layout file by looking for pdp-title
        if 'class="pdp-title"' not in content:
            continue

        # Extract the title
        title_match = re.search(r'<h1 class="pdp-title">(.*?)</h1>', content)
        if not title_match:
            continue
            
        title = title_match.group(1).strip()
        first_word = title.split()[0].upper() if title else "IS"
        # Generate SKU
        new_sku = f"{first_word[:5]}-SOLID-8X4"
        
        modified = False
        
        # Replace the SKU if it's the default CR-SOLID-8X4
        if '<div class="pdp-sku">SKU: CR-SOLID-8X4</div>' in content:
            content = content.replace('<div class="pdp-sku">SKU: CR-SOLID-8X4</div>', f'<div class="pdp-sku">SKU: {new_sku}</div>')
            modified = True
        
        # Replace official CRAYON e-catalogue with the actual product name
        if 'official CRAYON e-catalogue' in content:
            content = content.replace('official CRAYON e-catalogue', f'official {title} e-catalogue')
            modified = True
            
        # Optional: Clean up "CRAYON" alt tags if they were missed
        if 'alt="Crayon Laminate Solid Colour"' in content and title != "CRAYON":
            content = content.replace('alt="Crayon Laminate Solid Colour"', f'alt="{title}"')
            modified = True
            
        # Replace Whatsapp text if it says CRAYON but the product is different
        wa_match = re.search(r'Hi, I\'m interested in CRAYON', content)
        if wa_match and title != "CRAYON":
            content = content.replace("Hi, I'm interested in CRAYON", f"Hi, I'm interested in {title}")
            modified = True

        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count_modified += 1
            
print(f"Done fixing SKUs and e-catalogue references! Modified {count_modified} files.")
