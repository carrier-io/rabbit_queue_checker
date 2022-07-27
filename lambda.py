import json
from arbiter import Arbiter
import requests
from os import environ


def handler(event=None, context=None):
    try:
        user = event[0]["user"] if event else environ.get("rabbit_project_user")
        password = event[0]["password"] if event else environ.get("rabbit_project_password")
        vhost = event[0]["vhost"] if event else environ.get("rabbit_project_vhost")
        arbiter = Arbiter(host=environ.get("rabbit_host"), port=5672, user=user, password=password, vhost=vhost,
                          timeout=120)
        try:
            queues = list(arbiter.workers().keys())
        except:
            queues = []
        arbiter.close()

        url = f"{environ.get('galloper_url')}/api/v1/projects/rabbitmq/{vhost}"
        data = {"queues": json.dumps(queues)}
        headers = {'content-type': 'application/json'}
        if environ.get("token"):
            headers['Authorization'] = f'bearer {environ.get("token")}'
        requests.put(url, json=data, headers=headers)

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
    return {
        'statusCode': 200,
        'body': json.dumps('Done')
    }
