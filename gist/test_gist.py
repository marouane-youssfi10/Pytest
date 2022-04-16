import pytest


def test_our_first_test() -> None:
    assert 1 == 1


@pytest.mark.skip
def test_should_be_skipped() -> None:
    assert 1 == 2


@pytest.mark.skipif(4 > 1, reason="Skipped because 4 > 1")
def test_should_be_skipped() -> None:
    assert 1 == 2


@pytest.mark.xfail
def test_dont_care_if_fails() -> None:
    assert 1 == 2


@pytest.mark.slow
def test_with_custom_mark1() -> None:
    pass


@pytest.mark.slow
def test_with_custom_mark2() -> None:
    pass


class Company:
    def __init__(self, name: str, stock_symbol: str):
        self.name = name
        self.stock_symbol = stock_symbol

    def __str__(self):
        return f"{self.name}:{self.stock_symbol}"


@pytest.fixture
def company() -> Company:
    return Company(name="Fiver", stock_symbol="FVRR")


def test_with_fixture(company: Company) -> None:
    print(f"Printing {company} from fixture")


@pytest.mark.parametrize(
    "company_name",
    ["TikTok", "Instagram", "Twitch"],
    ids=["TikTok TEST", "Instagram TEST", "Twitch TEST"]
)
def test_parametrized(company_name: str) -> None:
    print(f"\nTest with {company_name}")

def raise_covid19_exception() -> None:
    raise ValueError("CoronaVirus Exception")

def test_raise_covid19_exception_should_pass() -> None:
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert "CoronaVirus Exception" == str(e.value)