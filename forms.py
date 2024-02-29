from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email


class EditCustomer(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    street = StringField('Street', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    submit = SubmitField(label="Submit")

class NewCustomer(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    surname = StringField('Surname', validators=[InputRequired()])
    street = StringField('Street', validators=[InputRequired()])
    city = StringField('City', validators=[InputRequired()])
    zip = StringField('Zip', validators=[InputRequired()])
    country = StringField('Country', validators=[InputRequired()])  
    country_code = StringField('Country Code', validators=[InputRequired()])
    national_id = StringField('National Id', validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])

