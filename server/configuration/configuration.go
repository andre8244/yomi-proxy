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

package configuration

import (
	"encoding/json"
	"fmt"
	"os"
)

type Configuration struct {
	ClientID       string `json:"client_id"`
	ClientSecret   string `json:"client_secret"`
	RedisAddress   string `json:"redis_address"`
	RedisPassword  string `json:"redis_password"`
	YomiBaseURL    string `json:"yomi_base_url"`
	YomiUploadPath string `json:"yomi_upload_path"`
}

var Config = Configuration{}

func Init(ConfigFilePtr *string) {
	// read configuration
	if _, err := os.Stat(*ConfigFilePtr); err == nil {
		file, _ := os.Open(*ConfigFilePtr)
		decoder := json.NewDecoder(file)
		// check errors or parse JSON
		err := decoder.Decode(&Config)
		if err != nil {
			fmt.Println("Configuration parsing error:", err)
		}
	}

	if os.Getenv("CLIENT_ID") != "" {
		Config.ClientID = os.Getenv("CLIENT_ID")
	}
	if os.Getenv("CLIENT_SECRET") != "" {
		Config.ClientSecret = os.Getenv("CLIENT_SECRET")
	}
	if os.Getenv("REDIS_ADDRESS") != "" {
		Config.RedisAddress = os.Getenv("REDIS_ADDRESS")
	}
	if os.Getenv("REDIS_PASSWORD") != "" {
		Config.RedisPassword = os.Getenv("REDIS_PASSWORD")
	}
	if os.Getenv("YOMI_BASE_URL") != "" {
		Config.YomiBaseURL = os.Getenv("YOMI_BASE_URL")
	}
	if os.Getenv("YOMI_UPLOAD_PATH") != "" {
		Config.YomiUploadPath = os.Getenv("YOMI_UPLOAD_PATH")
	}
}
