import requests

def connection_result() -> bool:
    try:
        response = requests.get(url="https://www.google.com", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False