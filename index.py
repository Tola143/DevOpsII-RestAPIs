# Name: Tola Kan    ID: 6407012662064

from flask import Flask, request, jsonify

app = Flask(__name__)

items = [
    {"name": "iphon", "category": 1, "price": 1400, "instock":  100 },
    {"name": "dell", "category": 2, "price": 2000, "instock":  400 }
    ]

def _find_next_category(category):
    data = [x for x in items if x['category']==category] 
    return data

@app.route('/items', methods=["GET"])
def get_items():
    return jsonify(items)

# GET ---------------------------------------------------------
@app.route('/item/<category>', methods=["GET"])
def get_item(category):
    category = int(category)
    item= _find_next_category(category)
    if items:
        return jsonify(item)
    else:
        return "ERROR 404"
    
# POST ------------------------------------------------------------
@app.route('/add_item/', methods=["POST"])
def post_item():
    category = int(request.form.get('category'))
    name = request.form.get('name')
    price = request.form.get('price')
    instock = request.form.get('instock')
    
    new_data = {
        "category": category,
        "name": name,
        "price": price,
        "instock": instock
    }
 
    if _find_next_category(category):
        return {"error": "Bad Request"}, category
    else:
        items.append(new_data)
        return jsonify(items)

# Put -----------------------------------------------------------------------
@app.route('/update_item/<int:c_category>', methods=["PUT"])
def update_item(c_category): 
    global items
    name = request.form.get('name')
    price = request.form.get('price')
    instock = request.form.get('instock')
    
    for item in items:
        if c_category == item.get('category'):
            item["name"] = str(name)
            item["price"] = str(price)
            item["instock"] = str(instock)
            return jsonify(items)
    else:
        return jsonify({"error": f"Bad Request: there is no item in category {c_category} in the list."}), 404

# Patch ----------------------------------------------------------------------
@app.route('/patch_item/<int:c_category>', methods=['PATCH'])
def patch_item(c_category):
    patch_data = request.get_json()
    for item in items:
        if item['category'] == c_category:
            item["name"]= str(patch_data['name'])
            item["price"]= str(patch_data['price'])
            item["instock"]= str(patch_data['instock'])
            return jsonify(items)
            
    else:
        return jsonify({"error": f"Bad Request: there is no country with id = {c_category} in the list."}), 404

    

# DELETE --------------------------------------------------------------------
@app.route('/delete_item/<int:category>', methods=["DELETE"])
def delete_item(category): 
    global items
    category = int(category)
    for data in items:
        if data['category'] == category:
            items = list(filter(lambda item : item['category'] != category, items))
            return jsonify(items)
        
    else:
        return {"error": f"Bad Request: wrong id = {type(category)}"}, 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)