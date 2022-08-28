from fastapi import APIRouter
from features.users import users_controller, users_service
from typing import Any


USERS_ROUTER = APIRouter()

USERS_ROUTER.add_api_route(path="/me",
                            methods=["GET"],
                            endpoint=users_controller.get_current_user,
                            tags=["Users"],
                            response_model=users_service.UserOutDB
                        )
""" USERS_ROUTER.add_api_route(path="/{id}",
                            methods=["GET"],
                            endpoint=users_controller.get_user_by_id,
                            tags=None,
                            response_model=users_service.UserOutDB
                        )    """                         