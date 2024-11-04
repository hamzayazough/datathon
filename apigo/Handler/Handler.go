package Handler

import (
	"godatatthon/Facades"
	"net/http"
	"strings"
)

var symbols = []string{
	"AAPL", "AMZN", "TSLA", "GOOGL", "MSFT", "NVDA", "META", "BRK.B", "JPM", "V",
	"JNJ", "PG", "DIS", "MA", "HD", "BAC", "PFE", "XOM", "KO", "PEP",
	"CSCO", "INTC", "NFLX", "WMT", "BA", "MRK", "NKE", "ORCL", "ABT", "CVX",
}

func verifyIfExist(ticker string) bool {
	for _, v := range symbols {
		if v == ticker {
			return true
		}
	}
	return false
}

func AskByTicker(w http.ResponseWriter, r *http.Request) {
	ticker := r.PathValue("ticker")
	ticker = strings.ToUpper(ticker)
	if !verifyIfExist(ticker) {
		http.Error(w, "Bad ticker", http.StatusBadRequest)
		return
	}
	answer, err := Facades.FindOrAsk(ticker, r.Context())
	if err != nil {
		return
	}
	w.Write([]byte(answer))
}
