#!/usr/bin/env python3
######################
# S.CAPS Dec 2021
# OCP-ECHO-DEMO
######################

TEST = False

from flask import Flask, render_template, request, jsonify, copy_current_request_context
from expiringdict import ExpiringDict
import os, json, datetime, copy

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

svc_list = []
env_list = ["dev", "test", "integration", "production"]

cache = ExpiringDict(max_len=512, max_age_seconds=3600)

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/', methods=['GET'])
def index():
    return jsonify({ "status": "ok", "cached-data": cache } )

@app.route('/health', methods=['GET']) 
def health():
    return jsonify( { "status": "ok", "message": "I'm alive !" } )

@app.route('/api/version', methods=['GET']) 
def get_version():
    global svc_list, env_list
    svc_list_version = {}
    for svc in svc_list:
        svc_list_version[svc] = {}

        for env in env_list:
            _id = "svc_{0}/env_{1}".format(svc, env)
            if _id in cache and cache[_id] != None:
                svc_list_version[svc][env] = copy.copy(cache[_id])
            else:
                svc_list_version[svc][env] = 'NoVersion'
    
    return jsonify( { "version": svc_list_version } )

@app.route('/api/version', methods=['UPDATE','POST'])
def set_version():
    global cache, svc_list, env_list
    if request.headers['Content-Type'].find('application/json') <= -1:
        return jsonify( { "status": False , "message": "json header missing" } ), 400

    service_name     = request.json['service'].strip()
    environment_name = request.json['environment'].strip()
    version_data     = request.json['version'].strip()
   
    if not service_name in svc_list:
        app.logger.info("Discovered new service name {0}".format(service_name))
        svc_list.append(service_name)

    if not environment_name in env_list:
        app.logger.info("Discovered new environment name {0}".format(environment_name))
        env_list.append(environment_name)

    id = "svc_{0}/env_{1}".format(service_name, environment_name)
    
    cache[id] = version_data

    return jsonify({ "status": True, "message": "Thanks for the update" })

@app.route('/api/cache', methods=['DELETE'])
@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    global cache
    cache.clear()
    return jsonify( { "status": True, "message": "cache cleared" } )

@app.route('/api/service/add', methods=['POST'])
def add_service():
    global svc_list
    if request.headers['Content-Type'].find('application/json') <= -1:
        return jsonify( { "status": False , "message": "json header missing" } ), 400

    service_name     = request.json['service'].strip()

    if not service_name in svc_list:
        app.logger.info("Discovered new service name {0}".format(service_name))
        svc_list.append(service_name)

    return jsonify( { "status": True, "message": "Service added" } )

@app.route('/api/service', methods=['DELETE'])
@app.route('/api/service/clear', methods=['POST'])
def reset_service():
    global svc_list
    svc_list = []
    return jsonify( { "status": True, "message": "Service list cleared" } )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("8080"), debug=TEST)