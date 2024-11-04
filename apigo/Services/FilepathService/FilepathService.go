package FilepathService

import (
	"fmt"
	"time"
)

const FOLDER = "TA/"

func getDate() string {
	currentTime := time.Now()
	return currentTime.Format("2006-01")
}

func CreateKey(filename string) string {
	return fmt.Sprintf("%s%s-%s", FOLDER, filename, getDate())
}
