<<<<<<< HEAD
from httpStubFramework.httpServerOperate import StubOperate

# init stub
fileAppConfig = {
    "http_port": 8771,
    "socket_client_port": 8772,
    "socket_server_port": 8773,
}

fileAppStub = StubOperate(fileAppConfig["http_port"], fileAppConfig["socket_client_port"],
                          fileAppConfig["socket_server_port"])

=======
from httpStubFramework.httpServerOperate import StubOperate

# init stub
fileAppConfig = {
    "http_port": 8771,
    "socket_client_port": 8772,
    "socket_server_port": 8773,
}

fileAppStub = StubOperate(fileAppConfig["http_port"], fileAppConfig["socket_client_port"],
                          fileAppConfig["socket_server_port"])

>>>>>>> 79ffeff93db58c559e3491c93f439cd73c418f76
print("init stub")