from flask import Flask
from database import init_db
from controllers import lister, main, sjov, findetdyr, omsiden
import os

init_db()

app = Flask(__name__)

app.register_blueprint(lister.bp)
app.register_blueprint(main.bp)
app.register_blueprint(sjov.bp)
app.register_blueprint(findetdyr.bp)
app.register_blueprint(omsiden.bp)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
