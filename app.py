from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from routes.upload import upload

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(upload)

@app.route("/")
def home():
    return render_template("dashboard.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)