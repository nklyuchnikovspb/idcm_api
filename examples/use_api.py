from idcm_api import IDCMApi

if __name__ == '__main__':
    '''
    get_depth method use public api, so you don`t need to use correct key and secret
    '''
    API_KEY = ''
    API_SECRET = ''

    api = IDCMApi(key=API_KEY, secret=API_SECRET)

    response = api.get_depth(currency='OST', base_currency='BTC')
    print(response)
