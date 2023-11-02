from app import app, data_base
from app.common.common import render, to_readable
from .domain.Feedback import Satisfaction, Feedback
from .forms import AddFeedback
from flask import redirect, url_for, request, flash, session


@app.route('/feedback', methods=['GET'])
def feedback():
    form = AddFeedback()
    feedbacks = Feedback.query.all()
    return render('feedback/feedback', form=form, feedbacks=feedbacks, readable=to_readable)


@app.route('/feedback', methods=['POST'])
def add_feedback():
    form = AddFeedback()
    if not form.validate_on_submit():
        return render('feedback/feedback', form=form)

    feedback = form.feedback.data
    satisfaction = Satisfaction[form.satisfaction.data]

    entity = Feedback(feedback=feedback, satisfaction=satisfaction)
    data_base.session.add(entity)
    data_base.session.commit()
    return redirect(url_for('feedback'))
