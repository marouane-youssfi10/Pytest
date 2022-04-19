import pytest
import requests
import json

testing_env_companies_url = "http://127.0.0.1:8000/companies/"



def test_zero_companies_django_agnostic() -> None:
    response = requests.get(url=testing_env_companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []