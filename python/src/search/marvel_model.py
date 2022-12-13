import hashlib, time
import requests
import re

class Marvel():

    def __init__(self):
        self.base_endpoint = 'https://gateway.marvel.com'
        self.priv_key = '80e1f7ccdbcacb1bcc1cab0a388061cad0c17b32'
        self.pub_key = '48dff3be35a7dee465601741c0ed9152'

    def __generate_payload(self):
        time_stamp = str(time.time())

        str_to_hash = time_stamp + self.priv_key + self.pub_key
        hash = hashlib.md5(str_to_hash.encode()).hexdigest()

        return {'ts':time_stamp, 'apikey':self.pub_key, 'hash':hash}

    def __request_api_data(self, api):
        '''
        Returns:
            results: (list)
            status_code: (int)
        '''
        api = self.base_endpoint+api
        payload = self.__generate_payload()
        # Extra
        payload['limit'] = 100 # Maximun of data

        response = requests.get(url=api, params=payload)
        response_json = response.json()

        if not response.ok:
            print(f"ClientError: {response_json['code']}. {response_json['message']}")
            return [], response.status_code

        return response_json['data']['results'], response.status_code

    def __get_all_characters(self):
        print('\n\tRequesting all characters...\n')

        return self.__request_api_data('/v1/public/characters')

    def __get_all_comics(self):
        print('\n\tRequesting all comics...\n')

        return self.__request_api_data('/v1/public/comics')

    def __get_thumbnail(self, element):
        if not element.get('thumbnail').get('path'):
            # Image not found placeholder
            return 'https://i0.wp.com/codigoespagueti.com/wp-content/uploads/2022/10/Anya-y-Pochita-se-vuelven-amigos-en-tierno-fanart-de-Chainsaw-Man-y-Spy-x-Family-1.jpg?resize=1280%2C1947&quality=80&ssl=1'
        return f"{element.get('thumbnail').get('path')}.{element.get('thumbnail').get('extension')}"

    def __simplify_characters_response_list(self, response_list):
        return [{
            'id':char.get('id'),
            'name':char.get('name'),
            'image':self.__get_thumbnail(char),
            'appearance':char.get('comics').get('available')
        } for char in response_list]

    def __simplify_comics_response_list(self, response_list):
        def get_sale_date(comic):
            placeholder = [date.get('date') for date in comic.get('dates') if date.get('type')=='onsaleDate']
            if len(placeholder):
                return placeholder[0]
            return ''
                
        return [{
            'id':comic.get('id'),
            'title':comic.get('title'),
            'image':self.__get_thumbnail(comic),
            'onSaleDate':get_sale_date(comic),
            } for comic in response_list]

    def __get_simplified_list(self, type):
        '''
        Input:
            list of dictionaries
        Output:
            same
        '''
        if type=='characters':
            characters, _status = self.__get_all_characters()
            return self.__simplify_characters_response_list(characters)
        elif type=='comics':
            comics, _status = self.__get_all_comics()
            return self.__simplify_comics_response_list(comics)
    
    def __filter_characters_by_name_query(self, simplified_list, str_query):
        pattern = re.compile(f'.*?{str_query.lower()}.*?')
        filtered_list = filter(lambda element_dict: pattern.match(element_dict['name'].lower()), simplified_list )
        return list(filtered_list)

    def __filter_comics_by_name_query(self, simplified_list, str_query):
        pattern = re.compile(f'.*?{str_query.lower()}.*?')
        filtered_list = filter(lambda element_dict: pattern.match(element_dict['title'].lower()), simplified_list )
        return list(filtered_list)

    def search(self, search_query='', type_filter=''):
        
        # If there's filtered by type
        if type_filter=='characters':
            characters = self.__get_simplified_list('characters')

            if not search_query:
                return {'characters':characters}

            # If there's a search query
            return {'characters': self.__filter_characters_by_name_query(characters, search_query)}

        elif type_filter=='comics':
            comics = self.__get_simplified_list('comics')

            if not search_query:
                return {'comics':comics}

            # If there's a search query
            return {'comics': self.__filter_comics_by_name_query(comics, search_query)}

        # If there's no filtered by type:
        characters = self.__get_simplified_list('characters')
        comics = self.__get_simplified_list('comics')

        if not search_query:
            return {'characters':characters, 'comics':comics}

        return {'characters': self.__filter_characters_by_name_query(characters, search_query), 'comics': self.__filter_comics_by_name_query(comics, search_query)}

        