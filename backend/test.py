from secrets import token_urlsafe

for i in range(10):
    print(token_urlsafe(16))