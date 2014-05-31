from flask import Flask, render_template, request
from pymongo import MongoClient
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
    if request.method=='GET':
        brand_name = request.args.get('brand', '')
        print(brand_name)
        products_db = db.webpages.find({'transformed.data.brand_name': brand_name})
        products = [{ 'number': i,
                      'category': p['transformed']['data']['category_name'], 
                      'volume': p['transformed']['data'].get('unit',{}).get('value', 'unknown'),
                      'alcoholicity': p['transformed']['data'].get('alcoholicity','unknown'),
                      'product_name': p['transformed']['data']['product_name']
                    } for i, p in enumerate(products_db)]
        products = sorted(products, key=lambda x: x['volume'])
        products = sorted(products, key=lambda x: x['category'],reverse=True)
        print(products)
        return render_template('row_template.html', 
                        products = products)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5478, debug=True)
