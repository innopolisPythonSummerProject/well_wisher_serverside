import flask
from flask_cors import CORS
import holidayAPI
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.environ.get('OPENAI_TOKEN')
openai.organization = os.environ.get('OPENAI_ORG')

app = flask.Flask(__name__)
CORS(app)
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"


@app.route('/holiday', methods=["GET"])
def index():
    args = flask.request.args
    response = {}
    if 'date' in args:
        date = args['date']
        response = flask.jsonify(holidayAPI.getHoliday(date))
    else:
        response = flask.jsonify(holidayAPI.getHoliday())
    print(response)
    response.status_code = 200
    return response


@app.route('/image', methods=["GET"])
def image():
    args = flask.request.args
    response = {}
    if 'prompt' in args:
        prompt = args['prompt']
        image = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
        )
        response = flask.jsonify(image)
        response.status_code = 200
        return response
    else:
        response.status_code = 400
        return response


@app.route('/greeting', methods=["GET"])
def greeting():
    args = flask.request.args
    response = {}
    if 'holiday' in args:
        holiday = args['holiday']
        prompt = f"Напиши поздравление моему другу, поздравь его с днем {holiday}. Сделай его смешным и запоминающимся."
        greeting = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
        )
        response = flask.jsonify(greeting)
        response.status_code = 200
        return response
    else:
        response.status_code = 400
        return response


if __name__ == '__main__':
    app.run(debug=True)
