import requests, os, pathlib, json
path = str(pathlib.Path(__file__).parent.resolve())
os.chdir(path)

def get_prices(city):
    with open('prices.json') as data:
        index = json.load(data)
        data.close()
    tier = 'T4'+'_'
    api_base = 'https://www.albion-online-data.com/api/v2/stats/prices/'+tier
    api_end = '.json?locations='+str(city)
    for token in index:
        print(token)
        for category in index[token]:
            total = 0
            if category != 'value':
                print(category)
                for item in index[token][category]:
                    if item != 'NONE':
                        item_address = item
                        api_url = api_base+item_address+api_end
                        api_response = requests.get(api_url)
                        response_json = api_response.json()
                        sell_price = response_json[0]['sell_price_min']
                        if sell_price > 0:
                            index[token][category][item] = sell_price
                            total += 1
                            print('updated',str(total)+'/9')
    with open('prices.json', 'w') as outfile:
        json.dump(index, outfile)
        outfile.close()

def get_profit():
    with open('prices.json') as data:
        index = json.load(data)
        data.close()
    mostProfitable = [0, 0]
    for item in index:
        cost = 50*index[item]['value']
        for item2 in index[item]:
            if item2 != 'value':
                count = 0
                avg = 0
                for item3 in index[item][item2]:
                    count = count + 1
                    avg = avg + index[item][item2][item3]
                avg = avg/count
                profit = avg / cost
                print([cost, (item, item2), profit])
                if profit > mostProfitable[1]:
                    mostProfitable = [(item, item2), profit]
    return mostProfitable

get_prices('Thetford')
get_profit()