from datetime import date, timedelta
import pytest

from app.models import Entry


def test_entry_create_future(mock_db):
    """Entry can't be created in the future."""
    with pytest.raises(ValueError):
        Entry.create("test", date.today() + timedelta(days=1))


def test_entry_create(db_conn):
    """Test basic entry functions: create."""
    # Expect creation on today by default
    count = Entry.count()
    result = Entry.create("test")
    assert result == 1
    assert Entry.count() == count + 1
    # Expect creation on specified day
    result = Entry.create("test", date(2024, 1, 1))
    assert result == 1
    # Expect no duplicate entry creation
    result = Entry.create("test", date(2024, 1, 1))
    assert result == 0


def test_entry_update(db_conn):
    """Test basic entry functions: update."""
    entries = Entry.list()

    # Expect update with given id
    test_id = entries[0].id
    new_text = "test update"
    result = Entry.update(id=test_id, content=new_text)
    assert result == 1
    # Expect db properties are updated
    updated_entry = Entry.get(id=test_id)
    assert updated_entry.content == new_text
    assert updated_entry.created != updated_entry.updated

    # Expect can't update nonexistent entry
    test_id = max([entry.id for entry in entries]) + 1
    result = Entry.update(id=test_id, content=new_text)
    assert result == 0


def test_entry_delete(db_conn):
    """Test basic entry functions: delete."""
    entries = Entry.list()

    # Expect update with given id
    test_id = entries[0].id
    result = Entry.delete(id=test_id)
    assert result == 1
    assert Entry.get(id=test_id) is None

    # Expect can't update nonexistent entry
    test_id = max([entry.id for entry in entries]) + 1
    result = Entry.delete(id=test_id)
    assert result == 0
