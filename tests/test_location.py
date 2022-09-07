import pytest
from warehouseroute.location import AreaLocation, RackLocation, DeepStackingLocation


def test_location_not_equal(arealocation, racklocation, deepstackinglocation):
    assert arealocation != racklocation
    assert arealocation != deepstackinglocation
    assert racklocation != deepstackinglocation


def test_location_equal(arealocation, racklocation, deepstackinglocation):
    assert arealocation == arealocation
    assert racklocation == racklocation
    assert deepstackinglocation == deepstackinglocation


@pytest.fixture
def arealocation():
    return AreaLocation("BUFF3")


@pytest.fixture
def racklocation():
    return RackLocation("BUFF3", "15", "3", "14")


@pytest.fixture
def deepstackinglocation():
    return DeepStackingLocation("BUFF3", "3", "14")
