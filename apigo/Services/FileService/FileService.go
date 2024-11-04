package FileService

import (
	"godatatthon/Services/FilepathService"
	"log"
	"os"
)

func ensureDir(dirPath string) error {
	if _, err := os.Stat(dirPath); os.IsNotExist(err) {
		// Create the directory
		_ = os.MkdirAll(dirPath, os.ModePerm)
	}
	return nil
}
func Write(filename string, text string) {
	ensureDir(FilepathService.FOLDER)
	err := os.WriteFile(filename, []byte(text), 0666)
	if err != nil {
		log.Fatalf("Error writing file: %s\n", err)
	}
}

func Delete(filename string) {
	os.Remove(filename)
}
