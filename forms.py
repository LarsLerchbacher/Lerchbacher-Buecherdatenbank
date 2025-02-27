#
# forms.py
# ----------
# Book database project
# (c) Lars Lerchbacher 2025
#


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, IntegerField, BooleanField, HiddenField, PasswordField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField("Name: ", validators=[DataRequired()])
    authors = SelectMultipleField("Author/en: ", choices=[], coerce=int, validate_choice=False)
    publisher = StringField("Verlag: ")
    isbn = StringField("ISBN-13 (Nur Ziffern): ")
    edition = IntegerField("Auflage Nr. :")
    year = IntegerField("Erscheinungsjahr: ", default=2000)
    types = StringField("Buchtyp/en (mit ; trennen): ")
    tags = StringField("Kategorie/n (mit ; trennen): ")
    room = SelectField("Zimmer: ", choices=["Lars Zimmer", "Linos Zimmer", "Lilos Zimmer", "Schlafzimmer", "Bibliothek", "Wohnzimmer", "Arbeitszimmer", "Sonst irgendwo"])
    shelf = StringField("Regal und/oder Fach: ")
    lend = BooleanField("Ausgeborgt? ", default=False)
    id = HiddenField()
    submit = SubmitField()


class DeleteForm(FlaskForm):
    checkbox = BooleanField("Möchten Sie dieses Object wirklich löschen?")
    passphrase = PasswordField("Sicherheitscode eingeben: ", validators=[DataRequired()])
    submit = SubmitField()
