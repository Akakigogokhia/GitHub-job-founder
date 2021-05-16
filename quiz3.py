import json
import requests
import sqlite3

description = input("შეიყვანეთ საძიებო სიტყვა (მაგ. პროგრამირების ენა): ")
location = input("შეიყვანეთ ლოკაცია სადაც გსურთ სამუშაოს ძებნა(ქალაქი,ზიპ კოდი): ")
payload = {'description': description, 'location': location}
resp = requests.get("https://jobs.github.com/positions.json?", params=payload)
print(resp.status_code)
print(resp.headers)
print(resp.url)
res = json.loads(resp.content)
print(json.dumps(res, indent=4))
for i in res:
    if i['location'] == 'Remote':
        print(i['url'])

with open('data.json', 'w') as f:
    json.dump(res, f, indent=4)

conn = sqlite3.connect('jobs.sqlite')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE jobs 
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description varchar(250),
        location varchar(50),
        company varchar(50),
        title varchar(250),
        url = varchar(100)
        )
''')
rows_list = []
rows = tuple()
for d in res:
    for j in d:
        description = i['description']
        location = i['location']
        company = i['company']
        title = i['title']
        url = i['url']
    rows = (description, location, company, title, url)
    rows_list.append(rows)
cursor.executemany("INSERT INTO jobs (description, location, company, title) VALUES (?, ?, ?, ?)", rows_list)
conn.commit()
