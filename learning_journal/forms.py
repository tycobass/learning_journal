from wtforms import (
    Form,
    TextField,
    TextAreaField,
    validators,
    BooleanField,  #added to  support edit, may not be necessary
    StringField,  #added to  support edit, may not be necessary
)

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
    title = TextField(
        'Entry title available to edit',
        [validators.Length(min=1, max=255)],
        filters=[strip_filter]
    )
    body = TextAreaField(
        'Entry body available to edit',
        [validators.Length(min=1)],
        filters=[strip_filter]
    )

