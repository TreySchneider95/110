from mock_data import catalog
from pprint import pprint

# pprint(catalog)


counter = 0
def find_prod(text):
    matching = [x['title'] for x in catalog if text.lower() in x['title'].lower()]
    return [f"title: {x['title']}, price: {x['price']}" for x in catalog if text.lower() in x['title'].lower()]

    
    


print(find_prod('ock'))