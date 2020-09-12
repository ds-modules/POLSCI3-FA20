#What I used to create trump_immigrants.csv
import matplotlib.pyplot as plt
import pandas as pd
states = {'Alabama': 'AL',  'Alaska': 'AK',  'Arizona': 'AZ',  'Arkansas': 'AR',  'California': 'CA',  'Colorado': 'CO',  'Connecticut': 'CT',  'Delaware': 'DE',  'Florida': 'FL',  'Georgia': 'GA',  'Hawaii': 'HI',  'Idaho': 'ID',  'Illinois': 'IL',  'Indiana': 'IN',  'Iowa': 'IA',  'Kansas': 'KS',  'Kentucky': 'KY',  'Louisiana': 'LA',  'Maine': 'ME',  'Maryland': 'MD',  'Massachusetts': 'MA',  'Michigan': 'MI',  'Minnesota': 'MN',  'Mississippi': 'MS',  'Missouri': 'MO',  'Montana': 'MT',
          'Nebraska': 'NE',  'Nevada': 'NV',  'New Hampshire': 'NH',  'New Jersey': 'NJ',  'New Mexico': 'NM',  'New York': 'NY',  'North Carolina': 'NC',  'North Dakota': 'ND',  'Ohio': 'OH',  'Oklahoma': 'OK',  'Oregon': 'OR',  'Pennsylvania': 'PA',  'Rhode Island': 'RI',  'South Carolina': 'SC',  'South Dakota': 'SD',  'Tennessee': 'TN',  'Texas': 'TX',  'Utah': 'UT',  'Vermont': 'VT',  'Virginia': 'VA',  'Washington': 'WA',  'West Virginia': 'WV',  'Wisconsin': 'WI',  'Wyoming': 'WY'}

immigrants = pd.read_excel("immigrantpopshare.xlsx", header=2).dropna(subset=['State']).iloc[:52, :3].rename(columns={
    "Unauthorized\nimmigrant\npopulation": "Immigrant Population", "Unauthorized immigrant % of population": "Unauthorized Immigrant Population Share"})
immigrants['State'] = immigrants.State.apply(
    lambda val: states[val] if val in states else None)
immigrants.dropna().set_index('State')
votes = pd.read_excel("federalelections2016.xlsx", sheet_name=2, header=3).drop(columns=['Trump (R)', 'Clinton (D)']).rename(columns={
    'Unnamed: 0': 'State', 'Trump (R).1': 'Trump', 'Clinton (D).1': 'Clinton'}).set_index('State')  # .apply(lambda row: row['Trump']/row['Total Vote'], axis=1)
for cand in ('Trump', 'Clinton'):
    votes[cand+' Vote Share'] = votes[cand]/votes['Total Vote']
merged = votes.merge(immigrants, on='State')
merged.iloc[:50, :].to_csv('trump_immigrants.csv', index=False)
