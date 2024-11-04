package Facades

import (
	"context"
	"godatatthon/Services/FileService"
	"godatatthon/Services/FilepathService"
	"godatatthon/Services/LLMService"
	"godatatthon/Services/S3Service"
	"io"
	"log"
	"strings"
)

func FindOrAsk(ticker string, ctx context.Context) (string, error) {
	existingAnswer, err := find(ticker, ctx)
	if err != nil {
		newAnswer, _ := ask(ticker, ctx)
		return newAnswer, nil
	}
	return existingAnswer, nil

}

func find(ticker string, ctx context.Context) (string, error) {
	key := FilepathService.CreateKey(ticker)
	file, err := S3Service.FindFile(key, ctx)
	if err != nil {
		return "", err
	}
	var builder strings.Builder
	_, err = io.Copy(&builder, *file)
	if err != nil {
		log.Fatalln("Error reading from reader:", err)
		return "", err
	}
	return builder.String(), nil
}

func writeAnswer(ticker string, answer string) {
	key := FilepathService.CreateKey(ticker)
	FileService.Write(key, answer)
	defer FileService.Delete(key)
	S3Service.UploadAndDelete(key)
}

func ask(ticker string, ctx context.Context) (string, error) {
	answer, err := LLMService.Ask(ticker, ctx)
	if err != nil {
		return "", nil
	}
	writeAnswer(ticker, answer)
	return answer, nil
}
