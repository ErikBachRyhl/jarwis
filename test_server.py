import requests

print(
    requests.post(
        "http://127.0.0.1:8000/graph",
        json={
            "topic": "General Relativity"
            #"openai_api_key": "sk-xxxx"
        }
    ).json()
)