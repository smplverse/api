from flask import Flask

from src.inference_package.matcher import Matcher

app = Flask(__name__)


@app.route("/")
def hello():
    matcher = Matcher()
    print(matcher)
    return "asdf"
