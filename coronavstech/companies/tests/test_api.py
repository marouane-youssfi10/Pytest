import json
from typing import List

import pytest

from django.urls import reverse

from companies.models import Company

companies_url = reverse("companies-list")
pytestmark = pytest.mark.django_db


def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert (json.loads(response.content)) == []


@pytest.fixture
def amazon() -> Company:
    return Company.objects.create(name="amazon")


def test_one_company_exists_should_succeed(client, amazon) -> None:
    # test_company = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == amazon.name
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


# -------------------------- test post companies --------------------------------
def test_create_company_without_arguments_should_fail(client) -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_create_existing_company_should_fail(client) -> None:
    Company.objects.create(name="Tuesday")
    response = client.post(path=companies_url, data={"name": "Tuesday"})
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "name": ["company with this name already exists."]
    }


def test_create_company_with_only_name_all_fields_should_be_default(client) -> None:
    response = client.post(path=companies_url, data={"name": "test name company"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "test name company"
    assert response_content.get("status") == "Hiring"
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""


def test_create_company_with_layoffs_status_should_succeed(client) -> None:
    response = client.post(
        path=companies_url, data={"name": "test name company", "status": "Layoffs"}
    )
    assert response.status_code, 201
    response_content = json.loads(response.content)
    assert response_content.get("status") == "Layoffs"


def test_create_company_with_wrong_status_should_fail(client) -> None:
    response = client.post(
        path=companies_url, data={"name": "test name company", "status": "WrongStatus"}
    )
    assert response.status_code == 400
    assert "WrongStatus" in str(response.content)
    assert "is not a valid choice" in str(response.content)


def test_should_be_ok_if_fails(client) -> None:
    assert 1 == 1


@pytest.mark.skip
def test_should_be_skipped(client) -> None:
    assert 1 == 1


def raise_covid19_exception() -> None:
    raise ValueError("CoronaVirus Exception")


def test_raise_covid19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)


import logging

logger = logging.getLogger("CORONA_LOGS")


def function_that_logs_something() -> None:
    try:
        raise ValueError("CoronaVirus Exception")
    except ValueError as e:
        logger.warning(f"I am logging {str(e)}")


def test_logged_warning_level(caplog) -> None:
    function_that_logs_something()
    assert "I am logging CoronaVirus Exception" in caplog.text


def test_logged_info_level(caplog) -> None:
    with caplog.at_level(logging.INFO):
        logger.info("I am logging info level")
        assert "I am logging info level" in caplog.text


# ----------------------- fixtures ------------------------


@pytest.fixture()
def companies(request, company) -> List[Company]:
    companies = []
    names = request.param
    for name in names:
        companies.append(company(name=name))

    return companies

@pytest.fixture()
def company(**kwargs):
    def _company_factory(**kwargs) -> Company:
        company_name = kwargs.pop("name", "Test Company INC")
        return Company.objects.create(name=company_name, **kwargs)
    return _company_factory

@pytest.mark.parametrize(
        "companies",
        [
            ["Tiktok", "Twitch", "Test Company INC"],
            ["Facebook", "Instagram"]
        ],
        ids=["3 T companies", "Zuckerberg's companies"],
        indirect=True
    )
def test_multiple_companies_exists_should_succeed(client, companies) -> None:
    company_names = set(map(lambda x: x.name, companies))
    print(company_names)
    response_companies = client.get(companies_url).json()

    # Test len of company_names equal response_companies
    assert len(company_names) == len(response_companies)
    response_company_names = set(
        map(lambda company: company.get("name"), response_companies)
    )
    assert company_names == response_company_names