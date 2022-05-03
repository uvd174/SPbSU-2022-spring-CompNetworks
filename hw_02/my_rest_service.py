"""
Thanks to this (https://habr.com/ru/post/246699/) habr article
for clear explanation of building REST services with Flask.
"""
import json
import os.path
from os.path import join
import uuid

from flask import Flask, jsonify, abort, request, send_file

IMAGES_FOLDER = './images'
ALLOWED_EXTENSIONS = {'png', 'jpg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_json(some_string):
    try:
        json.loads(some_string)
    except (ValueError, TypeError):
        return False
    return True


app = Flask(__name__)
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER


product_list = [
    {
        'id': '12cbb33e-7993-414c-bde7-70f3dc5c4ec1',
        'name': 'Orange',
        'description': 'Oranges are round orange-coloured fruit that grow on a tree',
        'icon': '12cbb33e-7993-414c-bde7-70f3dc5c4ec1.jpg',
    },
    {
        'id': '041b25b1-3580-4340-9d45-dcebda568cd0',
        'name': 'Strawberry',
        'description': 'A strawberry is a small red fruit which is soft and juicy',
        'icon': '041b25b1-3580-4340-9d45-dcebda568cd0.jpg',
    },
]


@app.route('/shop', methods=['GET', 'POST'])
def get_product_list():
    if request.method == 'POST':
        if (
            not request.files
            or not request.form
            or 'product' not in request.form
            or not is_json(request.form['product'])
            or 'name' not in request.form['product']
            or 'description' not in request.form['product']
            or 'image' not in request.files
            or not allowed_file(request.files['image'].filename)
        ):
            abort(400)
        product_data = json.loads(request.form['product'])
        if (
            not isinstance(product_data['name'], str)
            or not isinstance(product_data['description'], str)
        ):
            abort(400)

        product = {
            'id': str(uuid.uuid4()),
            'name': product_data['name'],
            'description': product_data['description'],
        }
        product_list.append(product)

        image_file = request.files['image']
        _, image_extension = os.path.splitext(image_file.filename)
        new_filename = f"{product['id']}{image_extension}"
        image_file.save(os.path.join(app.config['IMAGES_FOLDER'], new_filename))
        product['icon'] = new_filename

    return jsonify(product_list)


@app.route('/shop/<uuid:product_id>', methods=['GET'])
def get_product(product_id):
    product = list(filter(lambda prod: prod['id'] == str(product_id), product_list))
    if len(product) == 0:
        abort(404)
    return jsonify(product[0])


@app.route('/shop/<uuid:product_id>', methods=['PUT'])
def update_product(product_id):
    product = list(filter(lambda prod: prod['id'] == str(product_id), product_list))
    if len(product) == 0:
        abort(404)
    if (
        not request.files
        or not request.form
        or 'product' not in request.form
        or not is_json(request.form['product'])
        or 'name' not in request.form['product']
        or 'description' not in request.form['product']
        or 'image' not in request.files
        or not allowed_file(request.files['image'].filename)
    ):
        abort(400)
    product_data = json.loads(request.form['product'])
    if (
        not isinstance(product_data['name'], str)
        or not isinstance(product_data['description'], str)
    ):
        abort(400)

    product = product[0]
    product['name'] = product_data['name']
    product['description'] = product_data['description']

    image_file = request.files['image']
    _, image_extension = os.path.splitext(image_file.filename)
    new_filename = f"{product['id']}{image_extension}"
    image_file.save(join(app.config['IMAGES_FOLDER'], new_filename))
    product['icon'] = new_filename

    return jsonify(product)


@app.route('/shop/<uuid:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = list(filter(lambda prod: prod['id'] == str(product_id), product_list))
    if len(product) == 0:
        abort(404)
    product_list.remove(product[0])
    os.remove(join(app.config['IMAGES_FOLDER'], product[0]['icon']))
    return jsonify(product_list)


@app.route('/shop/images', methods=['GET'])
def get_images():
    file_names = [
        f"{request.base_url}/{product['icon']}"
        for product in product_list
    ]

    return jsonify(file_names)


@app.route('/shop/images/<string:image_name>', methods=['GET'])
def get_image(image_name):
    image_path = os.path.join(app.config['IMAGES_FOLDER'], image_name)
    if not os.path.exists(image_path) or not os.path.isfile(image_path):
        abort(404)
    return send_file(image_path)


if __name__ == '__main__':
    app.run(debug=True)
