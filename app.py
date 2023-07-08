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
# CORS(app)
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"


def insert_holiday(holiday, kitty, sparkles):
    if kitty == 'true' or kitty == 'True':
        kitty = 'with kitties'
    else:
        kitty = ''
    if sparkles == 'true' or sparkles == 'True':
        sparkles = 'with sparkles'
    else:
        sparkles = ''
    return f'''
Stable Diffusion is an AI art generation model similar to DALLE-2.
Below is a list of prompts that can be used to generate images with Stable Diffusion:

- portait of a homer simpson archer shooting arrow at forest monster, front game card, drark, marvel comics, dark, intricate, highly detailed, smooth, artstation, digital illustration by ruan jia and mandy jurgens and artgerm and wayne barlowe and greg rutkowski and zdislav beksinski
- pirate, concept art, deep focus, fantasy, intricate, highly detailed, digital painting, artstation, matte, sharp focus, illustration, art by magali villeneuve, chippy, ryan yee, rk post, clint cearley, daniel ljunggren, zoltan boros, gabor szikszai, howard lyon, steve argyle, winona nelson
- ghost inside a hunted room, art by lois van baarle and loish and ross tran and rossdraws and sam yang and samdoesarts and artgerm, digital art, highly detailed, intricate, sharp focus, Trending on Artstation HQ, deviantart, unreal engine 5, 4K UHD image
- red dead redemption 2, cinematic view, epic sky, detailed, concept art, low angle, high detail, warm lighting, volumetric, godrays, vivid, beautiful, trending on artstation, by jordan grimmer, huge scene, grass, art greg rutkowski
- a fantasy style portrait painting of rachel lane / alison brie hybrid in the style of francois boucher oil painting unreal 5 daz. rpg portrait, extremely detailed artgerm greg rutkowski alphonse mucha greg hildebrandt tim hildebrandt
- athena, greek goddess, claudia black, art by artgerm and greg rutkowski and magali villeneuve, bronze greek armor, owl crown, d & d, fantasy, intricate, portrait, highly detailed, headshot, digital painting, trending on artstation, concept art, sharp focus, illustration
- closeup portrait shot of a large strong female biomechanic woman in a scenic scifi environment, intricate, elegant, highly detailed, centered, digital painting, artstation, concept art, smooth, sharp focus, warframe, illustration, thomas kinkade, tomasz alen kopera, peter mohrbacher, donato giancola, leyendecker, boris vallejo
- ultra realistic illustration of steve urkle as the hulk, intricate, elegant, highly detailed, digital painting, artstation, concept art, smooth, sharp focus, illustration, art by artgerm and greg rutkowski and alphonse mucha

I want you to write me a list of detailed prompts exactly about the idea written after IDEA. Follow the structure of the example prompts. This means a very short description of the scene, followed by modifiers divided by commas to alter the mood, style, lighting, and more.

IDEA: cover for celebrating {holiday} picture {kitty}, {sparkles}

Give the answer in one Prompt without too much information
    '''


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
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/image', methods=["GET"])
def image():
    args = flask.request.args
    response = {}
    if 'prompt' in args:
        prompt = args['prompt']
        kittyOption = args['kitty']
        sparklesOption = args['Sparkles']
        prompt = openai.Completion.create(
            model="text-davinci-003",
            prompt=insert_holiday(prompt, kittyOption, sparklesOption),
            max_tokens=512,
        )["choices"][0]["text"]
        print(prompt)
        image = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
        )
        response = flask.jsonify(image)
        response.status_code = 200
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        response.status_code = 400
        response.headers.add('Access-Control-Allow-Origin', '*')
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
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        response.status_code = 400
        return response


if __name__ == '__main__':
    app.run(debug=True)
