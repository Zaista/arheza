python -m venv openai-env

openai-env\Scripts\activate

pip install --upgrade openai

gcloud functions deploy python-http-function --gen2 --runtime=python311 --region=europe-west3 --source=. --entry-point=hello_http --trigger-http --allow-unauthenticated