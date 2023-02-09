import requests
from .exceptions import InvalidPassword

BASE_URL = "https://aviral.iiita.ac.in/api/"

def auth(user : str, password: str):
    if (user == "test"):
        raise InvalidPassword
    
    s = requests.session()
    resp = s.post(BASE_URL+'login/', json={"username": user.lower(), "password": password}).json()
    if(resp["user_group"]):
        auth = {
            "Authorization": resp["jwt_token"]
        }
        auth["session"] = resp["session_id"]
        s.headers.update(auth)
        det = s.get(BASE_URL+'student/dashboard/').json()
        deatils = {
            "uid": det["student_id"],
            "name": (det["first_name"]+" "+det["middle_name"]+" "+det["last_name"]).strip(),
        }
        return deatils
    else:
        raise InvalidPassword
