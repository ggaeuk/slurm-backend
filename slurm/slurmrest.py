import requests
import time
import json

from jwt import JWT
from jwt.jwk import jwk_from_dict

from config import SLURM_SETTINGS


def get_slurm_jwt(username: str):
    signing_key = jwk_from_dict({
        'kty': 'oct',
        'k': SLURM_SETTINGS['private_key']
    })

    message = {
        "exp": int(time.time() + 3600),
        "iat": int(time.time()),
        "sun": username
    }
    compact_jws = JWT().encode(message, signing_key, alg='HS256')

    return compact_jws


def get_slurm_ping(username: str):
    compact_jws = get_slurm_jwt(username)
    headers = {
        'X-SLURM-USER-NAME': username,
        'X-SLURM-USER-TOKEN': compact_jws,
        'Content-Type': 'application/json'
    }
    url = 'http://localhost:6820/slurm/v0.0.38/ping'
    response = requests.get(url, headers=headers)

    return response.json()


def get_slurm_diag(username: str):
    compact_jws = get_slurm_jwt(username)
    headers = {
        'X-SLURM-USER-NAME': username,
        'X-SLURM-USER-TOKEN': compact_jws,
        'Content-Type': 'application/json'
    }
    url = 'http://localhost:6820/slurm/v0.0.38/diag'
    response = requests.get(url, headers=headers)

    return response.json()


def get_slurm_nodes(username: str):
    compact_jws = get_slurm_jwt(username)
    headers = {
        'X-SLURM-USER-NAME': username,
        'X-SLURM-USER-TOKEN': compact_jws,
        'Content-Type': 'application/json'
    }
    url = 'http://localhost:6820/slurm/v0.0.38/nodes'
    response = requests.get(url, headers=headers)

    return response.json()


def get_slurm_jobs(username: str):
    compact_jws = get_slurm_jwt(username)
    headers = {
        'X-SLURM-USER-NAME': username,
        'X-SLURM-USER-TOKEN': compact_jws,
        'Content-Type': 'application/json'
    }
    url = 'http://localhost:6820/slurm/v0.0.38/jobs'
    response = requests.get(url, headers=headers)

    return response.json()


def submit_job(username: str, job: dict):
    compact_jws = get_slurm_jwt(username)
    headers = {
        'X-SLURM-USER-NAME': username,
        'X-SLURM-USER-TOKEN': compact_jws,
        'Content-Type': 'application/json'
    }
    url = 'http://localhost:6820/slurm/v0.0.38/job/submit'
    response = requests.post(url, data=json.dumps(job), headers=headers)
    return response.json()


def delete_job(username: str, job_id: int):
    compact_jws = get_slurm_jwt(username)
    headers = {
        'X-SLURM-USER-NAME': username,
        'X-SLURM-USER-TOKEN': compact_jws,
        'Content-Type': 'application/json'
    }
    url = f'http://localhost:6820/slurm/v0.0.38/job/{job_id}'
    response = requests.delete(url, headers=headers)
    return response.json()
