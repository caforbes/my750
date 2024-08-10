def test_homepage_no_entry(client, db_conn):
    result = db_conn.execute("SELECT count(*) FROM entries;")

    assert result.fetchone()[0] == 3
