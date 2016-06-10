import os
import dataset
import requests

TABLE = 'healthdata'

if __name__ == '__main__':
    source = "http://www.slbr.sl/api/v1/slbiz/health.json"
    resp = requests.get(source)
    data = resp.json()
    for item in data['nodes']:
        item['node'].pop('image')
        table = dataset.connect(os.getenv('SL_DATABASE_URL'))[TABLE]
        table.insert(item['node'])
        print "Inserted {Name}: {description}".format(**item['node'])
