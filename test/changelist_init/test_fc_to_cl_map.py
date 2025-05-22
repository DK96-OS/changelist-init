""" Testing FC To CL Map Module Methods.
"""
from changelist_data import file_change

from changelist_init.fc_to_cl_map import create_fc_to_cl_dict, offer_fc_to_cl_dict, merge_fc_generator
from test.changelist_init.conftest import get_sample_fc_path


def test_create_fc_to_cl_dict_empty_list_returns_empty_dict():
    result = create_fc_to_cl_dict([])
    assert len(result.keys()) == 0


def test_offer_fc_into_cl_dict_scenario_0():
    assert not offer_fc_to_cl_dict({}, file_change.create_fc(get_sample_fc_path(0)))


def test_offer_fc_into_cl_dict_scenario_0_empty_fc_raises_exit():
    try:
        assert not offer_fc_to_cl_dict({}, file_change.FileChange())
        raised_exit = False
    except SystemExit:
        raised_exit = True
    assert raised_exit


def test_merge_fc_generator_scenario_0():
    result = list(merge_fc_generator([], []))
    assert len(result) == 0