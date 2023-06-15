import requests

RUNDECK_URL = 'http://rundeck.imbrisa.io'
RUNDECK_TOKEN = '4YSfJvkW9op0k00UE3p5evy67aQhxbQH'
RUNDECK_HEADERS = {
    'X-Rundeck-Auth-Token': RUNDECK_TOKEN,
    'Accept': 'application/json'
}


def getRundeckJobStatus(job_id):
    
    endpoint = f'/api/43/execution/{job_id}'

    req = requests.get(
        f'{RUNDECK_URL}/{endpoint}',
        headers=RUNDECK_HEADERS)
    
    if req.status_code == 200:
        return req.json()
    else:
        raise Exception(req.reason)

getRundeckJobStatus(232)