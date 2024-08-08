from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

from app.constants import MAX_ENTRY_LEN


class EntryForm(FlaskForm):
    content = TextAreaField(
        "What would you like to say today?",
        validators=[DataRequired(), Length(max=MAX_ENTRY_LEN)],
        render_kw={"autofocus": True},
    )
    submit = SubmitField("Save")
