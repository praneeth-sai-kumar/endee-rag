from endee import Endee, Precision


class EndeeVectorStore:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.client = Endee()
        self.client.set_base_url(f"{base_url}/api/v1")

    def create_index(self, name: str, dim: int):
        self.client.create_index(
            name=name,
            dimension=dim,
            space_type="cosine",
            precision=Precision.INT8D
        )

    def get_index(self, name: str):
        return self.client.get_index(name)

    def list_indexes(self):
        return self.client.list_indexes()
