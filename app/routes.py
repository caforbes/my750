from flask import flash, redirect, render_template, request, url_for

from app import app
from app.forms import EntryForm
from app.models import Entry
from utils import usertext_to_md


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

    return render_template("entry_new.html", title="A new day", form=form)


@app.route("/today/edit", methods=["GET", "POST"])
def edit_today():
    """
    Edit today's entry.
    """
    # FIX: what if it goes past midnight
    entry = Entry.get_today()
    if not entry:
        flash(
            "There is no entry for today, but you can create a new one!",
        )
        return redirect(url_for("new"))

    form = EntryForm(formdata=request.form, obj=entry)
    if form.validate_on_submit():
        res = Entry.update(id=entry.id, content=form.data["content"])
        if res == 1:
            flash("Thanks for the latest words!")
            return redirect(url_for("today"))
        else:
            flash("Something went wrong!", category="error")
    elif request.method == "POST":
        flash("Couldn't save that. There were no words to save!", category="error")
        form.content.data = entry.content  # go back to original content

    return render_template(
        "entry_edit.html", title="Edit today's entry", form=form, entry=entry
    )


@app.route("/today")
def today():
    entry = Entry.get_today()

    if not entry:
        flash("You have not written any words yet today! Start here.")
        return redirect(url_for("new"))

    html_content = usertext_to_md(entry.content)

    return render_template(
        "entry_view.html",
        title=f"Words for today",
        html_content=html_content,
        words=entry.wdcount,
        is_today=True,
    )
