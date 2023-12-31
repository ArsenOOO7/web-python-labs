#!/usr/bin/env python3
import cgi
import html
import os
from http.cookies import SimpleCookie

cookie = SimpleCookie(os.environ.get("HTTP_COOKIE"))

counter = int(cookie["counter"].value) if "counter" in cookie.keys() else 0

counter += 1
print(f"Set-cookie: counter={counter}")
print("Content-type:text/html\r\n\r\n")

form_data = cgi.FieldStorage()
key_set = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']

right_answers = {
    'first': 'requestMapping',
    'second': 'modelAttribute',
    'third': ['thymeleaf', 'html/jsp'],
    'fourth': ['ioc', 'repository'],
    'fifth': 'Singleton',
    'sixth': '4'
}

mark = 0
question = 1
print("<p> You answers: </p>")
for key in key_set: 
    value = form_data.getvalue(key, "Unanswered")
    right_answer = right_answers[key]

    text = f"<p> {question}. "
    if type(right_answer) == list and type(value) == list:
        text += html.escape(",".join(value))
        points = 1 / len(right_answer)
        for variant in value:
            if variant in right_answer:
                mark += points
    else:
        text += html.escape(value)
        mark += 1 if right_answer == value else 0
    text += "</p>"
    print(text)
    question += 1

seventh = form_data.getvalue('seventh')
print(f"<p>Total points: {mark}</p>")

if seventh == 'java':
    if mark > 5:
        print("Good job!")
    else:
        print("Not a good job...")
else:
    print("Good job!")

print("<p><a href='index.py'>Go back</a></p>")
