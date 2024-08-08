from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


MAX_LEN = 500_000


class EntryForm(FlaskForm):
    content = TextAreaField(
        "What would you like to say today?",
        validators=[DataRequired(), Length(max=MAX_LEN)],
        render_kw={"autofocus": True},
    )
    submit = SubmitField("Save")
