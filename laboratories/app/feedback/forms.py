from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField
from wtforms.validators import DataRequired

from app.common import to_readable
from app.domain.Feedback import Satisfaction


class AddFeedback(FlaskForm):
    feedback = TextAreaField("Feedback",
                             render_kw={'placeholder': 'Give your feedback...'},
                             validators=[
                                 DataRequired(message="Feedback is required.")
                             ])
    satisfaction = RadioField("Satisfaction",
                              choices=[(satisfaction.name, to_readable(satisfaction.value)) for satisfaction in
                                       Satisfaction],
                              validators=[
                                  DataRequired(message="Select your level of satisfaction.")
                              ])
