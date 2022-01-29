from copy import deepcopy
from unittest.mock import patch, MagicMock

import pytest
import requests

from requests_default import DefaultSession

default_url = 'https://jsonplaceholder.typicode.com'
defaults: dict = {
    'params': {'p1': 1},
    'headers': {
        'User-Agent': 'python-requests/2.27.1',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'h': 'h'},
    'timeout': 5,
    'allow_redirects': True,
}
ds = DefaultSession(url=default_url, **defaults)


@patch.object(requests.Session, 'request')
def test_default_session_not_updated(mocked_request: MagicMock):
    res = mocked_request.return_value
    res.status_code = 200
    res.text = 'aaa'

    res = ds.get(url='/todos', )
    print(res.text)
    res.raise_for_status()

    requests.Session.request.assert_called_with(method='GET', url=f'{default_url}/todos', **defaults)


@patch.object(requests.Session, 'request')
def test_default_session_updated(mocked_request: MagicMock):
    res = mocked_request.return_value
    res.status_code = 200
    res.text = 'aaa'

    updated_defaults, expected_defaults = deepcopy(defaults), deepcopy(defaults)
    updated_defaults['params']['p2'] = 2
    updated_defaults['allow_redirects'] = False

    expected_defaults['params'].update({'p2': 2})
    expected_defaults['allow_redirects'] = False

    res = ds.get(url='/todos', **updated_defaults)
    print(res.text)
    res.raise_for_status()

    requests.Session.request.assert_called_with(method='GET', url=f'{default_url}/todos', **updated_defaults)
