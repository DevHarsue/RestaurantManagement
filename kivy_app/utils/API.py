import requests
import json

class API:
    def __init__(self):
        self.host = "https://restaurantmanagmentapi.onrender.com/"
        try:
            with open("config.json", mode="r") as file:
                self.host = json.load(file)["host"]
        except Exception:
            try:
                with open("config.json", mode="w") as file:
                    json.dump({"host": self.host}, file)
            except Exception:
                self.host = "https://restaurantmanagmentapi.onrender.com/"
    
    def cambiar_host(self,host):
        self.host = host
        try:
            with open("config.json", mode="w") as file:
                json.dump({"host": host}, file)
        except Exception:
            self.host = "https://restaurantmanagmentapi.onrender.com/"
    
    def HTTPRequestGET(self,endpoint: str,body: dict={}):
        response = requests.get(self.host + endpoint, json=body)
        if response.status_code==200:
            return response.json()
        return None
    
    def HTTPRequestPOST(self,endpoint: str,body: dict={}):
        response = requests.post(self.host + endpoint, json=body)
        if response.status_code==201:
            return response.json()
        return None
    
    def HTTPRequestPUT(self,endpoint: str,body: dict={}):
        response = requests.put(self.host + endpoint, json=body)
        if response.status_code==200:
            return response.json()
        return None

    def test_host(self) -> dict:
        return self.HTTPRequestGET("")
    
    def get_initial_android(self) -> dict:
        return self.HTTPRequestGET("initial/android")
    def get_platos(self) -> list[dict]:
        return self.HTTPRequestGET('platos')
    def get_tipos_platos(self) -> list[dict]:
        return self.HTTPRequestGET('tipos_platos')
    def get_mesas(self) -> list[dict]:
        return self.HTTPRequestGET('mesas')
    def get_divisas(self) -> list[dict]:
        return self.HTTPRequestGET('divisas')
    def get_mesas_ocupadas(self) -> list[dict]:
        return self.HTTPRequestGET('mesas_ocupadas')
    def get_platos_orden(self,id) -> list[dict]:
        return self.HTTPRequestGET(f"detalles_ordenes_platos/?orden_id={id}")
    
    def post_orden(self) -> dict:
        return self.HTTPRequestPOST('ordenes',body={})
    def post_mesas_ocupadas(self,id,orden_id) -> dict:
        return self.HTTPRequestPOST('mesas_ocupadas',body={"id":id,"orden_id":orden_id})
    def post_detalles_ordenes_platos(self,orden_id,platos):
        return self.HTTPRequestPOST('detalles_ordenes_platos',body={"orden_id":orden_id,"platos":platos})
    
    def put_detalles_ordenes_platos(self,orden_id,plato_id,cantidad):
        return self.HTTPRequestPUT("detalles_ordenes_platos",body={
                                                                    "orden_id":orden_id,
                                                                    "plato_id":plato_id,
                                                                    "cantidad":cantidad
                                                                })

api = API()
