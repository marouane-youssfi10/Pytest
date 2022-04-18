import json
from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse

from companies.models import Company

companies_url = reverse("companies-list")

@pytest.mark.django_db
class BasicCompanyAPITestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    def tesrDown(self) -> None:
        pass

@pytest.mark.django_db
def test_zero_companies_should_return_empty_list(client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert (json.loads(response.content)) == []

@pytest.mark.django_db
def test_one_company_exists_should_succeed(client) -> None:
    test_company = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    response_content = json.loads(response.content)[0]
    assert response.status_code == 200
    assert response_content.get("name") == test_company.name
    assert response_content.get("application_link") == ""
    assert response_content.get("notes") == ""
    test_company.delete()

# -------------------------- test post companies --------------------------------
class TestPostCompanies(BasicCompanyAPITestCase):
    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {"name": ["This field is required."]})

    def test_create_existing_company_should_fail(self) -> None:
        Company.objects.create(name="Tuesday")
        response = self.client.post(path=self.companies_url, data={"name": "Tuesday"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"name": ["company with this name already exists."]}
        )

    def test_create_company_with_only_name_all_fields_should_be_default(self) -> None:
        response = self.client.post(path=self.companies_url, data={"name": "test name company"})
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("name"), "test name company")
        self.assertEqual(response_content.get("status"), "Hiring")
        self.assertEqual(response_content.get("application_link"), "")
        self.assertEqual(response_content.get("notes"), "")

    def test_create_company_with_layoffs_status_should_succeed(self) -> None:
        response = self.client.post(path=self.companies_url, data={"name": "test name company", "status": "Layoffs"})
        self.assertEqual(response.status_code, 201)
        response_content = json.loads(response.content)
        self.assertEqual(response_content.get("status"), "Layoffs")

    def test_create_company_with_wrong_status_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url, data={"name": "test name company", "status": "WrongStatus"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("WrongStatus", str(response.content))
        self.assertIn("is not a valid choice", str(response.content))

    @pytest.mark.xfail
    def test_should_be_ok_if_fails(self) -> None:
        self.assertEqual(1, 2)

    @pytest.mark.skip
    def test_should_be_skipped(self) -> None:
        self.assertEqual(1, 2)

def test_should_be_skipped() -> None:
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
