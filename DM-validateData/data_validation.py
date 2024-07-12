import os
import pandas as pd

"""
Key Features:
- Reads source and target CSV files into pandas DataFrames.
- Validates the presence of a unique identifier field in both files.
- Compares each field's values between the source and target files.
- Identifies discrepancies where values differ or are missing in either file.
- Reports discrepancies with field names, values from both source and target files, and corresponding row numbers.
- Generates a detailed report file (validation_report.txt) for in-depth analysis.
- Provides a summary of validation results in the terminal, indicating whether the validation passed or failed and the total number of discrepancies found.

"""

def validate_data(source_file, target_file, report_file):

    unique_id_field = 'field1' # Edit this line if your files use a different unique identifier field name. 

    try:
        # Read the source and target files into DataFrames
        source_df = pd.read_csv(source_file)
        target_df = pd.read_csv(target_file)
    except Exception as e:
        report_content = f"Error reading files: {e}\n"
        with open(report_file, 'w') as file:
            file.write(report_content)
        print("Validation failed! Please check the report file for details.")
        return

    # Check if the unique identifier field exists in both DataFrames
    if unique_id_field not in source_df.columns or unique_id_field not in target_df.columns:
        report_content = f"Validation failed!!\nThe unique identifier field '{unique_id_field}' is missing in one of the files.\n"
        with open(report_file, 'w') as file:
            file.write(report_content)
        print("Validation failed! Please check the report file for details.")
        return

    # Add row numbers to both DataFrames
    source_df['row_number'] = source_df.index
    target_df['row_number'] = target_df.index

    # Set the unique identifier as the index for easier alignment
    source_df.set_index(unique_id_field, inplace=True)
    target_df.set_index(unique_id_field, inplace=True)

    # Merge DataFrames on the unique identifier
    merged_df = source_df.join(target_df, how='outer', lsuffix='_source', rsuffix='_target', sort=False)

    discrepancies = []

    # Check for missing unique identifiers in the target file
    missing_ids = merged_df[merged_df.filter(like='_target').isna().all(axis=1)]

    for index, row in missing_ids.iterrows():
        discrepancies.append({
            'Field': unique_id_field,
            'Source Row Number': row['row_number_source'] + 1,
            'Target Row Number': 'NaN',
            'Value source': index,
            'Value target': 'NaN'
        })

    # Iterate through each field (excluding the unique identifier and row number) to find discrepancies
    for field in source_df.columns:
        if field in [unique_id_field, 'row_number']:
            continue
        source_field = f'{field}_source'
        target_field = f'{field}_target'
        
        for index, row in merged_df.iterrows():
            src_value = row[source_field] if source_field in row else None
            tgt_value = row[target_field] if target_field in row else None
            src_row_number = row['row_number_source'] + 1 if 'row_number_source' in row else 'NaN'
            tgt_row_number = row['row_number_target'] + 1 if 'row_number_target' in row else 'NaN'

            if pd.notna(src_value) and pd.notna(tgt_value):
                if src_value != tgt_value:
                    discrepancies.append({
                        'Field': field,
                        'Source Row Number': src_row_number,
                        'Target Row Number': tgt_row_number,
                        'Value source': src_value,
                        'Value target': tgt_value
                    })
            elif pd.isna(src_value) and pd.notna(tgt_value):
                discrepancies.append({
                    'Field': field,
                    'Source Row Number': 'NaN',
                    'Target Row Number': tgt_row_number,
                    'Value source': 'NaN',
                    'Value target': tgt_value
                })
            elif pd.notna(src_value) and pd.isna(tgt_value):
                discrepancies.append({
                    'Field': field,
                    'Source Row Number': src_row_number,
                    'Target Row Number': 'NaN',
                    'Value source': src_value,
                    'Value target': 'NaN'
                })

    # Create the report content
    report_content = "*****R E P O R T*****\n"
    report_content += "*********************\n"
    if discrepancies:
        report_content += "Validation failed!!\n"
        report_content += f"Discrepancies found: {len(discrepancies)}\n"
        for discrepancy in discrepancies:
            report_content += (f"Field: {discrepancy['Field']} ; Source Row Number: "
                               f"{discrepancy['Source Row Number']} ; Target Row Number: "
                               f"{discrepancy['Target Row Number']} ; Value source: "
                               f"{discrepancy['Value source']} ; Value target: "
                               f"{discrepancy['Value target']}\n")
    else:
        report_content += "Validation passed!!\n"

    # Write the report content to the file
    with open(report_file, 'w') as file:
        file.write(report_content)

    # Print the summary to the terminal
    if discrepancies:
        print(f"Validation failed! - {len(discrepancies)} discrepancies found.")
    else:
        print("Validation passed!! - No discrepancies found")
    print(f"Please check the report file at: {report_file}")

def main():
    # Define the path to the Documents folder
    DOCUMENTS_PATH = os.path.expanduser('~/Documents')
    
    # Define file paths
    source_file = os.path.join(DOCUMENTS_PATH, 'source-AB.csv')
    target_file = os.path.join(DOCUMENTS_PATH, 'target-AB.csv')
    report_file = os.path.join(DOCUMENTS_PATH, 'validation_report.txt')
    
    # Validate data
    validate_data(source_file, target_file, report_file)

if __name__ == "__main__":
    main()

































