import json
import logging
import os

from flask import Blueprint
from flask import Response
from kafka_components.producer import Producer


routes = Blueprint("routes", __name__, url_prefix="/")


@routes.route("/", methods=["GET"])
@routes.route("/healthcheck", methods=["GET"])
def healthcheck() -> Response:
    logging.info("Start healthcheck")
    return Response(json.dumps({"Status": "running"}), status=200, mimetype="application/json")


@routes.route("/shopping/create", methods=["GET", "POST"])
def push_data_assets_create() -> Response:
    logging.info("Start create venda")
    venda = Producer(os.environ["bootstrap_servers"], os.environ["topic_data"]).run()
    return Response(json.dumps({"data": {"Status": "ok", "venda": venda}}), status=200, mimetype="application/json")
