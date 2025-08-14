from flask import Blueprint, render_template, request
from models.findetdyr import get_animallist, get_zoos, get_info


bp = Blueprint('finddyr', __name__, url_prefix='/')


@bp.route('/findetdyr', methods=['GET', 'POST'])

def findetdyr():
    animallist = get_animallist()
    data = []
    dyr = 'Intet valgt'
    info = ''
    if request.method == 'POST':
        dyr = request.form['choose_query']
        data = get_zoos(dyr)
        info = get_info(dyr)
    return render_template('finddyr.html', animallist=animallist, data = data, dyr=dyr, info=info)