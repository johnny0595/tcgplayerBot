import requests

filters = {'algorithm': '',
 'context': {'cart': {}, 'shippingCountry': 'NL'},
 'filters': {'match': {},
  'range': {},
  'term': {'productLineName': ['yugioh'], 'setName': ['the-grand-creators']}},
 'from': 0,
 'listingSearch': {'context': {'cart': {}},
  'filters': {'exclude': {'channelExclusion': 0},
   'range': {'quantity': {'gte': 1}},
   'term': {'channelId': 0, 'sellerStatus': 'Live'}}},
 'size': 10,
 'sort': {}}

response = requests.post(
    "https://mpapi.tcgplayer.com/v2/search/request?q=&isList=true",
    headers={
        'Content-type':'application/json', 
        'Accept':'application/json'
    },
    params={"q": "", "isList": True},
    json=filters
).json()