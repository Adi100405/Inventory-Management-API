from auth.security import create_access_token

token = create_access_token(
    {"sub": "aditya@gmail.com"}
)

print(token)