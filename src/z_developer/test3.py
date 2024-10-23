from auth_jwt.schemas import UserAuthJWT


john = UserAuthJWT(
    username="john",
    password="qwerty",
    active=True,
    email="j111@1111j.com",
)
print(john.username, john.password, john.email)

# print(settings.auth_jwt.algorithm)
