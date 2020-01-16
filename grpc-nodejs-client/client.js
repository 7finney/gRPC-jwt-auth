var PROTO_PATH = './protos/conn.proto';
var grpc = require('@grpc/grpc-js');
var protoLoader = require('@grpc/proto-loader');

var packageDefinition = protoLoader.loadSync(
  PROTO_PATH,
  {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true
  });

// var clientCallService = grpc.loadPackageDefinition(packageDefinition).ClientCallService;

var protoDescriptor = grpc.loadPackageDefinition(packageDefinition);

var client_tests_pb = protoDescriptor.eth_client_call;

var client = new client_tests_pb.ClientCallService('clientcallapi.localhost:50053', grpc.credentials.createInsecure());

var meta = new grpc.Metadata();
meta.add('authorization', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtYWNoaW5lSUQiOiJzYmRjamtjYmtqYSJ9.84g5qDtLy06eGlG0ztU1iTBmLojTZ6g4rjN1f5YLVCo');

var data = {
  callInterface: {
    command: "deploy-contract",
    payload: "9522"
  }
}


client.RunDeploy(data, meta, function (err, Response) {
  if (err) {
    console.log("err", err);
  } else {
    console.log("feaaaaaa", Response);
  }
});