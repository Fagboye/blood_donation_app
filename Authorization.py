# import the relevant libraries
import jwt
from dotenv import load_dotenv
import os

# import the secret token from the .env file 
load_dotenv()



# define the generate_token function 
def generate_token(user_id):
  #define the payload for the token 
  payload = {'user_id': user_id}

  # generate the token 
  token = jwt.encode(payload, os.getenv("SECRET_TOKEN"), algorithm='HS256')

  #return the token as a string
  return token


# FUNCTION TO CHECK THE AUTHORIZATION OF THE USER WHEN INTERACTING WITH THE DATABASE
def get_user_id_from_token(token):
       try:
           payload = jwt.decode(token, os.getenv("SECRET_TOKEN"), algorithms=['HS256'])
           user_id = payload['user_id']
           return user_id
       except jwt.ExpiredSignatureError:
           return None
       except jwt.InvalidTokenError:
           return None
