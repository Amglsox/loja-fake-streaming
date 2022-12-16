class KafkaConnection:
    def __init__(self, bootstrap_servers: str, topic_data: str) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.topic_data = topic_data

    def _to_dict(self) -> dict:
        return {"bootstrap_servers": self.bootstrap_servers, "topic_data": self.topic_data}
