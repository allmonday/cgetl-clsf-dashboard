from flask import Flask, render_template, request
from pymongo import MongoClient
from utils import dget
from collections import OrderedDict

#db = MongoClient('192.168.1.21')['caigen-development']
db = MongoClient()['caigen-development']

app = Flask(__name__)

#----------------------route table --------------------------------------
mapping = {
    'formula' : {
                'data':OrderedDict([
                        ('_id', '_id'),
                        ('category', 'transformed.data.category_name'), 
                        ('duanwei', 'transformed.data.duanwei'),
                        ('unit', 'transformed.data.unit.value'),
                        ('variety', 'transformed.data.variety'),
                        ('importd', 'transformed.data.importd'),
                        ('product_name', 'transformed.data.product_name'),
                        ('source', 'transformed.data.source'),
                        ('product_id', 'extracted.data.product_id'),
                        ]), 
                'sort' : ['weight', 'duanwei', 'category']
                },
    'beer' : { 
                'data': OrderedDict([
                        ('_id', '_id'),
                        ('category', 'transformed.data.category_name'), 
                        ('volume', 'transformed.data.unit.value'), 
                        ('alcoholicity', 'transformed.data.alcoholicity'),
                        ('product_name', 'extracted.data.product_name'),
                    ]),
                'sort' : ['alcoholicity', 'volume', 'category']
            }
    }
#----------------------end of route table -------------------------------


@app.route('/')
def index():
    industries = ['formula', 'beer']
    brand = []
    return render_template('index.html', 
                          industries=industries,
                          brand=brand)


@app.route('/industry', methods=['GET'])
def industry():
    '''return the brand name list'''
    global industry
    if request.method== 'GET':
        industry = request.args.get('industry', '')
        if industry:
            brand = db.webpages.distinct('transformed.data.brand_name')
            return  '\n'.join(['<option>%s</option>'%i for i in brand])


@app.route('/brand', methods=['GET'])
def brand():
    '''return products meet the industry& brand'''

    if request.method=='GET':
        
        idsty = dget(mapping, '%s.data'%industry)
        idsty_sort = dget(mapping, '%s.sort'%industry)
        brand_name = request.args.get('brand', '')
        products_db = db.webpages.find({'transformed.data.brand_name': brand_name})

        #for easy to get, write back will be a mess .. so we need a map
        products_key = list(idsty.keys())
        products = [
                    [dget(p, idsty[k], '') for k, v in idsty.items()] 
                    for p in products_db
                   ]

        #sort the data, to the convinent of displaying..
        for fs in idsty_sort:
            try:
                products = sorted(products, key=lambda x: x[products_key.index(fs)])
            except:
                print(fs)

        return render_template('row_template.html', 
                                products = products,
                                titles = list(idsty.keys()))

@app.route('/submit', methods=['GET'])
def submit():
    '''get the post info'''
    if request.method == "GET":
        print(request.args.get('submit'))
    return "hello world"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5478, debug=True)
