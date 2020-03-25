from requests.exceptions import HTTPError
from requests import get, delete


def request(method, target, params=None, headers=None):

    try:

        response = method(target, headers=headers, params=params)
        response.raise_for_status()
        return response

    except HTTPError as error:

        status_code, text = error.response.status_code, error.response.text
        print(f"{method.__name__.upper()} to {target} failed:", status_code, text)
