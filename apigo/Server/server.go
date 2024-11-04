package Server

import (
	"fmt"
	"godatatthon/Handler"
	"godatatthon/Services/LLMService"
	"godatatthon/Services/S3Service"
	"net/http"

	"github.com/rs/cors"
)

const PORT = ":8080"

func AddRoutes(mux *http.ServeMux) {
	cors.New(cors.Options{
		AllowedOrigins:   []string{"*"},
		AllowCredentials: true,
		AllowedMethods:   []string{"*"},
		AllowedHeaders:   []string{"*"},
	}).Handler(mux)
	mux.HandleFunc("GET /ask/{ticker}", Handler.AskByTicker)
}

func NewServer() *http.Server {
	S3Service.Setup()
	LLMService.Setup()
	router := http.NewServeMux()
	AddRoutes(router)

	return &http.Server{
		Addr:    PORT,
		Handler: router,
	}
}

func Run(server *http.Server) {
	fmt.Printf("Listing at http://localhost%s\n", PORT)
	server.ListenAndServe()
}
