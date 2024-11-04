package LLMService

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/bedrockagentruntime"
	"github.com/aws/aws-sdk-go-v2/service/bedrockagentruntime/types"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/google/uuid"
)

var client *bedrockagentruntime.Client
var cfg aws.Config

func Setup() {
	cfg, err := config.LoadDefaultConfig(
		context.Background(),
	)
	if err != nil {
		log.Fatal(err)
	}
	client = bedrockagentruntime.NewFromConfig(cfg)

}

func Ask(ticker string, ctx context.Context) (string, error) {
	agentId := os.Getenv("AGENT_ID")
	sessionId := uuid.New().String()
	response, err := client.InvokeAgent(ctx, &bedrockagentruntime.InvokeAgentInput{
		AgentId:      aws.String(agentId),
		InputText:    aws.String(ticker),
		AgentAliasId: aws.String("GZIBIQPVC3"),
		EnableTrace:  aws.Bool(false),
		SessionId:    aws.String(sessionId),
	})
	if err != nil {
		fmt.Printf("failed to invoke: %s\n", err)
		return "", err
	}

	stream := response.GetStream().Reader
	events := stream.Events()
	completeResponse := ""
	for {
		event := <-events
		if event != nil {
			if chunk, ok := event.(*types.ResponseStreamMemberChunk); ok {
				completeResponse += string(chunk.Value.Bytes)
			}
		} else {
			break
		}
	}
	stream.Close()

	return completeResponse, nil
}
