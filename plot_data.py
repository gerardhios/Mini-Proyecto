from matplotlib import pyplot as plt
import pandas as pd 

columns = ["Time","CH1MEAN","CH2MEAN","CH3MEAN","CH4MEAN","CH5MEAN","CH6MEAN","CH7MEAN","CH8MEAN","CH9MEAN","CH10MEAN","CH11MEAN","CH12MEAN","CH13MEAN","CH14MEAN","CH1STD","CH2STD","CH3STD","CH4STD","CH5STD","CH6STD","CH7STD","CH8STD","CH9STD","CH10STD","CH11STD","CH12STD","CH13STD","CH14STD"]

df = pd.read_csv("data/Records/Raw/Processed/2023.10.13-12.18.34.csv", usecols=columns)

plt.plot(df.Time, df.CH1MEAN, marker="o")

plt.show()