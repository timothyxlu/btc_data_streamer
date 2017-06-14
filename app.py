import datasource.okcoin
import persistance.mongo

if __name__ == '__main__':
    persister = persistance.mongo.MongoPersister.get_persister('okcoin', 'ok_sub_spotusd_btc_ticker')
    client = datasource.okcoin.OkcoinClient(persister=persister, channel='ok_sub_spotusd_btc_ticker')
    client.run()
