from dataclasses import dataclass
from enum import Enum, auto, IntEnum


class HTTP_METHODS(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()


class HTTP_CODES(IntEnum):
    GET_OK = 200
    CREATED = 201
    NOT_FOUND = 404
    BAD_REQUEST = 400


@dataclass
class HttpResp:
    code: int
    data: dict


class FakeServer:

    def __init__(self):
        self.__next_id = 3
        self.db = {"users": [{"id": 1, "name": "Jan"},
                              {"id": 2, "name": "Anna"}]}

    def handle_request(self, request: dict):
        method = request['method']
        if method == HTTP_METHODS.GET:
            return self.__get(request)
        elif method == HTTP_METHODS.POST:
            return self.__post(request)
        else:
            return HttpResp(HTTP_CODES.NOT_FOUND, {})

    def __get(self, request: dict):
        p: str = request['path']

        if p == '/users':
            return HttpResp(HTTP_CODES.GET_OK, {'users': self.db['users']})

        if p.startswith('/users/'):
            try:
                user_id = int(p.split('/')[-1])
                user = self.__db_user_by_id(user_id)
                return HttpResp(HTTP_CODES.GET_OK, user)
            except ValueError:
                return HttpResp(HTTP_CODES.BAD_REQUEST, {"error": "Nieprawidłowe ID"})
            except StopIteration:
                return HttpResp(HTTP_CODES.NOT_FOUND, {})

        return HttpResp(HTTP_CODES.NOT_FOUND, {})

    def __post(self, request: dict):
        p: str = request['path']
        if p == '/users':
            nuser = self.__db_user_create(request['data']['name'])
            return HttpResp(HTTP_CODES.CREATED, nuser)
        return HttpResp(HTTP_CODES.NOT_FOUND, {})

    def __db_user_create(self, name: str):
        nuser = {'id': self.__next_id, 'name': name}
        self.db['users'].append(nuser)
        self.__next_id += 1
        return nuser

    def __db_user_by_id(self, id: int):
        for user in self.db['users']:
            if user['id'] == id:
                return user
        raise StopIteration


class FakeClient:
    def send(self, server, request):
        print(f"\n>>> Wysyłam: {request['method'].name} {request['path']}")
        odpowiedz = server.handle_request(request)
        print(f"<<< Status: {odpowiedz.code}")
        print(f"<<< Body: {odpowiedz.data}")
        return odpowiedz


# Testy
serwer = FakeServer()
klient = FakeClient()

# Test 1 – pobranie wszystkich użytkowników
klient.send(serwer, {"method": HTTP_METHODS.GET, "path": "/users"})

# Test 2 – pobranie użytkownika po ID
klient.send(serwer, {"method": HTTP_METHODS.GET, "path": "/users/1"})

# Test 3 – dodanie nowego użytkownika
klient.send(serwer, {"method": HTTP_METHODS.POST, "path": "/users", "data": {"name": "Ewelina"}})

# Test 4 – nieistniejący zasób
klient.send(serwer, {"method": HTTP_METHODS.GET, "path": "/products"})

# Test 5 – nieprawidłowe ID
klient.send(serwer, {"method": HTTP_METHODS.GET, "path": "/users/abc"}) 