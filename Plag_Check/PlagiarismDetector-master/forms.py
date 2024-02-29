from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, FileField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired


class PlagForm(FlaskForm):
    checkText = TextAreaField('Cosine_Similarity Algorithm', validators=[DataRequired()])
    fileInput = FileField('Upload Pdf')
    submit = SubmitField('Submit')



class matchingform(FlaskForm):
    checkText = TextAreaField('Boyer-Moore Algorithm', validators=[DataRequired()])
    fileInput = FileField('Upload Pdf')
    submit = SubmitField('Submit')
    algorithm = HiddenField('Algorithm', default='cosine')


class Ngarmform(FlaskForm):
    checkText = TextAreaField('N-gram Algorithm', validators=[DataRequired()])
    fileInput = FileField('Upload Pdf')
    submit = SubmitField('Submit')


class fingerprintingform(FlaskForm):
    checkText = TextAreaField('Fingerprinting Algorithm', validators=[DataRequired()])
    fileInput = FileField('Upload Pdf')
    submit = SubmitField('Submit')


class cosineform(FlaskForm):
    checkText = TextAreaField('Cosine_Similarity Algorithm', validators=[DataRequired()])
    fileInput = FileField('Upload Pdf')
    submit = SubmitField('Submit')

