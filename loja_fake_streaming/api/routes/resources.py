import json
import logging

from flask import Blueprint
from flask import Response


routes = Blueprint("webhook", __name__, url_prefix="/")


@routes.route("/", methods=["GET"])
@routes.route("/healthcheck", methods=["GET"])
def healthcheck() -> Response:
    logging.info("Start healthcheck")
    return Response(json.dumps({"Status": "running"}), status=200, mimetype="application/json")


@routes.route("/shopping/create", methods=["GET", "POST"])
def push_data_assets_create() -> Response:
    logging.info("Start create venda")
    return Response(json.dumps({"Status": "ok"}), status=200, mimetype="application/json")
