import os

# Get the path to the user's documents directory using os.path.expanduser()
DOCUMENTS_PATH = os.path.expanduser('~/Documents')

def write_to_log(message, log_file, mode="a"):
    """Write a message to a log file."""
    with open(log_file, mode) as f:
        f.write(message + "\n")

def read_checksums(checksums_file, log_file):
    """Read checksums from a checksums file."""
    checksums = {}
    try:
        with open(checksums_file, "r") as f:
            for line_number, line in enumerate(f, start=1):
                try:
                    file_path, checksum = line.strip().split(": ")
                    checksums[file_path] = (checksum, line_number)
                except ValueError:
                    write_to_log(f"Invalid format in line {line_number}: {line.strip()}", log_file)
    except FileNotFoundError:
        write_to_log(f"Checksums file not found: {checksums_file}", log_file)
    return checksums

def compare_checksums(previous_checksums_file, current_checksums_file, log_file):
    """Compare checksums from two checksums files and write the results to a log file."""
    previous_checksums = read_checksums(previous_checksums_file, log_file)
    current_checksums = read_checksums(current_checksums_file, log_file)
    
    passed_count = 0
    failed_files = []
    missing_files = []
    
    log_messages = []

    if previous_checksums and current_checksums:            
        for file_path, (prev_checksum, prev_line_number) in previous_checksums.items():
            if file_path in current_checksums:
                current_checksum = current_checksums[file_path][0]
                if prev_checksum == current_checksum:
                    passed_count += 1
                else:
                    failed_files.append((file_path, prev_line_number))
            else:
                missing_files.append((file_path, prev_line_number))

        # Print failed comparisons
        log_messages.append("\nFailed checksum comparisons:")
        for file_path, line_number in failed_files:
            log_messages.append(f"{file_path}: FAILED (Line {line_number})")
        
        log_messages.append("\nMissing File Lines:")
        for file_path, line_number in missing_files:
            log_messages.append(f"{file_path}: FAILED (Line {line_number})")
        
    else:
        log_messages.append("Cannot compare checksums. Checksums files are missing or empty.\n\n")


    total_files = len(previous_checksums)
    failed_count = len(failed_files) + len(missing_files)
    dash = '-' * 60
    titleR = (" TEST REPORT ").center(60, '#')
    summary = f"\nSUMMARY: ==>  PASSED: {passed_count}, FAILED: {failed_count}, TOTAL FILES: {total_files} \n"
    
    log_messages.append("\n")
    log_messages.extend([dash, dash, titleR, summary, dash, dash])
    write_to_log("\n".join(log_messages), log_file, mode="w")

if __name__ == "__main__":
    previous_checksums_file = os.path.join(DOCUMENTS_PATH, "previousChecksums.txt")
    current_checksums_file = os.path.join(DOCUMENTS_PATH, "currentChecksums.txt")
    log_file = os.path.join(DOCUMENTS_PATH, "checksum_comparison_log.txt")
    compare_checksums(previous_checksums_file, current_checksums_file, log_file)

