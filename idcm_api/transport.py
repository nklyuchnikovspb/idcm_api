from urllib.parse import urljoin
import hmac
import hashlib
import json
import requests
import base64


class IDCMTransport:
    BASE_URL = 'https://api.IDCM.io:8323/api/v1/'

    def __init__(self, key, secret):
        self.KEY = key
        self.SECRET = secret

    def _get_url(self, path):
        return urljoin(self.BASE_URL, path)

    def _get_signature(self, data: dict):
        signature = hmac.new(
            self.SECRET.encode(),
            json.dumps(data).encode(),
            hashlib.sha384
        ).digest()
        return base64.b64encode(signature).decode()

    def _get_headers(self, data: dict):
        headers = {
            'X-IDCM-APIKEY': self.KEY,
            'X-IDCM-SIGNATURE': self._get_signature(data),
            'X-IDCM-INPUT': json.dumps(data)
        }
        return headers

    def _request(self, path: str, data: dict, request_type: str = 'POST'):
        headers = self._get_headers(data)
        url = self._get_url(path)

        result = requests.request(method=request_type, json=data, headers=headers, url=url).json()
        return result
