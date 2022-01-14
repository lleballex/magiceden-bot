import requests
from json import dumps
from loguru import logger


class Parser:
    def __init__(self, collection, filters={}, id=0):
        self.url = 'https://api-mainnet.magiceden.io/rpc/getListedNFTsByQuery'
        self.collection = collection
        self.checked_items = []
        self._filters = {}
        self.filters = filters.copy()
        self.id = id

        price = {}
        if filters.get('min_price'):
            price['$gte'] = int(filters.pop('min_price') * 10**9)
        if filters.get('max_price'):
            price['$lte'] = int(filters.pop('max_price') * 10**9)

        _filters = []
        for filter in filters:
            _filter = []
            for value in filters[filter]:
                _filter.append({'attributes': {
                    '$elemMatch': {'trait_type': filter, 'value': value},
                }})
            _filters.append({'$or': _filter})

        if _filters: self._filters['$and'] = _filters
        if price: self._filters['takerAmount'] = price

        self.params = self._get_params()

    def _get_params(self, limit=7):
        return dumps({
            '$match': {'collectionSymbol': self.collection, **self._filters},
            '$sort': {'createdAt': -1},
            '$skip': 0,
            '$limit': limit,
        })

    @classmethod
    def from_model(cls, model):
        return cls(model.collection, model.get_filters(), model.id)

    def parse(self, initial=False):
        if len(self.checked_items) > 50:
            logger.debug('update')
            self.checked_items = self.checked_items[len(self.checked_items) - 30:len(self.checked_items)]

        params = (self._get_params(30) if initial else self.params)
        response = requests.get(f'{self.url}?q={params}')

        if response.status_code != 200:
            return (False, response.status_code)

        items = []

        for item in response.json()['results']:
            if not item['escrowPubkey'] in self.checked_items and item['price']:
                logger.debug(f'New: {item["title"].split()[-1]} - {item["mintAddress"]}'
                             f' - {item["escrowPubkey"]} - {item["price"]}')

                self.checked_items.append(item['escrowPubkey'])
                items.append({
                    'image': item['img'],
                    'url': f'https://magiceden.io/item-details/{item["mintAddress"]}',
                    'price': f'{item["price"]} SOL',
                    'collection': item['collectionTitle']
                })
            else:
                logger.debug(f'Old: {item["title"].split()[-1]} - {item["mintAddress"]}'
                             f' - {item["escrowPubkey"]} - {item["price"]}')

        return (True, items[::-1])

    def get_text(self):
        text = f'{self.collection}\n\n'
        filters = self.filters.copy()

        if filters.get('min_price'):
            text += f'MIN PRICE: {filters.pop("min_price")}\n'
        if filters.get('max_price'):
            text += f'MAX PRICE: {filters.pop("max_price")}\n'

        for filter in filters:
            text += f'{filter}: {(", ").join([str(value) for value in self.filters[filter]])}\n'

        return text