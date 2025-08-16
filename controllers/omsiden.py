from flask import Blueprint, render_template, request

bp = Blueprint('omsiden', __name__, url_prefix='/')


@bp.route('/omsiden', methods=['GET', 'POST'])


def omsiden():
    return render_template('omsiden.html')
