from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
users = Blueprint('users', __name__)


# Get all the products from the database, package them up,
# and return them to the client
@users.route('/users', methods=['GET'])
def get_all_users():
    
    query = '''
        SELECT  userid, 
                username, 
                datecreated, 
                UserStatus,  
        FROM User
    '''
    
    # Same process as above
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response
