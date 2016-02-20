from wtforms import (
    Form,
    TextField,
    TextAreaField,
    validators,
    BooleanField,  #added to  support edit, may not be necessary
    StringField,  #added to  support edit, may not be necessary
    HiddenField,  #Support capturing current row id value
)
#add an import:
from wtforms import PasswordField


strip_filter = lambda x: x.strip() if x else None


class EntryCreateForm(Form):
    title = TextField(
        'Entry title',
        [validators.Length(min=1, max=255)],
        filters=[strip_filter]
    )
    body = TextAreaField(
        'Entry body',
        [validators.Length(min=1)],
        filters=[strip_filter]
    )


class EntryEditForm(Form):
    id = HiddenField()  #capture and store row_id information

# and a new form class from class notes
class LoginForm(Form):
    username = TextField(
        'Username', [validators.Length(min=1, max=255)]
    )
    password = PasswordField(
        'Password', [validators.Length(min=1, max=255)]
    )