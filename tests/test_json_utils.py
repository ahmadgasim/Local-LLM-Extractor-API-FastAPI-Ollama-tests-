import pytest
from week1.experiments.json_utils import extract_first_json

def test_extract_first_json_removes_fences():
    raw = """```json
    {"a": 1, "b": [1,2,3]}
    ```"""
    data = extract_first_json(raw)
    assert data["a"] == 1
    assert data["b"] == [1, 2, 3]

def test_extract_first_json_handles_trailing_commas():
    raw = """```json
    {"a": 1, "b": [1,2,3,],}
    ```"""
    data = extract_first_json(raw)
    assert data["a"] == 1
    assert data["b"] == [1, 2, 3]

def test_extract_first_json_raises_on_no_json():
    with pytest.raises(Exception):
        extract_first_json("hello there")