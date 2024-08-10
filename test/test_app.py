from app.models import Entry

# GET homepage


class TestHomepage:
    path = "/"

    def test_homepage_no_entry(self, client, db_conn):
        response = client.get(self.path)

        assert response.status_code == 200
        assert b"My750" in response.data  # title
        assert b"<nav class=" in response.data  # navigation
        # button to create new entry
        assert b"Start writing" in response.data
        assert b"/new" in response.data

    def test_homepage_with_entry(self, client, db_conn):
        Entry.create("test entry for today")

        response = client.get(self.path)

        assert response.status_code == 200
        # button to continue today's entry
        assert b"Continue" in response.data
        assert b"/new" not in response.data
        # TODO: show the edit or view today button


# TODO: GET: create entry


class TestCreateNew:
    path = "/new"

    def test_new_entry_get(self, client, db_conn):
        response = client.get("/new")

        assert response.status_code == 200
        assert b'method="post"' in response.data
        assert b'<div id="flash"' not in response.data

    def test_new_entry_get_already_exists(self, client, db_conn):
        Entry.create("test entry for today")

        response = client.get("/new", follow_redirects=True)

        assert len(response.history) == 1

        # assert response.request.path == url_for("today") # TODO
        assert b"read today's words" in response.data
        # assert b"is-danger" in response.data

    # TODO: POST: create entry

    def test_new_entry_post(self, client, db_conn):
        orig_count = Entry.count()

        formdata = {"content": "Writing text for an entry"}
        response = client.post("/new", data=formdata, follow_redirects=True)

        assert len(response.history) == 1
        assert response.status_code == 200
        assert b"Another journal entry" in response.data

        new_count = Entry.count()
        assert new_count == orig_count + 1

    def test_new_entry_post_blank(self, client, db_conn):
        orig_count = Entry.count()

        formdata = {"content": ""}
        response = client.post("/new", data=formdata)

        assert response.status_code == 200
        assert b"is-danger" in response.data
        assert orig_count == Entry.count()

    def test_new_entry_post_whitespace(self, client, db_conn):
        orig_count = Entry.count()

        formdata = {"content": "      "}
        response = client.post("/new", data=formdata)

        assert response.status_code == 200
        assert b"is-danger" in response.data
        assert orig_count == Entry.count()

    def test_new_entry_post_already_exists(self, client, db_conn):
        Entry.create("test entry for today")
        orig_count = Entry.count()

        formdata = {"content": "Duplicate daily entry"}
        response = client.post("/new", data=formdata, follow_redirects=True)

        assert len(response.history) == 1

        assert response.status_code == 200
        # FIX
        # assert b"already exists" in response.data
        # assert b"is-danger" in response.data
        assert orig_count == Entry.count()
