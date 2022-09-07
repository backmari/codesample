import pytest
from unittest import mock
from warehouseroute.parser import GraphParser


def test_parse_graph_json_file(graph_json):

    # Setup
    parser = GraphParser()

    # Mock reading the graph from a file
    mock_open = mock.mock_open(read_data=graph_json)
    with mock.patch('builtins.open', mock_open):
      graph = parser.parse_json('filename')

    # Test that the created graph has the correct number of nodes
    assert graph.len() == 2


@pytest.fixture
def graph_json() -> str:
  return '''[
  {
    "id": 0,
    "position": {
      "x": 68.4948,
      "y": 88.2296
    },
    "location": {
      "locationType": 2,
      "mha": "PICK1",
      "rack": 18,
      "horcoor": 12,
      "vercoor": 41
    },
    "adjacencies": [
      {
        "nodeTo": 2,
        "cost": 5.2
      }
    ]
  },
  {
    "id": 1,
    "position": {
      "x": 68.4948,
      "y": 88.2296
    },
    "location": {
      "locationType": 2,
      "mha": "PICK2",
      "rack": 18,
      "horcoor": 12,
      "vercoor": 41
    },
    "adjacencies": [
      {
        "nodeTo": 2,
        "cost": 5.2
      }
    ]
  }
  ]'''
