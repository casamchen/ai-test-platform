import requests

class APIRequester:
    def __init__(self, base_url, session=None):
        self.base_url = base_url
        self.session = session or requests.Session()
        # self.session.hooks['response'] = self.capture_request_and_response

    def capture_request(self, response, *args, **kwargs):

        request_info = {
            'method': response.request.method,
            'url': response.request.url,
            'headers': dict(response.request.headers),
            'body': response.request.body
        }
        return request_info

    def request(self, method, endpoint, payload=None):
        url = self.base_url + endpoint
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=payload)
            elif method.upper() == 'POST':
                response = self.session.post(url, data=payload)
            else:
                raise ValueError("不支持的请求方法")
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            raise e
        
        return response

    def get(self, endpoint, payload=None):
        return self.request('GET', endpoint, payload=payload)

    def post(self, endpoint, payload=None):
        return self.request('POST', endpoint, payload=payload)
