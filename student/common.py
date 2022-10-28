
import jwt
from datetime import datetime, timezone
from server.settings import SECRET_KEY
def generateToken(username, password):

    # Create token based on user data, timestamp, and secret key
    encoded_jwt = jwt.encode({"username": username,
                              "password": password,
                              'timenow': str(datetime.now(timezone.utc))},
                             SECRET_KEY,
                             algorithm="HS256")

    return encoded_jwt
