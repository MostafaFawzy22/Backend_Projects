from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=10, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Regexp("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField('Sign Up')
    def __repr__(self):
        return f'<RegistrationForm {self.full_name}>'
    
    def validate_image_file(self, field):
        if field.data is not None:
            if field.data.mimetype not in ['image/jpg', 'image/png']:
                raise validator.ValidationError('Please upload a JPG or PNG image')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")
    
class UpdateProfileForm(FlaskForm):
    full_name = StringField(
        "Username", validators=[DataRequired(), Length(min=15, max=30)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    bio = TextAreaField("Bio")
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField("Update")
    
    def __repr__(self):
        return f'<UpdateProfileForm {self.full_name}>'
    
    def validate_image_file(self, field):
        if field.data is not None:
            if field.data.mimetype not in ['image/jpg', 'image/png']:
                raise validator.ValidationError('Please upload a JPG or PNG image')

class VideoForm(FlaskForm):
    name = StringField(
        "Film", validators=[DataRequired(), Length(min=5, max=30)]
    )
    type_video = StringField(
        "Type Film", validators=[DataRequired(), Length(min=5, max=30)]
    )
    picture = FileField(
        "Add Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField('Add Film')
    def validate_image_file(self, field):
        if field.data is not None:
            if field.data.mimetype not in ['image/jpg', 'image/png']:
                raise validator.ValidationError('Please upload a JPG or PNG image')
            
class Video_NameForm(FlaskForm):
    type_video = StringField(
        "Type Film", validators=[DataRequired(), Length(min=2, max=30)]
    )
    picture = FileField(
        "Add Picture", validators=[FileAllowed(["jpg", "png", "jfif"])]
    )
    submit = SubmitField('Add Events')
    def validate_image_file(self, field):
        if field.data is not None:
            if field.data.mimetype not in ['image/jpg', 'image/png']:
                raise validator.ValidationError('Please upload a JPG or PNG image')

class UpdateFilmForm(FlaskForm):
    name = StringField(
        "Film", validators=[DataRequired(), Length(min=5, max=30)]
    )
    type_video = StringField(
        "Type Film", validators=[DataRequired(), Length(min=5, max=30),Regexp("(series|movies|anime)")]
    )
    picture = FileField(
        "Add Picture", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField('Add Film')
    def __repr__(self):
        return f'<UpdateProfileForm {self.name}>'
    def validate_image_file(self, field):
        if field.data is not None:
            if field.data.mimetype not in ['image/jpg', 'image/png']:
                raise validator.ValidationError('Please upload a JPG or PNG image')
            
class SearchForm(FlaskForm):
    search = StringField(
        "Search", validators=[Length(min=2, max=30)]
    )
    submit = SubmitField('Search')
    def __repr__(self):
        return f'<UpdateProfileForm {self.search}>'