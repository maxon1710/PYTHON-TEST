class TestPage:
    def __init__(self, input_login, input_password):
        self.name_secret = input_login
        self.super_secret = input_password

Max = TestPage("max", "2001")
Dima = TestPage("dmitry", "1999")
print(Max.name_secret)
print(Max.super_secret)


class TestPage:
    def __init__(self, username, password):
        self.username = username
        self.password = password

Max = TestPage("max", "2001")
Dima = TestPage("dmitry", "1999")
print(Dima.username)
print(Dima.password)
