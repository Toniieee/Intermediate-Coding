#importing function for code to work
import requests
import csv
import matplotlib.pyplot as plt
import pandas as pd


#Accessing API protocol - giving url and access with personal key
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'ef32ae2b-304e-4c9a-8fa2-ded32deb31a2',
}

params = {
    'start' : '1',
    'limit' : '10',
    'convert' : 'USD'
}
#Reponse from source code for checking (leave this line unchanged)
response = requests.get(url, params=params,  headers=headers)
response_json = response.json()

if response.status_code == 200:
    data = response_json['data']
else:
    print("Error fetching data:", response.status_code)
    exit()

csv_file = "coinmarketcap_data.csv"
csv_headers = ['symbol', 'name', 'price', 'market_cap', 'volume_24h', 'percent_change_24h']

#overwrite csv file with data from exacting API
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)
    writer.writeheader()
    
    for coin in data:
        writer.writerow({
            'symbol': coin['symbol'],
            'name': coin['name'],
            'price': coin['quote']['USD']['price'],
            'market_cap': coin['quote']['USD']['market_cap'],
            'volume_24h': coin['quote']['USD']['volume_24h'],
            'percent_change_24h': coin['quote']['USD']['percent_change_24h'],
        })
        
# Prepare coin data for DataFrame
coin_data = []
for coin in data:
    coin_data.append({
        'ID': coin['id'],
        'Name': coin['name'],
        'Code': coin['symbol'],
        'Year': 2024, 
        'Price (USD)': coin['quote']['USD']['price'],
        'Market Cap (USD)': coin['quote']['USD']['market_cap'],
        '24h Volume (USD)': coin['quote']['USD']['volume_24h'],
        'Percent Change 24h (%)': coin['quote']['USD']['percent_change_24h'],
    })

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(coin_data)

# Format columns for consistency (e.g., price to 2 decimal places)
df['Price (USD)'] = df['Price (USD)'].apply(lambda x: f"${x:,.2f}")
df['Market Cap (USD)'] = df['Market Cap (USD)'].apply(lambda x: f"${x:,.0f}")
df['24h Volume (USD)'] = df['24h Volume (USD)'].apply(lambda x: f"${x:,.0f}")
df['Percent Change 24h (%)'] = df['Percent Change 24h (%)'].apply(lambda x: f"{x:,.2f}%")

# Sort the DataFrame by Market Cap (USD) in descending order
df_sorted = df.sort_values(by='Market Cap (USD)', ascending=False)

# Create a bar plot using Matplotlib with the sorted DataFrame
plt.figure(figsize=(12, 6))
plt.bar(df_sorted['Name'], df_sorted['Market Cap (USD)'])
plt.xlabel('Cryptocurrency')
plt.ylabel('Market Cap (USD)')
plt.title('Market Cap of Top 5 Cryptocurrencies (Ranked)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print(pd)