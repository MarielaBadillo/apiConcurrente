import datetime
import asyncio
import uvloop
from sanic import app
from sanic import Sanic
from sanic.response import json
from motor.motor_asyncio import AsyncIOMotorClient

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = Sanic("MoradoConcurrente")

#Leer los datos de la bd
@app.route('/leer', methods=['GET'])
async def leer(request):
	mongo_connection = AsyncIOMotorClient('localhost', 27017, io_loop=app.loop)['api']
	contacts = mongo_connection.api.datosard
	data = await contacts.find().to_list(20)
	lista = []
	for x in data:
		x['id'] = str(x['_id'])
		del x['_id']
		x['hora']=x['hora'].strftime('%H:%M:%S.%f')
		lista.append(x)
	return json(lista)

@app.route('/agregaruno', methods=['GET'])
async def agregaruno(request):
	mongo_connection = AsyncIOMotorClient('localhost', 27017, io_loop=app.loop)['api']
	contacts = mongo_connection.api.datosard
	insert = await contacts.insert_one({'nombre': 'juan_sensor', 'estado':'chido(der)', 'hora':datetime.datetime.now()})
	return json({"inserted_id": str(insert.inserted_id)})
	
@app.route('/framework', methods=['GET'])
async def metodoConcurrente(request):
	#En esta parte se recaban los datos del arduino
	mongo_connection = AsyncIOMotorClient('localhost', 27017, io_loop=app.loop)['api']
	contacts = mongo_connection.api.datosard 
	#nombre = request.json["nombre"]
	#estado = request.json["estado"]
	#en esta parte se determina la hora
	#chora = datetime.datetime.now()
	#hora = chora.strftime('%H:%M:%S.%f')
	output = {'nombre' : 'cola_raton', 'estado' : 'centro', 'hora':datetime.datetime.now()}
	#return json(output)
	#object_id = await app.mongo['api']["datosard"].save(doc)
	#return json({'object_id': str(object_id)})
	insert = await contacts.insert_one(output)
	return json({"inserted_id": str(insert.inserted_id)})
	#desplegado de info
	
#Leer datos por nombre de dispositivo(incluido en json arduino)


@app.route('/framework/<nombre>', methods=['GET'])
async def get_one_framework(nombre):
	mongo_connection = AsyncIOMotorClient('localhost', 27017, io_loop=app.loop)['api']
	contacts = mongo_connection.api.datosard
	framework = mongo.db.framework
	q = framework.find_one({'nombre' : nombre})
	if q:
		output = {'nombre' : q['nombre'], 'estado' : q['estado'], 'hora':q['hora']}
	else:
		output = 'No results found'

	return json({'result' : output})


loop = asyncio.get_event_loop()

app.run(host="0.0.0.0", port=8000, workers=50)

#server = app.create_server(host="0.0.0.0", port=8000)
#loop = asyncio.get_event_loop()
#task = asyncio.ensure_future(server)
#loop.run_forever()
"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
"""

"""
@app.route("/new")
async def new(request):
    contact = request.json
    insert = await contacts.insert_one(contact)
    return json({"inserted_id": str(insert.inserted_id)})

async def new(request):
    doc = request.json
    print(type(app.mongo['test']))
    object_id = await app.mongo['test']["test_col"].save(doc)
    return json({'object_id': str(object_id)})

#Leer los datos de la bd
@app.route('/leer', methods=['GET'])
async def leer_datos():
    framework = mongo.db.framework 

    output = []

    for q in framework.find():
        output.append({'hora' : q['hora'], 'estado' : q['estado']})

    return jsonify({'result' : output})
"""
