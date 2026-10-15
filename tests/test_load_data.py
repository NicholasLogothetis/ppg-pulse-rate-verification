from src.load_data import clean_name


def test_clean_name_strips_trailing_comma():
    assert clean_name("PLETH,") == "PLETH"


def test_clean_name_strips_whitespace_and_comma():
    assert clean_name(" HR, ") == "HR"


def test_clean_name_leaves_plain_name_unchanged():
    assert clean_name("II") == "II"
