from flask import Blueprint
from flask import request

# from app.db import get_db

bp = Blueprint('request', __name__)

# GET /forecast?id=xxxx


@bp.route('/forecast', methods=['GET'])
def forecast():
    id = request.args['id']
    return id
