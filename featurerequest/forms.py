from crud_factory.auth import ValidationFailed
from wtforms import StringField, PasswordField, BooleanField, ValidationError, SelectField, \
    FloatField, IntegerField, widgets, Field, HiddenField, FormField, SelectMultipleField, RadioField
from wtforms_components import DateRange
from flask_wtf import FlaskForm
from wtforms.validators import Optional, DataRequired, Email, EqualTo, NumberRange
from wtforms.ext.dateutil.fields import DateField, DateTimeField
from featurerequest.models import *
from sqlalchemy import or_, func
from dateutil.relativedelta import relativedelta


class RequiredIf(DataRequired):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)


class RequiredOption(DataRequired):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, option_value, *args, **kwargs):
        self.other_field_name = other_field_name
        self.option_value = option_value
        super(RequiredOption, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data == self.option_value):
            super(RequiredOption, self).__call__(form, field)


class IntegerListField(Field):
    """ Custom field to support sending in multiple integers separated by commas and returning the content as a list """

    widget = widgets.TextInput()

    def __init__(self, label='', validators=None, **kwargs):
        super(IntegerListField, self).__init__(label, validators, **kwargs)

    def _value(self):
        if self.data:
            string_data = [str(y) for y in self.data]
            return u','.join(string_data)

        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [int(x.strip()) for x in valuelist[0].split(',')]
        else:
            self.data = []

    def process_data(self, valuelist):
        if valuelist:
            self.data = [int(x.strip()) for x in valuelist[0].split(',')]
        else:
            self.data = []


def check_chars(input):
    """ Checks if there's a special character in the text """

    chars = """ '"!@#$%^&*()+=]}_[{|\':;?/>,<\r\n\t """
    return any((c in chars) for c in input)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', validators=[Optional()])


class SignUpForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[Optional()])
    new_password = PasswordField('Password', validators=[DataRequired()])
    verify_password = PasswordField('Password', validators=[DataRequired(), EqualTo('new_password')])


class RequestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    client_id = SelectField('Client', validators=[DataRequired()], coerce=int)
    client_priority = SelectField('Client Priority', validators=[DataRequired()], coerce=int)
    target_date = DateTimeField('Target Date', validators=[DateRange(
            min=datetime.today(),
            max=datetime.today()+relativedelta(years=65)
        )])
    product_area_code = SelectField('Product Area', validators=[DataRequired()], coerce=str)

    def validate_client_id(self, field):
        if not Client.query.get(field.data):
            raise ValidationError("Invalid Client Selected")

    def validate_product_area_code(self, field):
        if not ProductArea.query.get(field.data):
            raise ValidationError("Invalid Product Area Selected")

    def validate_client_priority(self, field):
        if FeatureRequest.query.filter(FeatureRequest.client_id == self.client_id.data,
                                       FeatureRequest.client_priority == field.data).count()>0:
            raise ValidationError("Existing Priority set for the Client. Kindly choose another priority level.")
