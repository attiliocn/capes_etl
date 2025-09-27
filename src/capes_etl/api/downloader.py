import requests
from requests.adapters import HTTPAdapter, Retry
import os

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

def fetch_package_resources(package_id: str) -> list:
    '''
    _summary_

    Args:
        package_id (str): _description_

    Returns:
        list: _description_
    '''         
    response = requests.get(
        f'{CAPES_BASE_URL}/package_show',
        params={'id': package_id}
    )
    response.raise_for_status()
    data = response.json()
    results = data.get('result',{}).get('resources',[])
    return results

def select_resources(packages_resources: list) -> list:
    '''
    _summary_

    Args:
        packages_resources (list): _description_

    Returns:
        list: _description_
    '''
    selected_resources_list = []
    for resource in packages_resources:
        if resource['format'] == 'CSV':
            selected_resources_list.append(resource)
    return selected_resources_list 

session = requests.Session()
retries = Retry(
    total=5,              # total retries
    backoff_factor=1,     # sleep 1s, 2s, 4s, ...
    status_forcelist=[500, 502, 503, 504],
)
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

def download_resource(resource_metadata: dict, dest_folder: str) -> None:
    dest_path = os.path.join(dest_folder, resource_metadata['name']) + '.csv'
    with session.get(resource_metadata['url'], stream=True, timeout=30) as response:
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    f.write(chunk)

# query CAPES CKAN for entries
results = fetch_packages_ckan(CAPES_BASE_URL, 'catalogo de teses')
num_results = len(results)
print(f'Found {num_results} entries')

for i, result in enumerate(results):
    print(f'Result {i}: {result['name']}\nID: {result['id']}\n')

print(type(results))

for k in results[0].keys():
    print(k)

package_id_tests = results[0]['id']
print(package_id_tests)

package_details = fetch_package_resources(package_id_tests)
for k in package_details[0].keys():
    print(k)
print()
print(package_details[0]['format'])

to_download = select_resources(package_details)
print(to_download)
print(len(to_download))