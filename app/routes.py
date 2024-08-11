from flask import flash, redirect, render_template, request, url_for

from app import app
from app.forms import EntryForm
from app.models import Entry


@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    """
    Homepage - view whether there is an entry today, view archive, etc.
    """
    today_entry = Entry.get_today()
    last_ten_entries = Entry.list(10)

    return render_template(
        "home.html",
        written_today=today_entry.wdcount if today_entry else 0,
        entry_count=Entry.count(),
        past_entries=last_ten_entries,
    )


@app.route("/new", methods=["GET", "POST"])
@app.route("/today/new", methods=["GET", "POST"])
def new():
    """
    Create a new entry for today.
    """
    # If there is already an entry for today, go to the view area instead
    entry = Entry.get_today()
    if entry:
        if request.method == "POST":
            flash(
                "Can't add a new daily entry when one already exists!",
                category="error",
            )
        return redirect(url_for("today"))

    form = EntryForm()
    if form.validate_on_submit():
        data = form.data
        Entry.create(content=data["content"])
        flash(f"Another journal entry is on the page!")
        return redirect(url_for("home"))

    elif request.method == "POST":
        flash("You must write some words before saving!", category="error")

    return render_template("today_new.html", title="A new day", form=form)


@app.route("/today")
def today():
    entry = Entry.get_today()

    if not entry:
        return redirect(url_for("new"))

    # TODO: if you found something, display it - with link to today/edit page
    return "Page to read today's words"
