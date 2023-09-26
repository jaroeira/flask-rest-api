from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import abort
import logging

def save_db_item(item, db):
    try:
        db.session.add(item)
        db.session.commit()
    except SQLAlchemyError as e:
        logging.error(msg=f"save_db_item error: {e}")
        abort(500, message="An error occurred.")


def delete_db_item(item, db):
    try:
        db.session.delete(item)
        db.session.commit()
    except SQLAlchemyError as e:
        logging.error(msg=f"delete_db_item error: {e}")
        abort(500, message="An error occurred.")