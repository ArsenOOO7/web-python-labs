from app import app, data_base
from app.common.common import render, to_readable
from .domain.Feedback import Satisfaction, Feedback
from .forms import AddFeedback
from flask import redirect, url_for, flash, session


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

    user = None if session.get('user') is None else session['user']['login']
    entity = Feedback(feedback=feedback, satisfaction=satisfaction, user=user)
    data_base.session.add(entity)
    data_base.session.commit()
    return redirect(url_for('feedback'))


@app.route('/feedback/delete/<int:id>', methods=['GET'])
def delete_feedback(id=None):
    if id is None:
        return redirect(url_for('feedback'))

    if session.get('user') is None:
        return redirect(url_for('login'))

    feedback = data_base.get_or_404(Feedback, id)
    data_base.session.delete(feedback)
    data_base.session.commit()
    return redirect(url_for('feedback'))