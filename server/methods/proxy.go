/*
 * Copyright (C) 2020 Nethesis S.r.l.
 * http://www.nethesis.it - info@nethesis.it
 *
 * This file is part of Yomi-Proxy project.
 *
 * Yomi-Proxy is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * Yomi-Proxy is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with Yomi-Proxy. If not, see COPYING.
 *
 * author: Edoardo Spadoni <edoardo.spadoni@nethesis.it>
 */

package methods

import (
	"fmt"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/nethesis/yomi-proxy/server/cache"
	"github.com/nethesis/yomi-proxy/server/models"
	"github.com/nethesis/yomi-proxy/server/utils"
)

func CheckStatus(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"status": "everything is okay"})
}

func CheckHash(c *gin.Context) {
	// read hash from url
	hash := c.Param("hash")

	// init status obj
	var status models.Status

	// init redis instance
	r := cache.Instance()

	// check if hash is locally cached
	score, err := r.Get(hash).Result()

	if err == nil {
		// if locally cached return the value
		fScore, _ := strconv.ParseFloat(score, 64)
		status = models.Status{
			Score:       fScore,
			Malware:     "",
			YoroiSha256: hash,
			YomiID:      0,
			StatusCode:  200,
		}
	} else {
		// send the hash to yomi
		status = utils.CheckYomiHash(hash)

		// save hash in local cache
		err = r.Set(hash, status.Score, 0).Err()
		if err != nil {
			fmt.Println(err)
		}
	}

	// return value
	c.JSON(status.StatusCode, status)
}

/* func Submit(c *gin.Context) {
	sessionId := c.PostForm("session_id")
	operatorId := c.PostForm("operator_id")

	var session models.Session
	db := database.Instance()
	db.Where("session_id = ?", sessionId).First(&session)

	if session.Id == 0 {
		c.JSON(http.StatusNotFound, gin.H{"message": "No session found!"})
		return
	}

	sessionCreated := session.Started
	sessionConnected := time.Now().String()

	log := models.Log{
		SessionId:        sessionId,
		OperatorId:       operatorId,
		SessionCreated:   sessionCreated,
		SessionConnected: sessionConnected,
	}

	db.Save(&log)

	c.JSON(http.StatusCreated, gin.H{"id": log.Id})
} */
