import requests
import json

class API:
    def __init__(self):
        self.host = "https://restaurantmanagmentapi.onrender.com/"
        self.token = None
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
            with open("config.json", mode="r+") as file:
                data = json.load(file)
                data["host"] = host
                file.seek(0)
                json.dump(data, file)
                file.truncate()
        except Exception:
            self.host = "https://restaurantmanagmentapi.onrender.com/"
    
    def detectar_token(self):
        try:
            with open("config.json", mode="r") as file:
                self.token = json.load(file).get("token")
                if self.token:
                    return True
        except Exception as e:
            print(e)
            self.token = None
        
        return False

    def borrar_token(self):
        try:
            with open("config.json", mode="r+") as file:
                data = json.load(file)
                data = {"host":data["host"]}
                file.seek(0)
                json.dump(data, file)
                file.truncate()
        except Exception:
            pass
    
    def login(self,usuario,contraseña):
        response = requests.post(self.host + "token",data={"username":usuario,"password":contraseña})
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            try:
                with open("config.json", mode="r+") as file:
                    data = json.load(file)
                    data["token"] = self.token
                    file.seek(0)
                    json.dump(data, file)
                    file.truncate()
                    return True
            except Exception as e:
                print(e)
        return False
    
    def HTTPRequestGET(self,endpoint: str,body: dict={}):
        response = requests.get(self.host + endpoint, json=body,headers={"Authorization": f"Bearer {self.token}"})
        print(response.status_code)
        if response.status_code==200:
            return response.json()
        return None
    
    def HTTPRequestPOST(self,endpoint: str,body: dict={}):
        response = requests.post(self.host + endpoint, json=body,headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code==201:
            return response.json()
        return None
    
    def HTTPRequestPUT(self,endpoint: str,body: dict={}):
        response = requests.put(self.host + endpoint, json=body,headers={"Authorization": f"Bearer {self.token}"})
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