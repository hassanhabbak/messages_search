from flask import Flask, url_for, request, json, Response, jsonify
from jsonschema import validate
import jsonschema
import sys
import json
import messages_handler
import message_schema as m_schema
import urllib
app = Flask(__name__)


mh = messages_handler.MessagesHandler()

# Entry point for requests
@app.route('/messages', methods = ['POST', 'GET'])
def api_message():

    if request.method == 'GET':
        return message_get()
    elif request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        return message_post(request.json)
    else:
        return handle_not_found()

# Handle Get requests for the API
def message_get():

    recipient, originator, message_contains = None, None, None

    if 'recipient' in request.args:
        recipient = int(request.args['recipient'])
    if 'originator' in request.args:
        originator = str(request.args['originator'])
    if 'message_contains' in request.args:
        message_contains = urllib.parse.unquote(str(request.args['message_contains'])).split()

    return jsonify(mh.search(recipient=recipient, originator=originator, content_contains=message_contains))

# Handles and Validates Post request for API
def message_post(post_json):

    try:
        validate(post_json, m_schema.MESSAGE_SCHEMA)
    except jsonschema.exceptions.ValidationError as ve:
        print("Record #{}: ERROR\n".format(post_json))
        print(str(ve) + "\n")
        return handleServerError(str(ve), 400)
    mh.insert(post_json)
    message = {
            'status': 200,
            'message': 'Message Inserted'
    }
    resp = jsonify(message)
    return resp

# Helper function for handling 404
@app.errorhandler(404)
def handle_not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

# Helper function for showing errors
def handleServerError(error, code):
    message = {
            'status': code,
            'message': 'Error: ' + error,
    }
    resp = jsonify(message)
    resp.status_code = code

    return resp

if __name__ == '__main__':

    app.run()
