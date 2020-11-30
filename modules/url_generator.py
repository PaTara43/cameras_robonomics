import ast
import logging
import requests


def create_url():

    url = "https://url.today/yourls-api.php"
    querystring = {"username":"vadim.manaenko","password":"W&t88e54dzLrC5f","action":"shorturl","format":"json","url":"http://gateway.ipfs.io"}
    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring)

    logging.debug(response.text)
    keyword = ast.literal_eval(response._content.decode('utf-8'))['url']['keyword']
    link = "url.today/"+keyword
    return keyword, link

def update_url(keyword, hash):

    url = "https://url.today/yourls-api.php"
    querystring = {"username":"vadim.manaenko","password":"W&t88e54dzLrC5f","action":"update","format":"json","url":"http://gateway.ipfs.io/ipfs/"+hash,"shorturl":keyword}
    payload = ""
    response = requests.request("GET", url, data=payload, params=querystring)

    logging.debug(response)

if __name__ == '__main__':
    keyword, link = create_url()
    print(link)
    update_url(keyword, 'QmS9vM9YkuXPcceDg6dSMvnKtd21p1j3pdkEJ5y5HAnkzy')
