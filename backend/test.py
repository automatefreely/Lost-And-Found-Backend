from datetime import datetime

r = str(datetime.now())
print(r)

d = datetime.fromisoformat(r)
print(d, type(d))