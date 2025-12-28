""" Testing FC To CL Map Module Methods.
"""
import pytest
from changelist_data import file_change, Changelist
from changelist_data.file_change import create_fc

from changelist_init.fc_to_cl_map import create_fc_to_cl_dict, offer_fc_to_cl_dict, merge_fc_generator
from test.changelist_init.conftest import get_sample_fc_path, cl_sample_list, _SAMPLE_FC_0, root_cl_create_file, \
    _SAMPLE_FC_1, get_cl


def test_create_fc_to_cl_dict_empty_list_returns_empty_dict():
    result = create_fc_to_cl_dict([])
    assert len(result.keys()) == 0


def test_create_fc_to_cl_dict_():
    result = create_fc_to_cl_dict(cl_sample_list([
        'c', '', '',
    ]))
    assert len(result.keys()) == 1
    cl: Changelist = result[get_sample_fc_path(0)]
    assert len(cl.changes) == 1


def test_create_fc_to_cl_dict_create_sample_fc_3():
    result = create_fc_to_cl_dict(cl_sample_list([
        'c',
        ' c',
        '  c',
    ]))
    assert len(result.keys()) == 3
    #
    cl0: Changelist = result[get_sample_fc_path(0)]
    assert len(cl0.changes) == 1
    #
    cl1: Changelist = result[get_sample_fc_path(1)]
    assert len(cl1.changes) == 1
    #
    cl2: Changelist = result[get_sample_fc_path(2)]
    assert len(cl2.changes) == 1


@pytest.mark.parametrize(
    "test_cl_sample_list, expected_count", [
        (cl_sample_list(['c', '', '']), 1),
        (cl_sample_list(['u', ' d', '']), 2),
        (cl_sample_list(['cud', '', '']), 3),
        (cl_sample_list(['c', 'c', 'c']), 1),
        (cl_sample_list(['cc', 'cc', 'cc']), 2),
    ]
)
def test_create_fc_to_cl_dict_cl_sample_lists(
    test_cl_sample_list, expected_count
):
    result = create_fc_to_cl_dict(test_cl_sample_list)
    assert len(result.keys()) == expected_count


def test_offer_fc_to_cl_dict_scenario_0():
    assert not offer_fc_to_cl_dict({}, file_change.create_fc(get_sample_fc_path(0)))


def test_offer_fc_to_cl_dict_empty_fc_raises_exit():
    with pytest.raises(SystemExit):
        offer_fc_to_cl_dict({}, file_change.FileChange())


def test_offer_fc_to_cl_dict_create_sample_fc_0():
    test_map: dict[str, Changelist] = create_fc_to_cl_dict(
        cl_sample_list(['c', '', ''])
    )
    assert offer_fc_to_cl_dict(test_map, create_fc(_SAMPLE_FC_0))
    assert _SAMPLE_FC_0 in test_map
    default_cl: Changelist = test_map[_SAMPLE_FC_0]
    assert default_cl.is_default


def test_offer_fc_to_cl_dict_create_sample_fc_3():
    test_changelists = cl_sample_list([
        'c',
        ' c',
        '  c',
    ])
    test_map = create_fc_to_cl_dict(test_changelists)
    # The Changelists should be cleared before offer method.
    for cl in test_changelists:
        cl.changes.clear()
    # The map contains empty changelists
    for i in range(3):
        cl: Changelist = test_map[get_sample_fc_path(i)]
        assert len(cl.changes) == 0
    # Offer FC adds to Changelists
    for i in range(3):
        assert offer_fc_to_cl_dict(test_map, create_fc(get_sample_fc_path(i)))
        assert get_sample_fc_path(i) in test_map
        cl: Changelist = test_map[get_sample_fc_path(i)]
        assert len(cl.changes) == 1


def test_merge_fc_generator_scenario_0():
    result = list(merge_fc_generator([], []))
    assert len(result) == 0


def test_merge_fc_generator_root_cl_create():
    initial_cl = [root_cl_create_file()]
    result = list(merge_fc_generator(initial_cl, [file_change.create_fc(_SAMPLE_FC_0)]))
    assert len(result) == 0


def test_merge_fc_generator_root_cl_update():
    initial_cl = [root_cl_create_file()]
    result = list(merge_fc_generator(initial_cl, [file_change.update_fc(_SAMPLE_FC_0)]))
    assert len(result) == 0


def test_merge_fc_generator_root_cl_delete():
    initial_cl = [root_cl_create_file()]
    result = list(merge_fc_generator(initial_cl, [file_change.delete_fc(_SAMPLE_FC_0)]))
    assert len(result) == 0


def test_merge_fc_generator_root_cl_2():
    initial_cl = [root_cl_create_file()]
    result = list(merge_fc_generator(initial_cl, [file_change.create_fc(_SAMPLE_FC_0), file_change.create_fc(_SAMPLE_FC_1)]))
    assert len(result) == 1


def test_merge_fc_generator_default_cl():
    initial_cl = [get_cl(0, [])]
    updated_fc = [
        file_change.create_fc(_SAMPLE_FC_0),
        file_change.create_fc(_SAMPLE_FC_1),
    ]
    result = list(merge_fc_generator(initial_cl, updated_fc))
    assert len(result) == 2
    assert len(initial_cl[0].changes) == 0


def test_merge_fc_generator_2_changelists_2_file_changes_no_differences_yields_none():
    initial_cl = [
        get_cl(1, [file_change.create_fc(_SAMPLE_FC_0)]),
        get_cl(2, [file_change.create_fc(_SAMPLE_FC_1)]),
    ]
    updated_fc = [
        file_change.create_fc(_SAMPLE_FC_0),
        file_change.create_fc(_SAMPLE_FC_1),
    ]
    result = list(merge_fc_generator(initial_cl, updated_fc))
    assert len(result) == 0
    assert len(initial_cl[0].changes) == 1
    assert len(initial_cl[1].changes) == 1


def test_merge_fc_generator_2_changelists_add_file_change():
    initial_cl = [
        get_cl(1, [file_change.create_fc(_SAMPLE_FC_0)]),
        get_cl(2, []),
    ]
    updated_fc = [
        file_change.create_fc(_SAMPLE_FC_0),
        file_change.create_fc(_SAMPLE_FC_1),
    ]
    result = list(merge_fc_generator(initial_cl, updated_fc))
    assert len(result) == 1
    assert len(initial_cl[0].changes) == 1
    assert len(initial_cl[1].changes) == 0
