import json
import logging
import random
import uuid

from datetime import date
from datetime import datetime
from hashlib import sha256

from data.products_market import list_products
from faker import Faker
from kafka import KafkaProducer
from kafka_components.kafka_connection import KafkaConnection


class Producer(KafkaConnection):
    def run(self) -> str:
        """Summary line, max. 79 chars including period** Do something interesting."""

        producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

        valor = Producer.create_vendas()
        logging.info(f"Person {valor}")
        producer.send(self.topic_data, valor)
        logging.info("Person created")
        return valor

    def create_vendas() -> str:
        """Summary line, max. 79 chars including period** Do something interesting."""

        idRandomCompra = sha256(
            (str(uuid.uuid4()) + datetime.now().strftime("%Y-%m-%d %H:%m:%s")).encode("utf-8")
        ).hexdigest()
        fake = Faker("pt_BR")
        person = fake.profile()
        start_date = date(year=2019, month=1, day=1)

        seriesProdutos = random.choice(list_products)
        person = {
            "nome": person["name"],
            "dtNascimento": person["birthdate"].strftime("%Y-%m-%d"),
            "empresa": person["company"],
            "profissao": person["job"],
            "cpf": person["ssn"],
            "enderecoCompleto": person["residence"].replace("\n", " "),
            "logradouro": person["residence"].split("\n")[0],
            "bairro": person["residence"].split("\n")[1],
            "cep": person["residence"].split("\n")[2][:8],
            "cidade": person["residence"].split("\n")[2][9:].split("/")[0].strip(),
            "estado": person["residence"].split("\n")[2][9:].split("/")[1].strip(),
            "idCompra": str(idRandomCompra),
            "idProduto": int(seriesProdutos["id"]),
            "produtoDescricao": seriesProdutos["produto"],
            "qtCompra": int(random.choice(range(1, 6))),
            "dtCompra": fake.date_between(start_date=start_date, end_date=datetime.now()).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "precoUnitario": round(seriesProdutos["precoUnit"], 2) / 10,
            "pais": "Brasil",
        }

        return person
