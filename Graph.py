import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

column = "prefix"
title = "Frequentie tussenvoegsels --"
xlabel = "Tussenvoegsels"
ylabel = "Frequentie"
graphType = "bar"
maxBars = 30
toLowerCase = True

conn = sqlite3.connect("leerlingen.db")
prefixes = pd.read_sql(f"SELECT {column} FROM LEERLINGEN WHERE {column} != ''", conn)
prefixes = prefixes[column]
if (toLowerCase):
    prefixes = prefixes.str.lower()
values = prefixes.value_counts().sort_values(ascending=False).head(maxBars)
values.plot(kind=graphType, title=title, xlabel=xlabel, ylabel=ylabel)
plt.tight_layout()
plt.show()