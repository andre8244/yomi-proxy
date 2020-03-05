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
	"encoding/json"
	"fmt"
	"net/http"
	"path/filepath"

	"github.com/gin-gonic/gin"
	"github.com/nethesis/yomi-proxy/server/cache"
	"github.com/nethesis/yomi-proxy/server/configuration"
	"github.com/nethesis/yomi-proxy/server/models"
	"github.com/nethesis/yomi-proxy/server/utils"
)

func CheckStatus(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"status": "everything is okay"})
}

func CheckHash(c *gin.Context) {
	// init status obj
	var status models.Status

	// read hash from url
	hash := c.Param("hash")

	// init redis instance
	r := cache.Instance()

	// check if hash is locally cached
	var jsonCache models.Status
	value, err := r.Get(hash).Result()
	json.Unmarshal([]byte(value), &jsonCache)

	if err == nil {
		// if locally cached return the value
		status = models.Status{
			ID:         jsonCache.ID,
			Score:      jsonCache.Score,
			Malware:    jsonCache.Malware,
			Hash:       jsonCache.Hash,
			StatusCode: 200,
		}
	} else {
		// send the hash to yomi
		status = utils.CheckYomiHash(hash)

		// save hash in local cache
		if status.Malware != "Pending" {
			jsonStatus, _ := json.Marshal(status)
			err = r.Set(hash, jsonStatus, 0).Err()
			if err != nil {
				fmt.Println(err)
			}
		}
	}

	// return value
	c.JSON(status.StatusCode, status)
}

func Submit(c *gin.Context) {
	// init status obj
	var status models.Status

	// read upload file and hash
	hash := c.PostForm("hash")
	file, err := c.FormFile("file")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"mode": "read", "error": err.Error()})
		return
	}

	// init redis instance
	r := cache.Instance()

	// check if hash is locally cached
	var jsonCache models.Status
	value, err := r.Get(hash).Result()
	json.Unmarshal([]byte(value), &jsonCache)

	if err == nil {
		// if locally cached return the value
		status = models.Status{
			ID:         jsonCache.ID,
			Score:      jsonCache.Score,
			Malware:    jsonCache.Malware,
			Hash:       jsonCache.Hash,
			StatusCode: 200,
		}
	} else {
		// save file
		filename := configuration.Config.YomiUploadPath + "/" + filepath.Base(file.Filename)
		if err := c.SaveUploadedFile(file, filename); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"mode": "save", "error": err.Error()})
			return
		}

		// upload file to yomi
		status = utils.UploadYomiFile(filename)

		// save hash in local cache
		if status.StatusCode == 200 {
			jsonStatus, _ := json.Marshal(status)
			err = r.Set(hash, jsonStatus, 0).Err()
			if err != nil {
				fmt.Println(err)
			}
		}
	}

	// return value
	c.JSON(status.StatusCode, status)
}
