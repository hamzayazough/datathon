package main

import (
	"godatatthon/Server"

	"github.com/joho/godotenv"
)

func main() {
	godotenv.Load("creds.env")
	s := Server.NewServer()
	Server.Run(s)
}
