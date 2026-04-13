import sys
import os
import shutil
from copystatic import copy_files_recursive
from page_generator import generate_pages_recursive # <-- Update this import!

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"          # <-- Add this variable
template_path = "./template.html"       # <-- Add this variable

def main():
    # Set default basepath
    basepath = "/"
    
    # Check if a custom basepath was provided as a CLI argument
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print("Deleting docs directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_public)
    
    print(f"Generating pages with basepath: '{basepath}'...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)
if __name__ == "__main__":
    main()