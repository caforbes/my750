from datetime import date, timedelta
import pytest

from app.models import Entry


def test_entry_create_future(mock_db):
    """Entry can't be created in the future."""
    # mocker.patch("app.models.dbconnect")
    with pytest.raises(ValueError):
        Entry.create("test", date.today() + timedelta(days=1))


def test_entry_create(mock_db):
    """Test basic entry functions: create."""
    result = Entry.create("test")
    assert result
    result = Entry.create("test", date(2024, 1, 1))
    assert result
