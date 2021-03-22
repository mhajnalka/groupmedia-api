
from flask import request, jsonify, Blueprint


def get_employee():
    return jsonify(message="anyad"), 200