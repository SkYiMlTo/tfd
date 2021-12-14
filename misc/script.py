# import equests
#
# C = "7Je5n5Eh00MEiq27PSAkT9"
# NC = "6d0BMqF6SF59tCQHtwA2rP"
#
# req =   response.request
#
# command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
# method = req.method
# uri = req.url
# data = req.body
# headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
# headers = " -H ".join(headers)
# return command.format(method=method, headers=headers, data=data, uri=uri)
#
# r = test_requests.post('curl -X "POST" "https://api.spotify.com/v1/playlists/6d0BMqF6SF59tCQHtwA2rP/tracks?uris=spotify%3Atrack%3A5AtpIUEM221ILCVt93RMj4" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer token"')
# r.json()
