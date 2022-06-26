import random
import string

t_user = {
    "username": "testuser001",
    "email": "testemail@gmail.com",
    "pwd": "Testpwd123",
    "profile-pic": "https://cdn.pixabay.com/photo/2016/09/25/23/25/stones-1694879_960_720.jpg"
}


def random_char(y):  # generates a random e-mail address
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


t_user.update({"email": random_char(6) + "@gmail.com"})  # sets random e-mail address

t_comment = {
    "comment": "This is a new comment."
}
