import os
import pandas as pd
from datetime import datetime

"""
Key Features:
- Reads source and target CSV files into pandas DataFrames for efficient data handling.
- Validates the presence of a unique identifier field in both source and target files to ensure correct record matching.
- Compares columns by name, regardless of their order, ensuring accurate matching across both files.
- Detects discrepancies, including missing values, differing values, or unmatched rows.
- Generates a detailed report of discrepancies, including field names, row numbers, and mismatched values from both source and target files.
- Outputs a validation report (validation_report.txt) for in-depth review.
- Provides a summary of validation results in the terminal, showing whether the validation passed or failed, along with the total count of discrepancies found.

"""

def validate_data(source_file, target_file, report_file):
    unique_id_field = 'someIDField'  # Edit this line with the unique identifier field name present in your files.

    try:
        # Read the source and target files into DataFrames
        source_df = pd.read_csv(source_file, low_memory=False)
        target_df = pd.read_csv(target_file, low_memory=False)
        print("Files read successfully.")
    except Exception as e:
        write_report(report_file, f"Error reading files: {e}\n")
        print("Validation failed! Please check the report file for details.")
        return

    # Drop rows that are completely empty
    source_df.dropna(how='all', inplace=True)
    target_df.dropna(how='all', inplace=True)

    # Check if the unique identifier field exists in both DataFrames
    if unique_id_field not in source_df.columns or unique_id_field not in target_df.columns:
        write_report(report_file, f"Validation failed!!\nThe unique identifier field '{unique_id_field}' is missing in one of the files.\n")
        print("Validation failed! Please check the report file for details.")
        return

    # Drop rows where the unique identifier is missing
    source_df.dropna(subset=[unique_id_field], inplace=True)
    target_df.dropna(subset=[unique_id_field], inplace=True)

    # Ensure the unique ID fields are in string format for consistent comparison
    source_df[unique_id_field] = source_df[unique_id_field].astype(str)
    target_df[unique_id_field] = target_df[unique_id_field].astype(str)

    # Add row numbers to both DataFrames
    source_df['row_number'] = source_df.index
    target_df['row_number'] = target_df.index

    # Set the unique identifier as the index for easier alignment
    source_df.set_index(unique_id_field, inplace=True)
    target_df.set_index(unique_id_field, inplace=True)

    # Merge DataFrames on the unique identifier
    merged_df = pd.merge(source_df, target_df, how='outer', on=unique_id_field, suffixes=('_source', '_target'))

    discrepancies = []

    # Check for missing unique identifiers in the source and target files
    missing_in_target = merged_df[merged_df.filter(like='_source').isna().all(axis=1)]
    missing_in_source = merged_df[merged_df.filter(like='_target').isna().all(axis=1)]

    # Log discrepancies related to missing IDs
    discrepancies.extend(log_missing_discrepancies(missing_in_target, 'target', unique_id_field))
    discrepancies.extend(log_missing_discrepancies(missing_in_source, 'source', unique_id_field))

    # Filter out rows with missing IDs from further comparison
    valid_ids = merged_df[~merged_df.index.isin(missing_in_target.index) & ~merged_df.index.isin(missing_in_source.index)]

    # Iterate through each field (excluding the unique identifier and row number) to find discrepancies
    for field in source_df.columns:
        if field in [unique_id_field, 'row_number']:
            continue
        
        discrepancies.extend(compare_fields(valid_ids, field))

    # Create the report content
    report_content = create_report(discrepancies)
    
    # Write the report content to the file
    write_report(report_file, report_content)

    # Print the summary to the terminal
    print_summary(discrepancies, report_file)

# Write content to the report file.
def write_report(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing report file: {e}")

# Log discrepancies related to missing unique IDs.
def log_missing_discrepancies(df, file_type, unique_id_field):
    discrepancies = []
    for index, row in df.iterrows():
        discrepancies.append({
            'Field': unique_id_field,
            'Source Row Number': 'NaN' if file_type == 'target' else row.get('row_number_source', 'NaN') + 1,
            'Target Row Number': row.get('row_number_target', 'NaN') + 1 if file_type == 'target' else 'NaN',
            'Value source': 'NaN' if file_type == 'target' else index,
            'Value target': index if file_type == 'target' else 'NaN'
        })
    return discrepancies

# Compare values of a field in both source and target DataFrames.
def compare_fields(df, field):

    discrepancies = []
    source_field = f'{field}_source'
    target_field = f'{field}_target'

    for index, row in df.iterrows():
        src_value = row.get(source_field)
        tgt_value = row.get(target_field)
        src_row_number = row.get('row_number_source', 'NaN') + 1
        tgt_row_number = row.get('row_number_target', 'NaN') + 1

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
    
    return discrepancies

# Create the content of the report.
def create_report(discrepancies):
    # Current timestamp to be added in the report
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    report_content = "***********************************************\n"
    report_content += "***** V A L I D A T I O N   R E P O R T ******\n"
    report_content += "**********************************************\n"
    report_content += "\n"
    report_content += f"Generated on: {now}\n"
    report_content += "\n"

    if discrepancies:
        report_content += "Validation failed!!\n"
        report_content += "\n"
        report_content += f"Discrepancies found: {len(discrepancies)}\n"
        report_content += "\n"
        report_content += "--------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        report_content += "DETAILS OF DISCREPANCIES:\n"
        report_content += "--------------------------------------------------------------------------------------------------------------------------------------------------------\n"
        report_content += "\n"
        for discrepancy in discrepancies:
            report_content += (f"--> Field: {discrepancy['Field']} ; Source Row Number: "
                               f"{discrepancy['Source Row Number']} ; Target Row Number: "
                               f"{discrepancy['Target Row Number']} ; Value source: "
                               f"{discrepancy['Value source']} ; Value target: "
                               f"{discrepancy['Value target']}\n")
        report_content += "\n"
        report_content += "--------------------------------------------------------------------------------------------------------------------------------------------------------\n"
    else:
        report_content += "Validation passed!! - No discrepancies found \n"

    return report_content

# prints a summary in terminal
def print_summary(discrepancies, report_file):
    if discrepancies:
        print(f"Validation failed! - {len(discrepancies)} discrepancies found.")
    else:
        print("Validation passed!! - No discrepancies found")
    print(f"Please check the report file at: {report_file}")

def main():
    # Define the path to the Documents folder
    DOCUMENTS_PATH = os.path.expanduser('~/Documents')
    
    # Define file paths
    source_file = os.path.join(DOCUMENTS_PATH, 'source.csv')
    target_file = os.path.join(DOCUMENTS_PATH, 'target.csv')
    report_file = os.path.join(DOCUMENTS_PATH, 'validation_report.txt')
    
    # Validate data
    validate_data(source_file, target_file, report_file)

if __name__ == "__main__":
    main()

















































