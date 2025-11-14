#
# forms.py
# ----------
# Book database project
# (c) Lars Lerchbacher 2025
#


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, IntegerField, BooleanField, HiddenField, PasswordField, DateField, SearchField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField("Titel : ", validators=[DataRequired()])
    authors = SelectMultipleField("Author/en: ", choices=[], coerce=int, validate_choice=False)
    publisher = StringField("Verlag: ")
    isbn = StringField("ISBN-13 (Nur Ziffern): ")
    edition = IntegerField("Auflage Nr. :", default=1)
    year = IntegerField("Erscheinungsjahr: ", default=2000)
    type = SelectField("Buchtyp: ", choices=[], coerce=int, validate_choice=False)
    tags = StringField("Kategorie/n (mit ; trennen): ")
    room = SelectField("Zimmer: ", choices=["Lars Zimmer", "Linos Zimmer", "Lilos Zimmer", "Schlafzimmer", "Bibliothek", "Wohnzimmer", "Arbeitszimmer", "Sonst irgendwo"])
    shelf = StringField("Regal und/oder Fach: ")
    lend = HiddenField()
    id = HiddenField()
    submit = SubmitField()


class DeleteForm(FlaskForm):
    checkbox = BooleanField("Möchten Sie dieses Object wirklich löschen?")
    passphrase = PasswordField("Sicherheitscode eingeben: ", validators=[DataRequired()])
    submit = SubmitField()


class AuthorForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    country = StringField("Land: ", validators=[DataRequired()])
    birthdate = DateField("Geburtsdatum: ", validators=[DataRequired()], format="%Y-%m-%d")
    date_of_death = DateField("Sterbedatum: ")
    has_nobel_prize = BooleanField("Hat einen Nobel-Preis: ")
    id = HiddenField()
    submit = SubmitField()


class SearchForm(FlaskForm):
    searchBar = SearchField("Allgemeine Suche")
    submit = SubmitField("Suche")


class BookSearchForm(FlaskForm):
    title = StringField("Titel : ")
    authors = SelectMultipleField("Author/en: ", choices=[], coerce=int, validate_choice=False)
    publisher = StringField("Verlag: ")
    isbn = StringField("ISBN-13 (Nur Ziffern): ")
    edition = IntegerField("Auflage Nr. :")
    year = IntegerField("Erscheinungsjahr: ")
    type = SelectField("Buchtyp: ", choices=[], coerce=int, validate_choice=False)
    tags = StringField("Kategorie/n (mit ; trennen): ")
    room = SelectField("Zimmer: ", choices=["Bitte auswählen", "Lars Zimmer", "Linos Zimmer", "Lilos Zimmer", "Schlafzimmer", "Bibliothek", "Wohnzimmer", "Arbeitszimmer", "Sonst irgendwo"])
    shelf = StringField("Regal und/oder Fach: ")
    lend = SelectField("Ausgeborgt von: ")
    id = IntegerField("Id: ")
    submit = SubmitField("Suche")


class AuthorSearchForm(FlaskForm):
    name = StringField("Name: ")
    country = StringField("Land: ")
    birthdate = DateField("Geburtsdatum: ", format="%Y-%m-%d")
    date_of_death = DateField("Sterbedatum: ")
    has_nobel_prize = SelectField("Hat einen Nobel Preis: ", choices=["Bitte auswählen", "Ja", "Nein"])
    id = IntegerField("Id: ")
    submit = SubmitField("Suche")
