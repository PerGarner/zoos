from flask import Blueprint, render_template, request

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/', methods=['GET', 'POST'])


def mainpage():
    return render_template('main.html')
