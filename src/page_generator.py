import os
from markdown_to_html import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            # Slice off the "# " and strip any remaining whitespace
            return line[2:].strip()
    
    # If the loop finishes without returning, there was no h1!
    raise ValueError("All pages need a single h1 header for the title")

def generate_page(from_path, template_path, dest_path, basepath): # <-- Added basepath
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        markdown_content = f.read()
        
    with open(template_path, "r") as f:
        template_content = f.read()
        
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)
    
    # Replace the placeholders
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Replace relative paths with the basepath!
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')
    
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
        
    with open(dest_path, "w") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath): # <-- Added basepath
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        
        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                html_dest_path = dest_path[:-3] + ".html"
                generate_page(from_path, template_path, html_dest_path, basepath) # Pass it down
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath) # Pass it down