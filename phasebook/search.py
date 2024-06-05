from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200

def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters, sorted by ID
    """

    users = []

    if 'id' in args:
        user_id = next((user for user in USERS if user['id'] == args['id']), None)
        if user_id:
            users.append(user_id)

    if 'name' in args:
        user_name = args['name'].lower()
        users.extend(user for user in USERS if user_name in user['name'].lower())

    if 'age' in args:
        try:
            user_age = int(args['age'])
            users.extend(user for user in USERS if user['age'] in range(user_age - 1, user_age + 2))
        except ValueError:
            pass 

    if 'occupation' in args:
        user_occupation = args['occupation'].lower()
        users.extend(user for user in USERS if user_occupation in user['occupation'].lower())

    priority_users = {user['id']: user for user in users}.values()

    return list(priority_users)
