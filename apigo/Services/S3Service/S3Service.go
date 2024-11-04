package S3Service

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/feature/s3/manager"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go-v2/service/s3/types"
)

var client *s3.Client
var cfg aws.Config
var uploader *manager.Uploader

const BUCKET_NAME = "taindiractors"
const FOLDER = "TA/"

func Setup() {
	cfg, err := config.LoadDefaultConfig(
		context.Background(),
	)
	if err != nil {
		log.Fatal(err)
	}
	client = s3.NewFromConfig(cfg)
	uploader = manager.NewUploader(s3.NewFromConfig(cfg))
}

func FindFile(key string, ctx context.Context) (*io.ReadCloser, error) {
	file, err := client.GetObject(ctx, &s3.GetObjectInput{
		Bucket: aws.String(BUCKET_NAME),
		Key:    aws.String(key),
	})
	if err != nil {
		var noKey *types.NoSuchKey
		if errors.As(err, &noKey) {
			err = noKey
		}
		return nil, err
	}
	return &file.Body, err
}

func UploadAndDelete(key string) {
	file, err := os.Open(key)
	defer file.Close()

	var buf bytes.Buffer
	_, err = io.Copy(&buf, file)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Error reading file:", err)
		return
	}

	_, err = uploader.Upload(context.TODO(), &s3.PutObjectInput{
		Bucket: aws.String(BUCKET_NAME),
		Key:    aws.String(key),
		Body:   bytes.NewReader(buf.Bytes()),
	})

	if err != nil {
		fmt.Println("Error uploading file:", err)
		return
	}
}
