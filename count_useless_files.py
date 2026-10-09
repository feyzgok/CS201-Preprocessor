import os

def count_files_in_directory(directory_path):
    total_files = 0
    if not os.path.exists(directory_path):
        print(f"Error: The directory '{directory_path}' does not exist.")
        return 0

    for root, _, files in os.walk(directory_path):
        total_files += len(files)
        
    return total_files

if __name__ == "__main__":
    from config import USELESS_CODE_PATH
    target_directory = USELESS_CODE_PATH
    file_count = count_files_in_directory(target_directory)
    print(f"Total number of files in '{target_directory}': {file_count}")
