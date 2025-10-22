import json
from flask import Flask, jsonify, request, Response
from bson.json_util import dumps, loads
#Conectarse a la base de datos MongoDB
from pymongo import MongoClient

# 1. Crear una instancia de Flask
app = Flask(__name__)




# Datos de ejemplo en memoria (se podrían usar bases de datos)
items = [
    {"id": 1, "nombre": "Manzana"},
    {"id": 2, "nombre": "Banana"},
    {"id": 3, "nombre": "Sandía"},
    {"id": 4, "nombre": "Melón"}
]

client = MongoClient("mongodb://localhost:27017/")
db = client['bd_frutas']
lista_frutas = db['frutas']
#insert_result = lista_frutas.insert_many(items)
#carga_inicial();
# 2. Definir una ruta para obtener todos los items (GET)
@app.route('/frutas', methods=['GET'])
def get_futas():
    l=list(lista_frutas.find())
    return Response(dumps(l), mimetype='application/json')

# 3. Definir una ruta para obtener un item por ID (GET)
@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    for item in items:
        if item['id'] == id:
            return jsonify(item)
    return jsonify({"mensaje": "Item no encontrado"}), 404

# 4. Definir una ruta para crear un nuevo item (POST)
@app.route('/items', methods=['POST'])
def create_item():
    nuevo_item_data = request.json
    nuevo_id = items[-1]['id'] + 1 if items else 1 # Generar un nuevo ID
    nuevo_item = {"id": nuevo_id, "nombre": nuevo_item_data['nombre']}
    items.append(nuevo_item)
    return jsonify(nuevo_item), 201 # 201 es el código para creado

@app.route('/mongodb/frutas', methods=['POST'])
def create_item1():
    nueva_fruta= request.json
    lista_frutas.insert_one(nueva_fruta)
    return jsonify({'salida':'fruta_insetada'}), 201#jsonify(nueva_fruta), 201 # 201 es el código para creado

# 5. Definir una ruta para actualizar un item (PUT)
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    actualizar_data = request.json
    for item in items:
        if item['id'] == id:
            item['nombre'] = actualizar_data['nombre']
            return jsonify(item)
    return jsonify({"mensaje": "Item no encontrado"}), 404

# 6. Definir una ruta para eliminar un item (DELETE)
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    global items # Para poder modificar la lista global
    items = [item for item in items if item['id'] != id]
    return jsonify({"mensaje": "Item eliminado"})
    
 #x = lista_frutas.delete_many ( { } )  BORRA TODAS LAS FRUTAS
 #x.deleted_count     NUMERO DE DATOS BORRADOS
 
@app.route('/inicializar', methods=['DELETE'])
def delete_todo():
    global items # Para poder modificar la lista global
    lista_frutas.delete_many ( { } )
    lista_frutas.insert_many(items)
    return jsonify({"mensaje": "Base inicializada"})
 
 
@app.route('/mongodb/frutas/<int:id>', methods=['DELETE'])
def delete_fruta(id):
    myquery={"id":id}
    lista_frutas.delete_one(myquery)
     
    return jsonify({"mensaje": "fruta eliminada"})

@app.route('/mongodb/frutas', methods=['PUT'])
def update_fruta():
  actualizar_data = request.json
  nuevos_datos={"$set":{"nombre":"otra cosa"}}
  lista_frutas.update_one(actualizar_data,nuevos_datos)
  return jsonify({"mensaje": "fruta actualizada"})



# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
