#!/usr/bin/env python3
import cgi
import html

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
for key in key_set: 
    value = form_data.getvalue(key)
    right_answer = right_answers[key]

    if type(right_answer) == list:
        points = 1 / len(right_answer)
        for variant in right_answer:
            if variant in value:
                mark += points
    else:
        mark += 1 if right_answer == value else 0

print(f"Total points: {mark}")