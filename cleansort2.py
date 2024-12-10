import pandas as pd
import unicodedata
import sys
import argparse

def clean_data(df):
    """Clean unwanted characters and normalize text in the DataFrame."""
    # Normalize all string columns in the DataFrame
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: unicodedata.normalize('NFKD', x) if isinstance(x, str) else x)
    
    # Replace remaining unwanted characters
    df = df.replace(r'\s+', ' ', regex=True)  # Replace extra spaces/newlines
    df = df.replace(r'[\u2018\u2019\u201C\u201D]', "'", regex=True)  # Replace curly quotes with straight ones
    return df

# Accept the file path as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python cleansort.py <path_to_your_csv_file>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    # Reading the file with the correct encoding
    df = pd.read_csv(file_path, encoding='ISO-8859-1')  # Use 'utf-8' if ISO doesn't work
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found.")
    sys.exit(1)

# Clean the DataFrame
df_cleaned = clean_data(df)

# Save the cleaned file
df_cleaned.to_csv('cleaned_file.csv', index=False)

def find_columns(df):
    """Find the relevant columns dynamically based on keywords."""
    help_col = None
    unhelp_col = None
    suggestion_col = None

    for col in df.columns:
        if "HELPED" in col.upper():
            help_col = col
        elif "UNHELPFUL" in col.upper():
            unhelp_col = col
        elif "SUGGESTIONS" in col.upper():
            suggestion_col = col

    if not all([help_col, unhelp_col, suggestion_col]):
        raise ValueError("Could not find all required columns in the input file.")

    return help_col, unhelp_col, suggestion_col

def split_original_csv(file_path):
    """Split the original CSV into three separate dataframes and save them."""
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {file_path} with {len(df)} rows.")

        # Clean the data
        df = clean_data(df)

        # Find the relevant columns
        help_col, unhelp_col, suggestion_col = find_columns(df)

        # Create individual dataframes and rename columns
        df_question1 = df[[help_col]].dropna().rename(columns={help_col: "Question1_Helpful"})
        df_question2 = df[[unhelp_col]].dropna().rename(columns={unhelp_col: "Question2_Unhelpful"})
        df_question3 = df[[suggestion_col]].dropna().rename(columns={suggestion_col: "Question3_Suggestions"})

        # Save the renamed dataframes to new CSVs
        df_question1.to_csv('helpful_responses.csv', index=False)
        df_question2.to_csv('unhelpful_responses.csv', index=False)
        df_question3.to_csv('suggestions_responses.csv', index=False)

        print("Files saved as 'helpful_responses.csv', 'unhelpful_responses.csv', and 'suggestions_responses.csv'")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    """Main function to handle command-line input and run the program."""
    parser = argparse.ArgumentParser(description="Clean and split survey data.")
    parser.add_argument("file", type=str, help="Path to the original survey CSV file")

    args = parser.parse_args()

    # Split the original CSV into separate files
    split_original_csv(args.file)

if __name__ == "__main__":
    main()
