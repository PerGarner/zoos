from flask import Blueprint, render_template, request
from models.sjov import get_query, get_querylist, get_columns


bp = Blueprint('sjov', __name__, url_prefix='/')


@bp.route('/sjov', methods=['GET', 'POST'])


def sjovpage():
    data = []
    querylist = get_querylist()
    columns = []
    query = ''
    if request.method == 'POST':
        query = request.form['choose_query']
        data = get_query(query)
        columns = get_columns(query)
    return render_template('sjov.html', data=data, queries = querylist, columns = columns, query=query)