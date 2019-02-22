# -*- coding: utf-8 -*-
# 必要なモジュールの読み込み
from flask import Flask, jsonify,make_response,request,render_template
from gevent import pywsgi
import gevent
from geventwebsocket.handler import WebSocketHandler
from flask_sockets import Sockets
from gevent.event import AsyncResult
from time import sleep
import requests
import json
import random
#event処理の設定
message = AsyncResult()
# __name__は現在のファイルのモジュール名
app = Flask(__name__)
sockets = Sockets(app)
#context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context.load_cert_chain('cert.crt','server.pass.key')
#reqの初期化
@app.route('/')
def index():
	return render_template('index1.html')
@app.route('/shenron',methods=['POST'])
def post():
	i = random.randint(1,3)
	i = str(i)
	req = request.json['queryResult']['parameters']['Target']
	#characterの分岐
	if req == 'character':
		custom = request.json['queryResult']['parameters']['Custom']
		color = request.json['queryResult']['parameters']['Color']
		cascol = req+','+custom+','+color
		# massage.get()
		message.set(cascol)
		gevent.sleep(0)
		result = jsonify({"fulfillmentText": '<speak><audio src = "https://gsya-80fd3.firebaseapp.com/'+i+'.wav"/><sub alias="">test</sub></speak>'})
		return make_response(result)
	elif req == 'game':
		ans = request.json['queryResult']['parameters']['num']
		if ans == "":
			data=requests.get('https://us-central1-dungeon-3317e.cloudfunctions.net/quizResponchi?text=game')
			result = jsonify({"fulfillmentText": '<speak><audio src = "https://gsya-80fd3.firebaseapp.com/'+i+'.wav"/><sub alias="">'+data.text+'</sub></speak>'})
			return make_response(result)
		else :
			data=requests.get('https://us-central1-dungeon-3317e.cloudfunctions.net/quizResponchi?text='+ans)
			dataArray=data.text.split(',')
			#画面に表示するデータ
			text=dataArray[0]
			#判定処理に使うデータ
			judge=dataArray[1]
			gamereq= req+','+judge
			message.set(gamereq)
			gevent.sleep(0)
			if judge == "true":
				result = jsonify({"fulfillmentText": '<speak><audio src = "https://gsya-80fd3.firebaseapp.com/game_true.wav"/><sub alias="">'+text+'</sub></speak>'})
				return make_response(result)
			else:
				result = jsonify({"fulfillmentText": '<speak><audio src = "https://gsya-80fd3.firebaseapp.com/game_false.wav"/><sub alias="">'+text+'</sub></speak>'})
			return make_response(result)
	elif req == 'lifehack':
		material = request.json['queryResult']['parameters']['material']
		data = requests.get('https://script.google.com/macros/s/AKfycbyQfg85J9SR2KwH6yHOA4xrflDIy8LB5a313Fal-my7WgxjZw/exec?text='+material)
		#一度dict型に変換し、stringに変換
		data=data.json()
		title = data["title"]
		url = data["url"]
		img = data["img"]
		result = jsonify({"fulfillmentText": '<speak><audio src = "https://gsya-80fd3.firebaseapp.com/'+i+'.wav"/><sub alias="">'+'料理名は'+title+'urlは'+url+'だよ！'+'</sub></speak>'})
		return make_response(result)
	elif req == 'greeting':
		message.set(req)
		gevent.sleep(0)
		sleep(2)
		result = jsonify({"fulfillmentText": '<speak><audio src = "https://gsya-80fd3.firebaseapp.com/greeting.wav"/><sub alias="">test</sub></speak>'})
		return make_response(result)
	elif req == 'jump':
		message.set(req)
		gevent.sleep(0)
		result = jsonify({"fulfillmentText": '<speak><audio src = "https://gsya-80fd3.firebaseapp.com/'+i+'.wav"/><sub alias="">test</sub></speak>'})
		return make_response(result)
	elif req == 'action':
		message.set(req)
		gevent.sleep(0)
		result = jsonify({"fulfillmentText": '<speak><audio src = "https://gsya-80fd3.firebaseapp.com/'+i+'.wav"/><sub alias="">test</sub></speak>'})
		return make_response(result)
	else:
		gevent.sleep(0)
		result = jsonify({"fulfillmentText": '<speak><audio src = "https://gsya-80fd3.firebaseapp.com/'+i+'.wav"/><sub alias="">ok</sub></speak>'})
		return make_response(result)
#websocket側
@sockets.route('/shenron')
def ws(ws):
	if request.environ.get('wsgi.websocket'):
		ws = request.environ['wsgi.websocket']
		while True:
			gevent.sleep(0)
			ms=message.get()
			if ms is not None:
				print("ms:"+ms)
				ws.send(ms)
				message.set()
			else:
				ws.receive()
		return ''
		#return render_template('index.html')
	# エラーハンドリングi
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

def main():
	app.debug = True
	server = pywsgi.WSGIServer(("0.0.0.0",8000), app,handler_class=WebSocketHandler)
	server.serve_forever()

gevent.joinall([
	gevent.spawn(post),
	gevent.spawn(ws),
	])
if __name__ == "__main__":
    main()
