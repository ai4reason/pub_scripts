import pandas as pd
import sys

read_file = pd.read_csv (sys.argv[1] + '.csv',sep=";",header=None)
read_file.to_excel (sys.argv[1] + '.xlsx', index = None, header=None)
