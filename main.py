from flask import Flask, render_template, request
from pymongo import MongoClient
from utils import dget
db = MongoClient()['caigen-development']


app = Flask('etl-clsf')

@app.route('/')
def index():
    industries = ['beer', 'baby formula', 'others']
    brand = []
    return render_template('index.html', 
                          industries=industries,
                          brand=brand)


@app.route('/industry', methods=['GET'])
def industry():
    if request.method== 'GET':
        industry = request.args.get('industry', '')
        if industry:
            brand = db.webpages.distinct('transformed.data.brand_name')
            return  '\n'.join(['<option>%s</option>'%i for i in brand])


@app.route('/brand', methods=['GET'])
def brand():
    '''return products meet the industry& brand'''
    if request.method=='GET':

        brand_name = request.args.get('brand', '')
        products_db = db.webpages.find({'transformed.data.brand_name': brand_name})
        #for easy to get, write back will be a mess .. so we need a map
        products = [
                       { 
                            'category': dget(p,'transformed.data.category_name'), 
                            'volume': dget(p,'transformed.data.unit.value'),
                            'alcoholicity': dget(p,'transformed.data.alcoholicity'),
                            'product_name': dget(p,'transformed.data.product_name'),
                            '_id': dget(p, '_id')
                       } 
                            for p in products_db
                   ]
        #sort the data, to the convinent of displaying..
        products = sorted(products, key=lambda x: x.get('volume'))
        products = sorted(products, key=lambda x: x.get('alcoholicity'))
        products = sorted(products, key=lambda x: x.get('category'),reverse=True)

        return render_template('row_template.html', 
                                products = products)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5478, debug=True)
