import pandas as pd
from pathlib import Path

# Function to read all csv files and return a list with file names and dataframes
def read_csv_files(path:str):
    # Get all csv files in the path
    csv_files = Path(path).glob('*.csv')
    # Create a list of dataframes
    dfs = [pd.read_csv(file) for file in csv_files]
    # Get the name of each file inside the path
    p = Path(path)
    csv_files = list(p.glob('*.csv'))
    return [dfs, csv_files]

def process_row(row, iteration:int, label:str):
    # Delete the Time column
    del row['Time']
    # Rename the Channel x column to Chxlabel
    rename = {f'Channel {i}': f'CH{i}{label}' for i in range(1, 15)}
    # Add the iteration number as Time column
    row['Time'] = iteration + 1

    for key, value in rename.items():
        row[value] = row[key]
        del row[key]

    return row

def place_classification_column(merge_df): 

    # Create classification labels for each row 
    column = ['open_hand' for _ in range(20)] + ['rest' for _ in range(20)] + ['close_hand' for _ in range(20)] + ['rest' for _ in range(10)]
    
    # Set the classification column values 
    merge_df['Classification'] = column
    return merge_df

# Function to delete rename and apply changes to the dataframes
def process_dataframes(dataframes):
    drop_columns = ['Epoch', 'Event Id', 'Event Date', 'Event Duration']
    new_merge_df = pd.DataFrame()
    for i in range(len(dataframes[0])):
        means = []
        stds = []
        # Copy the dataframe 
        df = dataframes[0][i].copy()
        # Delete the columns that are not needed
        df.drop(columns=drop_columns, inplace=True)
        # Rename the Time:256Hz column to Time
        df.rename(columns={'Time:256Hz':'Time'}, inplace=True)
        # Calculate the iterations dividing the number of rows in the dataframe by 256
        iterations = int(len(df) / 256)
        # Iterate each 256 rows and calculate the mean of each column
        for j in range(iterations):
            # Calculate the start and end of the 256 rows
            start = j * 256
            end = start + 256
            # Calculate the mean of each column
            means.append(process_row(df.iloc[start:end].mean(), j, 'MEAN'))
            # Calculate the standard deviation of each column
            stds.append(process_row(df.iloc[start:end].std(), j, 'STD'))
        mean_dataframe = pd.DataFrame(means)

        std_dataframe = pd.DataFrame(stds)
        # Concatenate the mean and std dataframes
        new_dataframe = pd.merge(mean_dataframe, std_dataframe, on='Time')

        # Ignore first seconds of resting state
        new_dataframe = new_dataframe.iloc[10:]
        
        # Add classification column
        new_dataframe = place_classification_column(new_dataframe)

        # Remove all rows with rest in the classification column
        new_dataframe = new_dataframe[new_dataframe.Classification != 'rest']

        # Save the new dataframe to a csv file
        path = dataframes[1][i]
        # Check if exist the folder processed in the parent folder of the csv file
        if not Path(path.parent / 'Processed').exists():
            # Create the folder processed
            Path(path.parent / 'Processed').mkdir()
        # Save the new dataframe to a csv file
        new_dataframe.to_csv(path.parent / 'Processed' / path.name, index=False)

        # Concatenate the new dataframe to the merge dataframe ignoring the Time column and index
        new_dataframe.drop(columns=['Time'], inplace=True)
        new_merge_df = pd.concat([new_merge_df, new_dataframe], ignore_index=True)
    
    # Change the open_hand and close_hand values to 0 and 1
    new_merge_df.Classification.replace({'open_hand':0, 'close_hand':1}, inplace=True)
    # Save the merge dataframe to a csv file
    new_merge_df.to_csv(path.parent / 'Processed' / 'merged.csv', index=False)

if __name__ == '__main__':
    # Read all csv files
    dataframes = read_csv_files('data/Records/Raw')
    # Process the dataframes
    process_dataframes(dataframes)