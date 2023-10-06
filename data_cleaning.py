import pandas as pd

def replace(column, to_replace, replace_with):
    df[column] = df[column].apply(lambda x: x.replace(to_replace, replace_with))
    
def start(column, value):
    df[column] = df[column].apply(lambda x: x[value:])

df_original = pd.read_csv('companies.csv')

df = df_original.copy()

del df['Unnamed: 0']

start('Specialities', 2)

df['Status'] = df['Status'].apply(lambda x: str(x))

replace('Size', '  ', '')
replace('Status', '  ', '')
replace('Followers on Stack Overflow', '  ', '')

start('Followers on Stack Overflow', 2)
start('Size', 1)
start('Status', 1)
start('Location', 1)
start('Type', 1)

replace('Followers on Stack Overflow', '\n', '')
replace('Size', '\n', '')
replace('Status', '\n', '')

df['Followers on Stack Overflow'] = df['Followers on Stack Overflow'].apply(lambda x: x.replace(x[-1], ''))
df['Followers on Stack Overflow'][60] = 1800

df['Followers on Stack Overflow'] = df['Followers on Stack Overflow'].apply(lambda x: float(x))

df['Size'] = df['Size'].apply(lambda x: x.replace(x[-1], ''))
df['Status'] = df['Status'].apply(lambda x: x.replace(x[-1], ''))

df['Status'][62] = float('nan')

df['Link'] = df['Link'].apply(lambda x: 'https://stackoverflow.com' + x)

replace('Size', ' ', '')
replace('Size', 'employees', '')

df['Size_least'] = df['Size'].apply(lambda x: x.split('-')[0] if '-' in x else x)
df.insert(6, 'Size_least', df.pop('Size_least'))
df['Size_Max'] = df['Size'].apply(lambda x: x.split('-')[1] if '-' in x else 'nan')
df.insert(7, 'Size_Max', df.pop('Size_Max'))

df['Size_least'] = df['Size_least'].apply(lambda x: (x+'00' if '.' in x else x+'000') if 'k' in x else x)
df['Size_Max'] = df['Size_Max'].apply(lambda x: (x+'00' if '.' in x else x+'000') if 'k' in x else x)

replace('Size_least', '.', '')
replace('Size_Max', '.', '')
replace('Size_least', '+', '')
replace('Size_Max', '+', '')
replace('Size_least', 'k', '')
replace('Size_Max', 'k', '')

df['Size_least'] = df['Size_least'].apply(lambda x: float(x))
df['Size_Max'] = df['Size_Max'].apply(lambda x: float(x))

del df['Size']

df.to_csv('companies_cleaned.csv')