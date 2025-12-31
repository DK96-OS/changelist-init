import pytest

from changelist_init.git.git_tracking_status import GitTrackingStatus, from_str



def test_from_str_empty_raises_value_error():
    with pytest.raises(ValueError):
        from_str('')


def test_from_str_single_char_raises_value_error():
    with pytest.raises(ValueError):
        from_str('A')


def test_from_str_untracked():
    assert GitTrackingStatus.UNTRACKED == from_str('??')


@pytest.mark.parametrize(
    'status_code', [
        ' A',
        ' M',
        ' D',
        ' R',
    ]
)
def test_from_str_unstaged(status_code):
    assert GitTrackingStatus.UNSTAGED == from_str(status_code)


@pytest.mark.parametrize(
    'status_code', [
        'A ',
        'M ',
        'D ',
        'R ',
    ]
)
def test_from_str_staged(status_code):
    assert GitTrackingStatus.STAGED == from_str(status_code)


@pytest.mark.parametrize(
    'status_code', [
        'MA',
        'MM',
        'MD',
        'MR',
    ]
)
def test_from_str_partial_stage(status_code):
    assert GitTrackingStatus.PARTIAL_STAGE == from_str(status_code)
