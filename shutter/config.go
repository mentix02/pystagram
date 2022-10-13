package main

import (
	"database/sql"

	"github.com/gin-contrib/cors"
	_ "github.com/go-sql-driver/mysql"
)

func getDB(dataSourceName string) *sql.DB {
	db, err := sql.Open("mysql", dataSourceName)
	checkErr(err)
	return db
}

func getCorsConfig() cors.Config {
	config := cors.DefaultConfig()
	config.AllowOrigins = []string{"http://localhost:5173"}
	return config
}
