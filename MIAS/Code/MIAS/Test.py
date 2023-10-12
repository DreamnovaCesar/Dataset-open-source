import pandas as pd

txt_file = r"C:\Users\Slaye\OneDrive\Escritorio\Code Tesis\Code\Tesis\Datasets\MIAS\Code\MIAS\Info.txt"
df = pd.read_csv(txt_file)

csv_file = 'output.csv'
df.to_csv(csv_file, index=False)