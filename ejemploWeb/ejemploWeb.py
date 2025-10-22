import json
import requests
from flask import Flask, jsonify, request, Response, render_template, redirect

app = Flask(__name__)

secuencia_id=4;
@app.route('/',methods=['GET'])
def index():
  url_api = "http://localhost:5001/frutas"
  try:
       respuesta = requests.get(url_api)
       respuesta.raise_for_status() # Lanza una excepción si hay un error HTTP
       lista_frutas = respuesta.json()
       return render_template("index.html",mensaje="FRUTAS",lista_f=lista_frutas)     
  except requests.exceptions.RequestException as e:
       return jsonify({"error": str(e)}), 500 
       
  
@app.route('/inicializar',methods=['GET'])
def inicializar():
 url_api = "http://localhost:5001/inicializar"
 respuesta = requests.delete(url_api)
 return jsonify(respuesta.json())
 #render_template("index.html",mensaje="FRUTAS",lista_f=lista_frutas)


@app.route('/agregar', methods=["GET", "POST"])
def mostrar_formulario():
   global secuencia_id,lista_frutas
  
   if request.method == 'POST':
        nombre = request.form['nombre']
        secuencia_id+=1
        nueva_fruta={"id":secuencia_id,"nombre":nombre}
        url_api = "http://localhost:5001/mongodb/frutas"
        #lista_frutas.append(nueva_fruta)
        #print(lista_frutas)
        requests.post(url_api,json=nueva_fruta)
        #if next:
            #return redirect(next)
        return redirect("/")
        
   return render_template("formulario.html")


if __name__ == '__main__':
    app.run(debug=True)
