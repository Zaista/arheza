import os
import json
from dotenv import dotenv_values
from flask import Flask, request, render_template, Response
from openai import OpenAI
from google.cloud import secretmanager

if os.getenv('GAE_ENV', '').startswith('standard'):
    client = secretmanager.SecretManagerServiceClient()
    secret_name = "projects/307352298506/secrets/openai-api-key/versions/1"
    secret = client.access_secret_version(name=secret_name)
    apiKey = secret.payload.data.decode("UTF-8")

else:
    env = dotenv_values(".env")
    apiKey = env["OPENAI_API_KEY"]

client = OpenAI(api_key=apiKey)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def generate_output():
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a fantasy world tale teller, skilled in crafting mysterious and "
                                          "engaging adventures. You allways start an answer with a "
                                          "prompt tailored for DALL-E 3 which will generate an image for the story "
                                          "that you are about to tell. Signal the end of the prompt with"
                                          "end-of-image-prompt message. Then continue with the description part that "
                                          "should be approximately 400 characters long."},
            {"role": "user", "content": "Describe a starting point for a hero going on his first quest."}
        ],
        stream=True
    )
    for chunk in completion:
        yield f"data: {chunk.choices[0].delta.content}\n\n".encode('utf-8')


@app.route('/story')
def get_story():
    print("requesting story")
    return Response(generate_output(), content_type='text/event-stream', status=200)


@app.route('/image', methods=['POST'])
def get_image():
    print("requesting image")
    image = client.images.generate(
        prompt=request.get_json()["prompt"],
        model="dall-e-3",
        size="1024x1024",
        n=1,
    )

    image_url = image.data[0].url
    return json.dumps({'url': image_url})


if __name__ == '__main__':
    app.run(debug=True)
