# gRPC-jwt-auth
gRPC authentication using JWT


## Generate protobuf file for GRPC Go client
```shell
$  protoc --proto_path=protos --go_out=plugins=grpc:protos conn.proto
```

## Generate protobuf for Python GRPC server
```shell
$ python -m grpc_tools.protoc -I./protos --python_out=./generated/ --grpc_python_out=./generated/ ./protos/conn.proto
```

Run Python Server using
```shell
$ python3 server.py
```

While python server running, Run the ```main.go``` file
```shell
$ go run main.go
```
