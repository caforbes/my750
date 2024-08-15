import pytest
from app.models import Entry
from test.conftest import load_entries
import utils


class TestHomepage:
    path = "/"

    def test_homepage_no_entry(self, client, db_conn):
        count = Entry.count()

        # Expect to visit the homepage and see general layout
        response = client.get(self.path)

        assert response.status_code == 200
        assert b"My750" in response.data  # title
        assert b"<nav class=" in response.data  # navigation
        # Expect button to create new entry
        assert b"Start writing" in response.data
        assert b"/new" in response.data
        assert b'"/today"' not in response.data
        # Expect statistics of past entries
        assert f"{count} entries" in response.text
        # Expect list of recent entries
        assert b"Recent entries" in response.data
        assert b'<nav id="past-entries"' in response.data
        assert b'<a class="panel-block"' in response.data

    def test_homepage_with_entry(self, client, db_conn):
        Entry.create("test entry for today")
        count = Entry.count()

        # Expect to visit the homepage and see general layout
        response = client.get(self.path)

        assert response.status_code == 200
        # Expect button to continue today's entry
        assert b"Continue" in response.data
        assert b'"/today"' in response.data
        assert b"/new" not in response.data
        # Expect statistics of past entries
        assert f"{count} entries" in response.text
        # Expect list of recent entries
        assert b"Recent entries" in response.data
        assert b'<nav id="past-entries"' in response.data
        assert b'<a class="panel-block"' in response.data

    def test_homepage_no_previous_entries(self, client, db_conn_empty):
        for entry in Entry.list():
            Entry.delete(id=entry.id)
        assert Entry.count() == 0

        # Expect to visit the homepage
        response = client.get(self.path)
        assert response.status_code == 200
        # Expect statistics of past entries
        assert b"0 entries" in response.data
        # Expect list of recent entries is empty
        assert b'<nav id="past-entries"' not in response.data
        assert b"no past entries" in response.data


class TestCreateNew:
    path = "/new"

    def test_new_entry_get(self, client, db_conn):
        response = client.get("/new")

        # Expect form to create new entry, no errors
        assert response.status_code == 200
        assert b'method="post"' in response.data
        assert b'<div id="flash"' not in response.data

    def test_new_entry_get_already_exists(self, client, db_conn):
        Entry.create("test entry for today")

        # Expect redirection to view the existing entry, no error
        response = client.get("/new", follow_redirects=True)

        assert len(response.history) == 1
        assert response.request.path == "/today"

    def test_new_entry_post(self, client, db_conn):
        orig_count = Entry.count()

        text = "Writing text for an entry"
        formdata = {"content": text}
        response = client.post("/new", data=formdata, follow_redirects=True)

        # Expect new entry in database
        new_count = Entry.count()
        assert new_count == orig_count + 1
        # Expect redirection to view page for the entry you just created
        assert len(response.history) == 1
        assert response.status_code == 200
        assert b"Another journal entry" in response.data
        assert text in response.text

    @pytest.mark.parametrize(
        "bad_content",
        [
            "",  # blank entry
            " " * 10,  # whitespace only
        ],
    )
    def test_new_entry_post_bad(self, client, db_conn, bad_content):
        orig_count = Entry.count()

        formdata = {"content": bad_content}
        response = client.post("/new", data=formdata)

        # Expect bad form data, rerendering of the same form
        assert response.status_code == 200
        assert b"is-danger" in response.data
        # Expect no new db entry
        assert orig_count == Entry.count()

    def test_new_entry_post_already_exists(self, client, db_conn):
        Entry.create("test entry for today")
        orig_count = Entry.count()

        formdata = {"content": "Duplicate daily entry"}
        response = client.post("/new", data=formdata, follow_redirects=True)

        # Expect redirection to view page for that entry, with error
        assert len(response.history) == 1
        assert response.status_code == 200
        assert b"is-danger" in response.data
        # Expect no new db entry
        assert orig_count == Entry.count()


class TestViewToday:
    path = "/today"

    def test_get_today(self, client, db_conn):
        entry_text = 'test entry for today <a href="forbidden">link</a>'
        Entry.create(entry_text)

        response = client.get(self.path)

        # Expect general layout and view entry content
        assert response.status_code == 200
        assert b"My750" in response.data  # title
        assert b"<nav class=" in response.data  # navigation
        # Expect displayed user content to be html safe
        assert entry_text not in response.text
        assert utils.usertext_to_md(entry_text) in response.text
        # Expect links to editing and other page elements
        assert b">Edit this entry" in response.data  # FIX
        assert b">Go Home" in response.data

    def test_get_today_none(self, client, db_conn):
        response = client.get(self.path, follow_redirects=True)

        # Expect redirection to create new entry form, with message
        assert len(response.history) == 1
        assert response.status_code == 200
        assert b"flash" in response.data
        assert b"not written any words yet" in response.data
