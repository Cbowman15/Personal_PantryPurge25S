from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

recipes = Blueprint('recipes', __name__)

# ------------------------------------------------------------
# POST /recipes - Create and publish a new recipe

@recipes.route('/recipes', methods=['POST'])
def create_recipe():
    # Get the JSON data from the request body
    data = request.json
    
    # Extracting the fields from the request data
    recipe_name = data.get('RecipeName')
    servings = data.get('Servings')
    difficulty = data.get('Difficulty')
    calories = data.get('Calories')
    description = data.get('Description')
    cuisine = data.get('Cuisine')
    prep_time_mins = data.get('PrepTimeMins')
    cook_time_mins = data.get('CookTimeMins')
    publish_date = data.get('PublishDate')
    
    # Validating the required fields (e.g., RecipeName must be present)
    if not recipe_name or not chef_id:
        return jsonify({"error": "RecipeName and chef_id are required."}), 400

    # Optional fields should be handled carefully if missing, so we provide defaults if necessary
    servings = servings if servings is not None else 4
    difficulty = difficulty if difficulty else 'Medium'
    calories = calories if calories is not None else 0
    description = description if description else ''
    cuisine = cuisine if cuisine else 'General'
    prep_time_mins = prep_time_mins if prep_time_mins is not None else 30
    cook_time_mins = cook_time_mins if cook_time_mins is not None else 45
    publish_date = publish_date if publish_date else '2025-01-01'

    try:
        cursor = db.cursor()

        # Insert the recipe into the database with the provided fields
        cursor.execute(
            """
            INSERT INTO recipes (
                RecipeName, Servings, Difficulty, Calories, 
                Description, Cuisine, PrepTimeMins, CookTimeMins, 
                PublishDate
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING RecipeID;
            """,
            (recipe_name, servings, difficulty, calories, description, cuisine, 
             prep_time_mins, cook_time_mins, publish_date)
        )
        
        # Fetch the newly created RecipeID
        new_id = cursor.fetchone()[0]

        db.commit()
        cursor.close()

        # Respond with a success message and the ID of the newly created recipe
        return jsonify({
            "message": "Recipe created successfully.",
            "recipe_id": new_id
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@recipes.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    # Get the incoming JSON data
    data = request.json

    # Extract the fields from the request data
    recipe_name = data.get('RecipeName')
    servings = data.get('Servings')
    difficulty = data.get('Difficulty')
    calories = data.get('Calories')
    description = data.get('Description')
    cuisine = data.get('Cuisine')
    prep_time_mins = data.get('PrepTimeMins')
    cook_time_mins = data.get('CookTimeMins')
    publish_date = data.get('PublishDate')

    # Check if no fields were provided for update
    if not any([recipe_name, servings, difficulty, calories, description, cuisine, prep_time_mins, cook_time_mins, publish_date]):
        return jsonify({"error": "No fields to update"}), 400

    try:
        cursor = db.cursor()

        # Build the SET part of the SQL query dynamically based on provided fields
        fields = []
        values = []
        
        if recipe_name:
            fields.append("RecipeName = %s")
            values.append(recipe_name)
        if servings is not None:
            fields.append("Servings = %s")
            values.append(servings)
        if difficulty:
            fields.append("Difficulty = %s")
            values.append(difficulty)
        if calories is not None:
            fields.append("Calories = %s")
            values.append(calories)
        if description:
            fields.append("Description = %s")
            values.append(description)
        if cuisine:
            fields.append("Cuisine = %s")
            values.append(cuisine)
        if prep_time_mins is not None:
            fields.append("PrepTimeMins = %s")
            values.append(prep_time_mins)
        if cook_time_mins is not None:
            fields.append("CookTimeMins = %s")
            values.append(cook_time_mins)
        if publish_date:
            fields.append("PublishDate = %s")
            values.append(publish_date)

        # Add the recipe_id as the final value for the WHERE clause
        values.append(recipe_id)

        # Dynamically build the SQL UPDATE statement
        sql = f"UPDATE recipes SET {', '.join(fields)} WHERE RecipeID = %s"

        # Execute the update query
        cursor.execute(sql, tuple(values))

        # Commit the changes to the database
        db.commit()
        cursor.close()

        # Return a success response
        return jsonify({"message": "Recipe updated successfully."}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

# This blueprint will handle routes related to Newsletter submissions
newsletter_routes = Blueprint('newsletter_routes', __name__)

# ------------------------------------------------------------
# /newsletter: Post a recipe to be considered for the newsletter
# ------------------------------------------------------------
# /recipes/<id>/newsletter: Submit a recipe for the newsletter

@recipe_routes.route('/recipes/<int:recipe_id>/newsletter', methods=['POST'])
def submit_recipe_for_newsletter(recipe_id):
    # Get the incoming JSON data
    data = request.json

    # Extracting the ChefID and SubStatus from the request data
    chef_id = data.get('ChefID')
    sub_status = data.get('SubStatus', 'Pending')  # Default status is 'Pending'
    sub_date = datetime.now()  # Set the current time for submission date

    # Validation: Ensure ChefID is provided
    if not chef_id:
        return jsonify({"error": "ChefID is required."}), 400

    try:
        cursor = db.cursor()

        # Insert the recipe submission into the Newsletter table
        cursor.execute(
            """
            INSERT INTO Newsletter (ChefID, RecipeID, SubStatus, SubDate)
            VALUES (%s, %s, %s, %s)
            RETURNING SubID;
            """,
            (chef_id, recipe_id, sub_status, sub_date)
        )

        # Fetch the newly created SubID
        sub_id = cursor.fetchone()[0]

        # Commit the changes to the database
        db.commit()
        cursor.close()

        # Return a success message along with the SubID of the submission
        return jsonify({
            "message": "Recipe submission to newsletter successful.",
            "SubID": sub_id,
            "ChefID": chef_id,
            "RecipeID": recipe_id,
            "SubStatus": sub_status,
            "SubDate": sub_date
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500