# Data Migration Verification Scripts

## 1. Files Checksum Comparison

These Python scripts are designed to verify large files migrated during data migration processes. They work with the path to the user's documents directory.

Ensure you have Python installed and any required dependencies.

### Overview

The data migration verification process for these files involves the following main steps:

- **Generate Checksums for Source Files**: Use `checksumGeneratorFile.py` to generate checksums for the files you want to verify in the source directory. Rename the generated file to `previousChecksums.txt`.
- **Generate Checksums for Target Files**: Run `checksumGeneratorFile.py` again to generate checksums for the new set of files. Rename the generated file to `currentChecksums.txt`.
- **Compare Checksums**: Execute `checksumCompare.py` to compare the checksums of the files from before and after migration. This will provide a log file with the verification results.

### Detailed Instructions

Please see the detailed instructions in detailed_instructions.txt

## 2. Data Validation Scripts

### Purpose
The Data Migration Validation Script is designed to automate the validation of data between a source file and a target file. It ensures that the data in the target system matches the transformed data from the source, taking into account potential differences in record order.

### Main Steps

**1. Prepare Your Data**: Create and save your source and target CSV files with the data you want to validate.

**2. Install Dependencies**: Ensure that the pandas library is installed in your Python environment.

**3. Run the Script**: Execute the script to validate data between the source and target files.

**4. Review Results**: Check the result's output in terminal and report file to verify if the data migration is successful or if discrepancies are found.

### Detailed Instructions

Please see the detailed instructions in detailed_instructions.txt