from flask import Flask
from database import init_db
from controllers import lister, main, sjov, findetdyr

init_db()

app = Flask(__name__)

app.register_blueprint(lister.bp)
app.register_blueprint(main.bp)
app.register_blueprint(sjov.bp)
app.register_blueprint(findetdyr.bp)
