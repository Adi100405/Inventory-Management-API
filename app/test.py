from auth.hashing import (
    hash_password,
    verify_password
)

hashed = hash_password("123456")

print(hashed)

print(
    verify_password(
        "123456",
        hashed
    )
)