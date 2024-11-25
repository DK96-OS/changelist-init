""" Testing Provider methods.
"""
from test.changelist_init.conftest import create_sample_list_input, cl_sample_list, get_default_cl, fc_sample_list, \
    get_root_cl, get_test_cl, get_fc_status


def test_cl_sample_list_empty():
    result = cl_sample_list(['', '', ''])
    assert result == []


def test_cl_sample_list_default_create_single():
    result = cl_sample_list(['c', '', ''])
    assert result == [get_default_cl(fc_sample_list('c'))]


def test_cl_sample_list_default_create_double():
    result = cl_sample_list(['cc', '', ''])
    assert result == [get_default_cl(fc_sample_list('cc'))]


def test_cl_sample_list_root_create_single():
    result = cl_sample_list(['', 'c', ''])
    assert result == [get_root_cl(fc_sample_list('c'))]


def test_cl_sample_list_root_create_double():
    result = cl_sample_list(['', 'cc', ''])
    assert result == [get_root_cl(fc_sample_list('cc'))]


def test_cl_sample_list_root_update_single():
    result = cl_sample_list(['', 'u', ''])
    assert result == [get_root_cl(fc_sample_list('u'))]


def test_cl_sample_list_test_create_single():
    result = cl_sample_list(['', '', 'c'])
    assert result == [get_test_cl(fc_sample_list('c'))]


def test_cl_sample_list_test_create_double():
    result = cl_sample_list(['', '', 'cc'])
    assert result == [get_test_cl(fc_sample_list('cc'))]


def test_cl_sample_list_test_update_single():
    result = cl_sample_list(['', '', 'u'])
    assert result == [get_test_cl(fc_sample_list('u'))]


def test_create_sample_list_input_negative_one():
    result = create_sample_list_input(-1, 'cu')
    assert result == ['', '', '']


def test_create_sample_list_input_zero():
    result = create_sample_list_input(0, 'cu')
    assert result == ['cu', '', '']


def test_create_sample_list_input_one():
    result = create_sample_list_input(1, 'cu')
    assert result == ['', 'cu', '']


def test_create_sample_list_input_two():
    result = create_sample_list_input(2, 'cu')
    assert result == ['', '', 'cu']


def test_create_sample_list_input_3():
    result = create_sample_list_input(3, 'cu')
    assert result == ['cu', 'cu', 'cu']


def test_create_sample_list_input_lambda():
    result = create_sample_list_input(3,  lambda x: x * ' ' + get_fc_status(1))
    assert result == ['u', ' u', '  u']

