from flask import Flask, request
from marvel_model import Marvel
import json

server = Flask(__name__)

@server.route('/searchComics/', methods=['GET'])
def search():
    '''
    Get request parameters: 
    {
        'query' (optional): search query (str),
        'type' (optional): filter search by 'comics' or 'characters' only (str)
    }
    '''
    query = request.args.get('query', default='')
    type = request.args.get('type', default='')

    if type not in ['characters','comics', '']:
        return 'Missing valid type: characters or comics', 400

    MarvelAPI = Marvel()
    result = MarvelAPI.search(query,type)

    return result, 200

if __name__=='__main__':
    server.run(host='0.0.0.0', port=5000)