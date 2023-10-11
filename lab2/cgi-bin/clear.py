#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
from http.cookies import SimpleCookie

cookie = SimpleCookie(os.environ.get("HTTP_COOKIE"))

for item in cookie.keys():
    value = cookie[item].value
    expires = datetime.now() - timedelta(seconds=10)
    expires = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
    cookie[item]["expires"] = 0
print(cookie)


print("Content-type:text/html\r\n\r\n")
print("""
    <p>You have cleared up your cookies!</p>
    <p><a href="index.py">Go back</a></p>
    """)