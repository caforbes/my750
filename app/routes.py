from flask import flash, redirect, render_template, request, url_for

from app import app
from app.forms import EntryForm


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    # TODO: use real data
    written_today = False
    last_ten_entries = ["sample", "entry contains things"]
    placeholder_stats = {
        "total_entries": len(last_ten_entries),
        "total_words": len([wd for entry in last_ten_entries for wd in entry.split()]),
    }

    return render_template(
        "home.html",
        written_today=written_today,
        past_entries=last_ten_entries,
        stats=placeholder_stats,
    )


@app.route("/today")
def today():
    # TODO: get today's entry
    entry = None

    if not entry:
        return redirect(url_for("new"))

    # TODO: if you found something, display it - with link to today/edit page
    return "Page to read today's words"


@app.route("/new", methods=["GET", "POST"])
@app.route("/today/new", methods=["GET", "POST"])
def new():
    # If there is already an entry for today, go to the view area instead
    # TODO: get today's entry
    entry = None
    if entry:
        flash(
            "Can't add a new daily entry when one already exists!",
            category="error",
        )
        return redirect(url_for("today"))

    form = EntryForm()
    if form.validate_on_submit():
        flash("Your words have been sent to the ether!")  # FIX: store in db
        return redirect(url_for("home"))
    elif request.method == "POST":
        flash("You must write some words before saving!", category="error")
    return render_template("today_new.html", title="A new day", form=form)
