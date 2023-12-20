from msilib.schema import CheckBox

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flask_wtf.form import _Auto
from wtforms import TextAreaField, RadioField, StringField, SelectField, FileField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput

from app.common import to_readable
from app.domain.Category import Category
from app.domain.Post import Post, PostType
from app.domain.Tag import Tag


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
    categories = SelectField('Category',
                             validators=[
                                 DataRequired(message='Category is required.')
                             ])
    tags = SelectMultipleField('Tags', option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    image = FileField('Image',
                      render_kw={'accept': '.jpg, .jpeg, .png'},
                      validators=[
                          # FileAllowed(['.jpg', '.jpeg,' '.png'])
                      ])
    enabled = BooleanField('Enabled', default=True)

    def __init__(self):
        super(PostForm, self).__init__()
        self.categories.choices = [(category.id, category.name) for category in Category.query.all()]
        self.tags.choices = [(tag.name, tag.name) for tag in Tag.query.all()]

    def validate_categories(self, field):
        category_id = field.data
        if not Category.query.get(category_id):
            raise ValidationError('Undefined category.')


class CategorySearchForm(FlaskForm):
    categories = SelectField('Category',
                             choices=[(category.id, category.name) for category in Category.query.all()])
