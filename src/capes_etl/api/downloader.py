import requests

CAPES_BASE_URL = 'https://dadosabertos.capes.gov.br/api/3/action'

def fetch_packages_ckan(url: str, query: str) -> list:
    '''
    _summary_

    Args:
        url (str): _description_
        query (str): _description_

    Returns:
        list: _description_
    '''    
    response = requests.get(
        f'{CAPES_BASE_URL}/package_search',
        params={'q': query}
    )
    response.raise_for_status()
    data = response.json()
    results = data.get('result',{}).get('results',[])
    return results

results = fetch_packages_ckan(CAPES_BASE_URL, 'catalogo de teses')
num_results = len(results)
print(f'Found {num_results} entries')

for i, result in enumerate(results):
    print(f'Result {i}: {result['name']}\nID: {result['id']}\n')

print(type(results))