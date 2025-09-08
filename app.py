from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

#criar uma instancia do Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db' #configurar o banco de dados
db = SQLAlchemy(app) #criar uma instancia do SQLAlchemy
CORS(app) #habilitar CORS

#modelagem de dados
#Produto(id, nome, preco, descricao)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

#rotas
@app.route('/api/products/add', methods=['POST'])
def add_product():
    #lógica para adicionar um produto ao banco de dados
    data = request.json
    if "name" in data and "price" in data:
        product = Product(name=data['name'], price=data['price'], description=data.get('description',""))
        db.session.add(product)
        db.session.commit()
        return {'message': 'Produto adicionado com sucesso!'}
    return jsonify({'message': 'Dados inválidos!'}), 400

@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    #lógica para deletar um produto do banco de dados
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Produto deletado com sucesso!'}
    return jsonify({'message': 'Produto não encontrado!'}), 404

@app.route("/api/products/<int:product_id>", methods=['GET'])
def get_product_details(product_id):
    #lógica para obter os detalhes de um produto
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description
        })
    return jsonify({'message': 'Produto não encontrado!'}), 404

@app.route('/api/products/update/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    #lógica para atualizar os detalhes de um produto
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Produto não encontrado!'}), 404

    data = request.json
    if "name" in data:
        product.name = data['name']
    if "price" in data:
        product.price = data['price']
    if "description" in data:
        product.description = data['description']

    db.session.commit()
    return jsonify({'message': 'Produto atualizado com sucesso!'})

@app.route("/api/products", methods=['GET'])
def get_products():
    #lógica para listar todos os produtos
    products = Product.query.all()
    products_list = []
    for product in products:
        products_data = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        } 
        products_list.append(products_data)
    return jsonify(products_list)

#definir uma rota raiz da pagina inicial e a função que sera executada ao executar
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True) #debug=True não utilizar em produção

