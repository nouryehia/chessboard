from datetime import date
from project.src.utils.time import TimeUtil


def test_current_time():
    assert TimeUtil.get_current_year() == str(date.today().year)
