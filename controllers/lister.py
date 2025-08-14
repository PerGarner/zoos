from flask import Blueprint, render_template, request
from models.lister import list_animals, list_zoos


bp = Blueprint('lister', __name__, url_prefix='/')

@bp.route('/lister', methods=['GET', 'POST'])
def lister():
    animals = []
    chosen_zoo = ''
    søgeord = ''
    zoos = list_zoos()
    if request.method == 'POST':
        chosen_zoo = request.form['choose_zoo']
        søgeord = request.form['searched_for']
        animals = list_animals(chosen_zoo, søgeord)
    return render_template('lister.html', animals=animals, zoos=zoos, chosen_zoo=chosen_zoo, søgeord=søgeord)
   