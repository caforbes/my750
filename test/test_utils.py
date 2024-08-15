import pytest
import html
import markdown as md

import utils


def test_date_before_today_error():
    with pytest.raises(ValueError):
        utils.date_before_today(-2)


@pytest.mark.parametrize(
    "userinput,expected",
    [
        ("regular", "<p>regular</p>"),
        ("<script>", "<p>&lt;script&gt;</p>"),
        (
            '<a href="bad">link</a>',
            "<p>&lt;a href=&#34;bad&#34;&gt;link&lt;/a&gt;</p>",
        ),
        ("# Title", "<h1>Title</h1>"),
        ("# <script>", "<h1>&lt;script&gt;</h1>"),
        ("* List thing", "<ul>\n<li>List thing</li>\n</ul>"),
        # ("> Quoted", "<blockquote>Quoted</blockquote>"), # TODO: allow blockquotes
    ],
)
def test_usertext_to_md(userinput, expected):
    result = utils.usertext_to_md(userinput)
    assert result == expected
