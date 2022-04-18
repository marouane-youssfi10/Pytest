from datetime import datetime

import pytest


@pytest.fixture
def time_tracker():
    tick = datetime.now()
    yield
    track = datetime.now()
    diff = track - tick
    print(f"\n runtime {diff.total_seconds()}")