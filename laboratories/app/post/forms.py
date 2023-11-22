from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, RadioField, StringField, SelectField, FileField, BooleanField
from wtforms.validators import DataRequired

from app.common import to_readable
from app.domain.Post import Post, PostType


class PostForm(FlaskForm):
    title = StringField('Title',
                        render_kw={'placeholder': 'Title...'},
                        validators=[
                            DataRequired(message='Title is required.')
                        ])

    text = TextAreaField('Text',
                         render_kw={'placeholder': 'Content...'},
                         validators=[
                             DataRequired(message="Text...")
                         ])
    type = SelectField(label="Type",
                       render_kw={'placeholder': 'Type'},
                       choices=[(postType.name, to_readable(postType.value)) for postType in PostType],
                       validators=[
                           DataRequired(message='Type is required.')
                       ])
    image = FileField('Image',
                      render_kw={'accept': '.jpg, .jpeg, .png'},
                      validators=[
                          FileAllowed(['.jpg', '.jpeg,' '.png'])
                      ])
    enabled = BooleanField('Enabled', default=True)