from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms import StringField, PasswordField, IntegerField, DateField

class AddFoodForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=1, max=100)])
    quantity = IntegerField('quantity', validators=[DataRequired()])
    expiration_date = DateField('expiration_date', validators=[DataRequired()])