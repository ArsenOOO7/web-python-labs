from flask import redirect, url_for, flash
from flask_login import current_user, login_required

from app import app, data_base
from app.common.common import render, to_readable
from .domain.Feedback import Satisfaction, Feedback
from .forms import AddFeedback


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

    user = None if not current_user.is_authenticated else current_user.username
    entity = Feedback(feedback=feedback, satisfaction=satisfaction, user=user)
    data_base.session.add(entity)
    data_base.session.commit()
    flash(f"You have successfully added new feedback!", category="success")
    return redirect(url_for('feedback'))


@app.route('/feedback/delete/<int:id>', methods=['GET'])
@login_required
def delete_feedback(id=None):
    if id is None:
        return redirect(url_for('feedback'))

    feedback = data_base.get_or_404(Feedback, id)
    data_base.session.delete(feedback)
    data_base.session.commit()
    flash(f"You have successfully removed feedback with id {feedback.id}!", category="danger")
    return redirect(url_for('feedback'))
