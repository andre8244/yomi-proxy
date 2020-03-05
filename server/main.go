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

package main

import (
	"flag"
	"net/http"

	"github.com/gin-gonic/gin"

	"github.com/nethesis/yomi-proxy/server/cache"
	"github.com/nethesis/yomi-proxy/server/configuration"
	"github.com/nethesis/yomi-proxy/server/methods"
)

func main() {
	// read and init configuration
	ConfigFilePtr := flag.String("c", "/opt/yomi-proxy/server/conf.json", "Path to configuration file")
	flag.Parse()
	configuration.Init(ConfigFilePtr)

	// init cache
	r := cache.Init()
	defer r.Close()

	// init routers
	router := gin.Default()

	// define endpoints
	api := router.Group("/api")
	{
		api.GET("/status", methods.CheckStatus)
		api.GET("/hash/:hash", methods.CheckHash)
		api.POST("/submit", methods.Submit)
	}

	// handle missing endpoint
	router.NoRoute(func(c *gin.Context) {
		c.JSON(http.StatusNotFound, gin.H{"message": "API not found"})
	})

	// start router
	router.Run()

}
