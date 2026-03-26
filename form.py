from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField

class ContactForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    subscribe = BooleanField("Subscribe to our newsletter?")
    message = CKEditorField('Message:', validators=[DataRequired()])
    submit = SubmitField("Submit ☺️")
