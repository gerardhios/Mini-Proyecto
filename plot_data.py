from matplotlib import pyplot as plt
import pandas as pd
from pathlib import Path

p = Path('data/Records/Raw/Processed')
csv_files = list(p.glob('*.csv'))

# drop the last element of the list because it is the merged dataframe
csv_files.pop()

columns = ["CH1MEAN","CH2MEAN","CH3MEAN","CH4MEAN","CH5MEAN","CH6MEAN","CH7MEAN","CH8MEAN","CH9MEAN","CH10MEAN","CH11MEAN","CH12MEAN","CH13MEAN","CH14MEAN","CH1STD","CH2STD","CH3STD","CH4STD","CH5STD","CH6STD","CH7STD","CH8STD","CH9STD","CH10STD","CH11STD","CH12STD","CH13STD","CH14STD"]

for file in csv_files:
    df = pd.read_csv(file, usecols=columns)

    # Create a new column with the time in seconds from 1 to 40
    df['Time'] = [i for i in range(1, 41)]

    # Plot all the means columns
    plt.figure(figsize=(10, 5))
    plt.plot(df.Time, df.CH1MEAN, label='CH1MEAN', marker='o')
    plt.plot(df.Time, df.CH2MEAN, label='CH2MEAN', marker='o')
    plt.plot(df.Time, df.CH3MEAN, label='CH3MEAN', marker='o')
    plt.plot(df.Time, df.CH4MEAN, label='CH4MEAN', marker='o')
    plt.plot(df.Time, df.CH5MEAN, label='CH5MEAN', marker='o')
    plt.plot(df.Time, df.CH6MEAN, label='CH6MEAN', marker='o')
    plt.plot(df.Time, df.CH7MEAN, label='CH7MEAN', marker='o')
    plt.plot(df.Time, df.CH8MEAN, label='CH8MEAN', marker='o')
    plt.plot(df.Time, df.CH9MEAN, label='CH9MEAN', marker='o')
    plt.plot(df.Time, df.CH10MEAN, label='CH10MEAN', marker='o')
    plt.plot(df.Time, df.CH11MEAN, label='CH11MEAN', marker='o')
    plt.plot(df.Time, df.CH12MEAN, label='CH12MEAN', marker='o')
    plt.plot(df.Time, df.CH13MEAN, label='CH13MEAN', marker='o')
    plt.plot(df.Time, df.CH14MEAN, label='CH14MEAN', marker='o')
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Mean')
    plt.title('Mean of each channel')

    plt.show()
input()