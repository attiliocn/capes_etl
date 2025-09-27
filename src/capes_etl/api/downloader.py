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
print(f'Found {len(results)} entries')
print(f'Result 0 is {type(results[0])}')
print(f'Result 0 has the keys: {results[0].keys()}')
print()
for i, result in enumerate(results):
    print(f'Result {i}\n{result['name']}\nID: {result['id']}\n')

# Fetch the details of some package
package_id_tests = results[0]['id']
package_resources = fetch_package_resources(package_id_tests)
print(f'Package resources is {type(package_resources)}')
print(f'Package has {len(package_resources)} resources')
print(f'Resource 0 has the keys: {package_resources[0].keys()}')

# Select only csv files from the package's resources
print(f'Will select only csv files from resources')
selected_resources = select_resources(package_resources)
print(f'Selected {len(selected_resources)} resources')
for i, resource in enumerate(selected_resources):
    print(f'Resource {i}')
    print(f'Filename: {resource['name']}')
    print(f'Size: {resource['size']}')
    print(f'URL: {resource['url']}')
    print(f'')

for resource in selected_resources:
    download_resource(resource, '/home/attilio/repositories/capes_etl/data/raw')