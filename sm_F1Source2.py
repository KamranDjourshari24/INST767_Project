import requests
url = "http://ergast.com/api/f1/drivers.json?=123" 
payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)


# Hi Sean,
# 
# Just wanted to reach out about this other API source that I mentioned was giving me some trouble. Here is the source for reference again: 
# https://documenter.getpostman.com/view/11586746/SztEa7bL#intro
# 
# Within the intro it states " Response formats The API supports XML, JSON and JSONP response formats. XML is returned by default or when ".xml" is appended to URLs. JSON is obtained by appending ".json" to URLs" 
# 
# Just to test and experiment I used the "List of All Drivers"  within the "Drivers" folder from the left hand side on the site to attempt to make this work. I have just copied and pasted the provided code given for the xml to work and tried making the ".json" append which currently gives an error. If this would be possibly easier to collaborate on through zoom let me know your availability and we can go from there if that is better. I have my file attached to this email if you want to try something different.
# 
# I really appreciate your time and help,
# Saran Ram 
