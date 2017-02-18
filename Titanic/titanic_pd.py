import pandas as pd
import numpy as np

df = pd.read_csv('train.csv', header=0)


# df.describe() Invalid value encountered in percentile
df['Gender'] = df['Sex'].map(lambda x:x[0].upper())

df['Gender'] = df['Sex'].map({'female': 0, 'male': 1}).astype(int)

# Dealing with missing values of age
# Fill with noise? Median? Mean?

median_ages = np.zeros((2,3))
for i in range(0,2):
    for j in range(0,3):
        median_ages[i,j] = df[(df['Gender'] == i) &\
                              (df['Pclass'] == j+1)]['Age'].dropna().median()

print median_ages
