# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
import uuid

from flask import Blueprint, render_template, request, jsonify, current_app
from flask_assistant import ApiAi
from robo_analyst.assistant.webhook import assist


blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Landing page for the web/html blueprint"""
    return render_template('index.html')


@blueprint.route('/send_query', methods=['POST'])
def send_query():

    sessionID = request.headers.get("sessionID")

    if sessionID is None:  # maybe have header ids set if initalMessage below
        sessionID = str(uuid.uuid4())

    data = request.json
    query = data['messageData']['text']
    api_json = send_to_api(query, sessionID)
    print(api_json)

    return create_response(api_json, sessionID=sessionID)


def create_response(message_payload, **headers):
    response = jsonify(message_payload)
    for k, v in headers.items():
        response.headers[k] = v

    if 'sessionID' not in response.headers:
        current_app.logger.warn(
            'No sessionID with response, creating new session')
        request.headers['sessionID'] = str(uuid.uuid4())

    return response


def send_to_api(query_text, sessionID):
    api_json = ApiAi().post_query(query_text, sessionID)
    return api_json
