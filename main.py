import os
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
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a fantasy world tale teller, skilled in crafting mysterious and "
                                          "engaging adventures."},
            {"role": "user", "content": "Describe in up to 3 sentences a starting point for a hero going on a "
                                        "first quest."}
        ],
        stream=True
    )
    yield "data: \n\n".encode('utf-8')
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
        size="1024x1024",
        n=1,
    )

    image_url = image.data[0].url
    return image_url


if __name__ == '__main__':
    app.run(debug=True)
