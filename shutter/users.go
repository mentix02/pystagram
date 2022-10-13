package main

import (
	"fmt"

	"github.com/gin-gonic/gin"
)

func fieldAvailabilityHandlerFactory(field string) gin.HandlerFunc {
	return func(c *gin.Context) {
		var count int
		value := c.Query(field)
		query := fmt.Sprintf("SELECT COUNT(%s) FROM user_user WHERE %s = ?", field, field)

		stmt, _ := DB.Prepare(query)
		err := stmt.QueryRow(value).Scan(&count)

		if err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
		} else {
			c.JSON(200, gin.H{"available": count == 0})
		}
	}
}
