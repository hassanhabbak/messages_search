# Helper function for showing errors
def handleServerError(error, code):
    message = {
            'status': code,
            'message': 'Error: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = code

    return resp
