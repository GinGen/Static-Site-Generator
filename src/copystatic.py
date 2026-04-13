import os
import shutil

def copy_files_recursive(source_dir_path, dest_dir_path):
    # Step 1: Ensure the destination directory exists and is entirely empty
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        
        # Outputting what we are doing to make debugging easier
        print(f" * {from_path} -> {dest_path}")
        
        # Step 2: If it's a file, just copy it directly
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
            
        # Step 3: If it's a directory, we recursively call this exact function!
        else:
            copy_files_recursive(from_path, dest_path)