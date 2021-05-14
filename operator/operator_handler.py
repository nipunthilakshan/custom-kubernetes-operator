import kopf
import kubernetes
import json
import requests
import logging
import sys
import base64
import time
from requests.exceptions import HTTPError

log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.DEBUG)
log.addHandler(out_hdlr)
log.setLevel(logging.DEBUG)

consumer_key = "RfI05Aa7KOxnOYVWK0fe6hgNXmca"
consumer_secret = "LOkDasjJtByow8SHobFLdCOKU9sa"
apim_token_url = "https://localhost:8243/token?grant_type=client_credentials&scope=apim:api_view " \
                 "apim:api_create apim:api_publish"
apim_api_create_url = "https://localhost:9443/api/am/publisher/v1/apis/import-openapi"
apim_api_publish_url = "https://localhost:9443/api/am/publisher/v1/apis/change-lifecycle?action=Publish&apiId="
name_space = "selfcare"
delay_time = 7


# This method will be triggered when a ODA component is created in kubernetes cluster.
@kopf.on.create('oda.tmforum.org', 'v1alpha1', 'components')
def create_service(meta, spec, **kwargs):
    log.debug("ODA creation triggered")
    # Add delay since the service need to be deployed
    time.sleep(delay_time)
    try:
        apis = spec['coreFunction']['exposedAPIs']
        for api in apis:
            api_name = api['name']
            api_path = api['path']
            api_implementation = api['implementation']
            port = api['port']
            log.debug(
                f'api_name: {api_name},api_path: {api_path},api_implementation: {api_implementation},port: {port}')
            create_api(api_name, api_path, str(port), api_implementation)

    except Exception as err:
        log.error(f'Other error occurred: {err}')

    return {'message': "service creation triggered"}


# WSO2 APIM token generation.
def token_generation():
    log.debug("Token generation started")
    try:
        token = "dump"
        header_key = encoder()
        headers = {'Authorization': header_key}
        response = requests.post(apim_token_url, headers=headers, verify=False)
        if response.status_code == 200:
            log.debug("Token creation success")
            response_body = response.json()
            token = response_body["access_token"]
        else:
            log.error(f'Invalid response code: {response.status_code}')
    except HTTPError as http_err:
        log.error(f'HTTP error occurred: {http_err}')
    except Exception as err:
        log.error(f'Other error occurred: {err}')

    return token


def encoder():
    key = consumer_key + ":" + consumer_secret
    key_bytes = key.encode('ascii')
    base64_bytes = base64.b64encode(key_bytes)
    base64_key = base64_bytes.decode('ascii')
    header_key = "Basic " + base64_key
    return header_key


# Create an api in WSO2 APIM
def create_api(service_name, path, port, imlementation):
    log.debug("Api generation started")
    try:
        token = token_generation()
        token_bearer = "Bearer " + token
        # swagger_url = 'http://' + service_name + "." + name_space + '.svc.cluster.local' + '/v2/api-docs'
        swagger_url = 'http://' + service_name + path
        headers = {'Authorization': token_bearer, 'Content-Type': 'multipart/form-data'}
        log.debug(f"swagger: {swagger_url}")
        additional_data = {
            'name': service_name,
            'version': '1.0',
            'context': service_name,
            'policies': ['Bronze'],
            'endpointConfig': {
                'endpoint_type': 'http',
                'sandbox_endpoints': {'url': service_name + ':' + port},
                'production_endpoints': {'url': service_name + ':' + port},
            },
            'gatewayEnvironments': ['Production and Sandbox']
        }

        form_data = {'url': swagger_url,
                     'additionalProperties': json.dumps(additional_data)}
        response = requests.post(apim_api_create_url, headers=headers, files=form_data, verify=False)
        log.debug(f"response: {response.content}")
        if response.status_code == 201:
            log.debug("Api creation success")
            response_body = response.json()
            application_id = response_body["id"]
            publish_api(application_id, token)
        else:
            log.error(f'Invalid response code: {response.status_code}')

    except HTTPError as http_err:
        log.error(f'HTTP error occurred: {http_err}')
    except Exception as err:
        log.error(f'Other error occurred: {err}')


# Publish an api in WSO2 APIM
def publish_api(id, auth_token):
    try:
        log.debug("Api publish started")
        headers = {'Authorization': "Bearer " + auth_token}
        url = apim_api_publish_url + id
        response = requests.post(url, headers=headers, verify=False)
        if response.status_code == 200:
            log.debug("Api publish success")
    except HTTPError as http_err:
        log.error(f'HTTP error occurred: {http_err}')
    except Exception as err:
        log.error(f'Other error occurred: {err}')
