# from dotenv import dotenv_values
import functions_framework
from openai import OpenAI
from google.cloud import secretmanager

# env = dotenv_values(".env")
# openai.api_key = env["OPENAI_API_KEY"]

client = secretmanager.SecretManagerServiceClient()
secret_name = "projects/307352298506/secrets/openai-api-key/versions/1"

response = client.access_secret_version(name=secret_name)
# openai.api_key = response.payload.data.decode("UTF-8")
client = OpenAI(api_key=response.payload.data.decode("UTF-8"))


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

    if request.path == "/image":
        print("requesting image")
        image = client.images.generate(
            prompt=request.get_json()["prompt"],
            size="1024x1024",
            n=1,
        )

        image_url = image.data[0].url
        return image_url
    else:
        print("requesting chatGTP")
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a fantasy world tale teller, skilled in crafting mysterious and "
                                              "engaging adventures."},
                {"role": "user", "content": "Describe in up to 3 sentences a starting point for a hero going on a "
                                            "first quest."}
            ]
        )

        return completion.choices[0].message.content
