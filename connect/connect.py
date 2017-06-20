"""
Name:	GroupDB
Author:	John Rachwan

How to: Double click and provide the group name
BUT make sure your database has the following column names with the exact same syntax for it to properly work
First_name, Last_name, Position, Email, Comapany

Also make sure the api key is up to date with the one in this code
"""
import pyodbc
import json
import collections
import requests
import csv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=BE-09-095\SQLEXPRESS;DATABASE=gophish;')
cursor = conn.cursor()
cursor.execute("""
            SELECT First_name, Last_name, Position, Email, Comapany
            FROM Users
            """)
rows = cursor.fetchall()
rowarray_list = []
for row in rows:
    t = (row.First_name, row.Last_name, row.Position, row.Email)
    rowarray_list.append(t)

j = json.dumps(rowarray_list)
rowarrays_file = 'student_rowarrays.js'
f = open(rowarrays_file,'w')
print (f, j)
# Convert query to objects of key-value pairs

objects_list = []
for row in rows:
    d = collections.OrderedDict()
    d['First_name'] = row.First_name
    d['Last_name'] = row.Last_name
    d['Position'] = row.Position
    d['Email'] = row.Email
    d['Comapany'] = row.Comapany
    objects_list.append(d)

j = json.dumps(objects_list)
objects_file = 'student_objects.js'
f = open(objects_file, 'w')
#print (f, j)
#print(objects_list)
conn.close()

#####################################
#######Convert json into CSV file####
#####################################


x= json.loads(j)
f=csv.writer(open("targets.csv","wb+"))
f.writerow(["First Name", "Last Name", "Position", "Email","Company"])
for x in x:
    f.writerow([x["First_name"],
                x["Last_name"],
                x["Position"],
                x["Email"],
                x["Comapany"]
                ])


f=1
###########################################
#POST CSV file to get back targets in json#
###########################################

api_key = '32fdd0a809afcae2e6ac951e4691e0581a9a7813d3e696b37f641c1854718775'
csvfile = {'file': open('targets.csv')}
response = requests.post("https://localhost:3333/api/import/group?api_key="+ api_key,files=csvfile,verify=False)
data = json.dumps(response.json())
#print(data)

#################################
##########Create Group###########
#################################
groupname = raw_input('Enter a group name: ')
id = raw_input('Enter a id: ')
id = int(id)
f = {
  "id": id,
  "name": groupname,
  "modified_date": "2015-01-01T01:02:03.000000Z",
  "targets":response.json()
}
json_data=json.dumps(f)
#print json_data

respon = requests.post("https://localhost:3333/api/groups/?api_key="+ api_key,data=json_data,verify=False)