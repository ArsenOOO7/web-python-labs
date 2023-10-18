#!/usr/bin/env python3

import cgi
import html
import os
from http.cookies import SimpleCookie

cookie = SimpleCookie(os.environ.get("HTTP_COOKIE"))
counter = int(cookie["counter"].value) if "counter" in cookie.keys() else 0

content = f"""

<div class="block">
    <p>You have passed this test {counter} times</p>
    <p><a href="/cgi-bin/clear.py"><button>Clear cookies</button></a></p>
</div>

"""


print("Content-type:text/html\r\n\r\n")
with open('resources/template.html', 'r') as file:
    data = file.read()
    data = data.replace("{{content}}", content)
    print(data)