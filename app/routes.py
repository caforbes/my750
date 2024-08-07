from flask import render_template
from app import app


@app.route("/")
@app.route("/index")
def index():
    errors = []
    written_today = False
    last_ten_entries = ["sample", "entry"]
    placeholder_stats = {
        "total_entries": len(last_ten_entries),
        "total_words": len([wd for entry in last_ten_entries for wd in entry]),
    }

    return render_template(
        "home.html",
        written_today=written_today,
        past_entries=last_ten_entries,
        stats=placeholder_stats,
        errors=errors,
    )
