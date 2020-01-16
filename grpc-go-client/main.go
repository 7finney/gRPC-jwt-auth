package main

import (
	"context"
	"grpc-go-client/eth_client_call"
	"io"
	"log"

	"google.golang.org/grpc"
	"google.golang.org/grpc/metadata"
)

type CallInterface struct {
	Command string
	Payload string
}

func main() {
	// conn, err := grpc.Dial("localhost:4040", grpc.WithInsecure())
	conn, err := grpc.Dial("localhost:50053", grpc.WithInsecure())
	if err != nil {
		panic(err)
	}
	defer conn.Close()
	client := eth_client_call.NewClientCallServiceClient(conn)
	header := metadata.New(map[string]string{"authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtYWNoaW5lSUQiOiJxd2VydHkifQ.sqrLwRfVbxAxpq0kVEK238TlZoXLONAoy57Felg_9o"})
	ctx := metadata.NewOutgoingContext(context.Background(), header)
	ci := &eth_client_call.ClientCallInterface{
		Command: "deploy-contract",
		Payload: "no string"}
	c := &eth_client_call.ClientCallRequest{
		CallInterface: ci,
	}
	stream, err := client.RunDeploy(ctx, c)
	if err != nil {
		panic(err)
	}
	waitc := make(chan struct{})
	go func() {
		for {
			in, err := stream.Recv()
			if err == io.EOF {
				// read done.
				close(waitc)
				return
			}
			if err != nil {
				log.Fatalf("Failed to receive a note : %v", err)
			}
			log.Printf("Got message %s", in.Result)
		}
	}()
	stream.CloseSend()
	<-waitc
}
