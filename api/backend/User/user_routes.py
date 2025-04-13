from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
users = Blueprint('user', __name__)


# Get all the products from the database, package them up,
# and return them to the client
@user_accounts.route('/user_accounts', methods=['GET'])
def get_all_users():

    cursor = db.get_db().cursor()
    
    query = '''
        SELECT  userid, 
                username, 
                datecreated, 
                UserStatus  
        FROM User
    '''
    
    # Same process as above
    
    cursor.execute(query)
    theData = cursor.fetchall()

    
    response = make_response(theData)
    response.mimetype = 'application/json'
    response.status_code = 200
    return response
    

# Update customer info for customer with particular userID
#   Notice the manner of constructing the query.
@user_accounts.route('/user_accounts', methods=['PUT'])
def update_user():
    current_app.logger.info('PUT /user route')
    cust_info = request.json
    cust_id = cust_info['id']
    username = cust_info['username']
    created = cust_info['datecreated']
    Status = cust_info['userstatus']

    query = 'UPDATE customers SET username = %s, datecreated = %s, userstatus = %s where id = %s'
    data = (username, created,Status)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'user updated'
