
# Data Migration Verification Scripts

  

These Python scripts are designed to verify large files migrated during data migration processes. They work with the path to the user's documents directory.

Ensure you have Python installed and any required dependencies.

  

## Overview

  

The data migration verification process for these files, involves these main steps:

  

- Generate Checksums for Source Files: Use checksumGeneratorFile.py to generate checksums for the files you want to verify in the source directory. Rename the generated file to previousChecksums.txt.

- Generate Checksums for Target Files: Run checksumGeneratorFile.py again to generate checksums for the new set of files. Rename the generated file to currentChecksums.txt.

- Compare Checksums: Execute checksumCompare.py to compare the checksums of the files from before and after migration. This will provide a log file with the verification results.

  

## Instructions

  

1. Prepare the Source Files: Place the files you want to verify in the user's documents directory. Ensure there are no other files in this directory that you don't want to verify.

  

2. Generate Checksums for Source Files: Run the checksumGeneratorFile.py script and a file will be generated.

  

```powershell

python  checksumGeneratorFile.py
```

  

3. Rename the Generated File to 'previousChecksums.txt' :

  

```powershell
Rename-Item -Path "%USERPROFILE%\Documents\checksums.txt" -NewName "previousChecksums.txt"
```

  

4. Delete and Copy: Delete the files read in previous steps and copy the target files into the user's documents directory.

- Execute the delete command - expands the ~/Documents path to the full path and deletes all files in that directory.

- Copy the target files into the user's documents directory.

  

```powershell
Remove-Item ~/Documents/* -Force
```

  

```powershell
Copy-Item -Path "<location Target Files>" -Destination %USERPROFILE%\Documents\ -Recurse
```

  

5. Generate Checksums for Target Files: Run the checksumGeneratorFile.py script again. This will generate a checksums for the new set of files.

  

```powershell
python  checksumGeneratorFile.py
```

  

6. Compare Checksums: Run the checksumCompare.py script to compare the checksums. This will compare the checksums of the files from before and after migration.

  

```powershell
python  checksumCompare.py
```

  

7. Review the Log File: A log file will be generated in the user's documents directory with the verification results. Review this file to ensure the Migration Test was successful.