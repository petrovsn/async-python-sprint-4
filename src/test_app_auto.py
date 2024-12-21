from fastapi.testclient import TestClient
#from db.create import create_table
#чистим базу данных

# Импортируем сюда переменную приложения app, инициализированную в файле app.py
from main import app
import pytest
import time

#при запуске НЕ в режиме отладки возвращает ошибку
#The python test process was terminated before it could exit on its own, the process errored with: Code: 4294967295, Signal: null
#вопрос: почему?

client = TestClient(app)

class UrlShortGenApi:
    def create_user(login, password):
        #with TestClient(app) as client
            response = client.post('/users/create', json={
                                                "login": login,
                                                "password": password
                                                })
            return response
    
    def create_short_url(url, type = "public", login = None, password = None):
        #with TestClient(app) as client:
            response = client.post('/', 
                                json = {
                                    "url_full":url,
                                    "type": type
                                },
                                headers={
                                                "login": login,
                                                "password": password
                                                })
            return response
    
    def create_short_url_batch(urls, type = "public", login = None, password = None):
        #with TestClient(app) as client:
            response = client.post('/shorten', 
                                json = [{
                                    "url_full":url,
                                    "type": type
                                } for url in urls],
                                headers={
                                                "login": login,
                                                "password": password
                                    })
            return response
    
    def get_redirection(url_short):
        #with TestClient(app) as client:
            response = client.get(f"/{url_short}")
            return response
        
    def delete_url(url_short):
        #with TestClient(app) as client:
            response = client.delete(f"/{url_short}")
            return response
        
    def get_status_url(url_short):
        #with TestClient(app) as client:
            response = client.get(f"/{url_short}/info")
            return response
        
    def put_short_url(url_short, new_attrs, login = None, password = None):
        #with TestClient(app) as client:
            response = client.put(f"/{url_short}", json=new_attrs, headers={
                                                "login": login,
                                                "password": password
                                    })
            return response
    def ping_db():
        #with TestClient(app) as client:
            response = client.get("utils/ping")
            return response


#тестовый эндпойнт, предназначенный для проверки того, 
def test_testok():
    #with TestClient(app) as client:
        response = client.get('/test/ep') 
        return response


import random
def test_create_user():
    
    username = "user_"+str(random.randint(10,9999999999))
    response = UrlShortGenApi.create_user(username, "password")
    assert response.status_code == 200
    assert response.json()["login"] == username
    assert response.json()["password"] == "password"

def test_create_short_url():
    token = str(random.randint(10,9999999999)) 
    link = "http://ya.ru/"+token
    response = UrlShortGenApi.create_short_url(link)
    assert response.status_code == 201
    assert response.json()["url_full"] == link

def test_create_short_url_private():

    username = "user_"+str(random.randint(10,9999999999))
    password = "password"
    response = UrlShortGenApi.create_user(username,password )
    assert response.status_code == 200

    token = str(random.randint(10,9999999999)) 
    link = "http://ya.ru/"+token
    response = UrlShortGenApi.create_short_url(link, type = "private", login= username, password= password)
    assert response.status_code == 201
    assert response.json()["url_full"] == link


def test_create_short_url_batch():
    token = str(random.randint(10,9999999999)) 
    tested_urls_core = ["www.ya.ru", "www.google.com", "www.youtube.com"]
    tested_urls = [url+"/"+token for url in tested_urls_core]
    response = UrlShortGenApi.create_short_url_batch(tested_urls)
    assert response.status_code == 201
    created_data = [a["url_full"] for a in response.json()]
    for url in tested_urls:
        assert url in created_data


def test_get_redirected_url():
    token = str(random.randint(10,9999999999)) 
    link = "http://ya.ru/"+token
    response = UrlShortGenApi.create_short_url(link)
    assert response.status_code == 201
    assert response.json()["url_full"] == link
    url_short = response.json()["url_short"]
    response = UrlShortGenApi.get_redirection(url_short)
    assert response.url == link

#создать закрытую ссылку, поменять тип на публичную, удалить и проверить статус.
#этот тест запускается почему-то только отдельно, не могу понять почему. 
#если он запускается в составе теста, возвращается ошибка:
"""def _loop_writing(self, f=None, data=None):
        try:
            if f is not None and self._write_fut is None and self._closing:
                # XXX most likely self._force_close() has been called, and
                # it has set self._write_fut to None.
                return
            assert f is self._write_fut
            self._write_fut = None
            self._pending_write = 0
            if f:
                f.result()
            if data is None:
                data = self._buffer
                self._buffer = None
            if not data:
                if self._closing:
                    self._loop.call_soon(self._call_connection_lost, None)
                if self._eof_written:
                    self._sock.shutdown(socket.SHUT_WR)
                # Now that we've reduced the buffer size, tell the
                # protocol to resume writing if it was paused.  Note that
                # we do this last since the callback is called immediately
                # and it may add more data to the buffer (even causing the
                # protocol to be paused again).
                self._maybe_resume_protocol()
            else:
>               self._write_fut = self._loop._proactor.send(self._sock, data)
E               AttributeError: 'NoneType' object has no attribute 'send'"""
#в чём специфика работы pytest под дебагом и под релизом?

def test_operation_over_shorturl():
    username = "user_"+str(random.randint(10,9999999999))
    password = "password"
    response = UrlShortGenApi.create_user(username,password )
    assert response.status_code == 200

    token = str(random.randint(10,9999999999)) 
    link = "http://ya.ru/"+token
    response = UrlShortGenApi.create_short_url(link, type = "private", login= username, password= password)
    assert response.status_code == 201
    assert response.json()["url_full"] == link
    url_short = response.json()["url_short"]

    response = UrlShortGenApi.put_short_url(url_short, {"type":"public"}, login = username, password= password)
    assert response.status_code == 200
    

    response = UrlShortGenApi.delete_url(url_short)
    assert response.status_code == 200

    #работа этого эндпойнта оказалась зависима от вызова фукнции await db.refresh(obj_to_del) в функции delete класса RepositoryURL
    #если её не выызвать, при следующем обращении возникает ошибка cannot-perform-operation-another-operation-is-in-progress
    #https://stackoverflow.com/questions/76359971/error-cannot-perform-operation-another-operation-is-in-progress-only-when-ru
    #вопрос: почему? Ведь если мы выходим из контекстного менеджера асинхронной сессии, это автоматически означает закрытие всех 
    #операций? Или я неправильно понимаю?

    response = UrlShortGenApi.get_status_url(url_short)
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"
    assert response.json()["type"] == "public"


def test_ping_db():
    response = UrlShortGenApi.ping_db()
    assert response.status_code == 200
    assert response.json() == True
