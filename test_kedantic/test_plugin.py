from inspect import Parameter
from ..kedantic.plugin import KedanticHook
from unittest.mock import MagicMock, Mock
from pydantic import BaseModel


class MockModel(BaseModel):
    test: str = "test"


def test_get_new_input():
    hook = KedanticHook()

    # Check non "params:" input key has no side effects
    inputs = {}
    input_key = "test_key"
    param = MagicMock(Parameter)
    hook._get_new_input(inputs, input_key, param)
    assert inputs == {}

    # Check that non Base Model parameter has no side effects
    input_key = "params:test"
    param.annotation = dict
    hook._get_new_input(inputs, input_key, param)
    assert inputs == {}

    # Check that input that isn't a dict has no side effect
    inputs = {"params:test": "test"}
    param.annotation = MockModel
    hook._get_new_input(inputs, input_key, param)
    assert inputs == {"params:test": "test"}

    # Check inputs get changed to model when proper condition
    inputs = {"params:test": {"test": "check"}}
    hook._get_new_input(inputs, input_key, param)
    assert inputs == {"params:test": MockModel(test="check")}
