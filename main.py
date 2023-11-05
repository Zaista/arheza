from flask import escape
from dotenv import dotenv_values
from google.cloud import secretmanager

import openai
import functions_framework

# env = dotenv_values(".env")
# openai.api_key = env["OPENAI_API_KEY"]


client = secretmanager.SecretManagerServiceClient()
secret_name = "projects/307352298506/secrets/openai-api-key/versions/1"

response = client.access_secret_version(name=secret_name)
openai.api_key = response.payload.data.decode("UTF-8")


@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and "name" in request_json:
        name = request_json["name"]
    elif request_args and "name" in request_args:
        name = request_args["name"]
    else:
        name = "John Doe"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming "
                                          "concepts with creative flair. Start with a greeting to " + escape(name)},
            {"role": "user", "content": "Compose a poem that explains the basic concept of chatGPT."}
        ]
    )

    return completion.choices[0].message.content
