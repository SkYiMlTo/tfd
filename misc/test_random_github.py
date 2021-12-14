import requests
from base64 import b64encode

client_id = ''
client_secret = ''
code = ''
scopes = ''
redirect_uri = ''

url = 'https://accounts.spotify.com/api/token'
#auth_header = b64encode(six.text_type(client_id + ':' + client_secret).encode('ascii'))
auth_header = '58d8a0730d2144e48ddea65b6033ad39:87ac3f4c385244448cb02b728ab4b9ed'
headers = {'Authorization':'Basic %s' % auth_header}
data = {'redirect_uri':redirect_uri,
    'code':code,
    'grant_type':'authorization_code',
    'scope':scopes}
r = requests.post(url, data=data, headers=headers, verify=True)
token_info = r.json()
print(token_info)
