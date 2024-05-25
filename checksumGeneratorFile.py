import os
import hashlib

# Get the path to the user's documents directory using os.path.expanduser()
documents_path = os.path.expanduser('~/Documents')

def generate_checksum(file_path, algorithm="sha256"):
    """Generate checksum for a file using the specified hashing algorithm."""
    try:
        hasher = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            while True:
                data = f.read(65536)  # Read in 64k chunks
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error calculating checksum for {file_path}: {e}")
        return None

def generate_checksums_in_folder(folder_path, output_directory, algorithm="sha256"):
    """Generate checksums for all files in a folder and its subfolders."""
    checksums = {}
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            checksum = generate_checksum(file_path, algorithm)
            if checksum is not None:
                checksums[file_path] = checksum
    
    output_file = os.path.join(output_directory, "checksums.txt")
    with open(output_file, "w") as f:
        for file_path, checksum in checksums.items():
            f.write(f"{file_path}: {checksum}\n")
    
    print(f"Checksums generated and saved to {output_file}.")

if __name__ == "__main__":
    folder_path = documents_path
    output_directory = documents_path
    generate_checksums_in_folder(folder_path, output_directory)
