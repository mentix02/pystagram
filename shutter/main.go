package main

import (
	"database/sql"
	"log"
	"os"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

var DB *sql.DB

func init() {
	checkErr(godotenv.Load())
	DB = getDB(os.Getenv("DB_URL"))
	// gin.SetMode(gin.ReleaseMode)
}

func main() {
	defer DB.Close()
	router := gin.Default()
	router.Use(cors.New(getCorsConfig()))

	checkErr(router.SetTrustedProxies(nil))

	v1 := router.Group("/api/v1")
	userRouter := v1.Group("/user")
	{
		userRouter.GET("/email-availability/", fieldAvailabilityHandlerFactory("email"))
		userRouter.GET("/username-availability/", fieldAvailabilityHandlerFactory("username"))
	}

	log.Println("Running server on http://0.0.0.0:8080")
	log.Fatalln(router.Run(":8080"))
}
