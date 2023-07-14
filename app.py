import flask
import holidayAPI
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.environ.get("OPENAI_TOKEN")
openai.organization = os.environ.get("OPENAI_ORG")

app = flask.Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSONIFY_MIMETYPE"] = "application/json; charset=utf-8"


def insert_holiday(holiday, kitty, sparkles):
    """
    Returns a string containing a list of detailed prompts for generating images with Stable Diffusion based on the provided holiday, kitty and sparkles options.

    Args:
    holiday (str): The name of the holiday to celebrate.
    kitty (str): The option to include kitties in the generated image. Must be 'true' or 'false'.
    sparkles (str): The option to include sparkles in the generated image. Must be 'true' or 'false'.

    Returns:
    str: A string containing a list of detailed prompts for generating images with Stable Diffusion.
    """
    if kitty == "true" or kitty == "True":
        kitty = "with kitties"
    else:
        kitty = ""
    if sparkles == "true" or sparkles == "True":
        sparkles = "with sparkles"
    else:
        sparkles = ""
    return f"""
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
"""


@app.route("/holiday", methods=["GET"])
def index():
    """
    Returns a JSON response containing information about a holiday based on the date provided in the request arguments.
    If no date is provided, returns information about the current day's holiday.

    Args:
    date (str, optional): The date for which to retrieve holiday information. Must be in the format "YYYY-MM-DD".

    Returns:
    flask.Response: A JSON response containing information about the holiday.
    """
    args = flask.request.args
    response = {}
    # If there is a date in the arguments, get the holiday for that date
    if "date" in args:
        date = args["date"]
        # Create a JSON response with the holiday information
        response = flask.jsonify(holidayAPI.getHoliday(date))
    # If there is no date in the arguments, get the holiday for the current date
    else:
        response = flask.jsonify(holidayAPI.getHoliday())
    print(response)
    response.status_code = 200
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/image", methods=["GET"])
def image():
    """
    Generates an image based on a prompt using OpenAI's text-davinci-003 model and Image API.

    Returns:
    flask.Response: A JSON response containing the generated image.
    """
    args = flask.request.args
    response = {}
    if "prompt" in args:
        # Get the prompt from the arguments
        prompt = args["prompt"]
        # Get the kitty option from the arguments
        kitty_option = args["kitty"]
        # Get the sparkles option from the arguments
        sparkles_option = args["Sparkles"]
        # Generate a completion using OpenAI's text-davinci-003 model
        prompt = openai.Completion.create(
            model="text-davinci-003",
            prompt=insert_holiday(prompt, kitty_option, sparkles_option),
            max_tokens=512,
        )["choices"][0]["text"]
        # Print the generated prompt
        print(prompt)
        # Generate an image using OpenAI's Image API
        image = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
        )
        # Create a JSON response with the generated image
        response = flask.jsonify(image)
        response.status_code = 200
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        # If there is no prompt in the arguments, return a 400 error
        response.status_code = 400
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


@app.route("/greeting", methods=["GET"])
def greeting():
    """
    Generates a funny and memorable greeting message for a friend's holiday.

    Returns:
    flask.Response: A JSON response containing the generated greeting message.
    """
    args = flask.request.args
    response = {}
    if "holiday" in args:
        # Get the holiday from the arguments
        holiday = args["holiday"]
        # Generate a completion using OpenAI's text-davinci-003 model
        prompt = f"Напиши поздравление моему другу, поздравь его с днем {holiday}. Сделай его смешным и запоминающимся."
        greeting = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
        )
        # Create a JSON response with the generated greeting
        response = flask.jsonify(greeting)
        response.status_code = 200
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    # If there is no holiday in the arguments, return a 400 error
    else:
        response.status_code = 400
        return response


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
