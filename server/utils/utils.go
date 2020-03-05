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

package utils

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"

	"github.com/nethesis/yomi-proxy/server/configuration"
	"github.com/nethesis/yomi-proxy/server/models"
)

func Authenticate() string {
	// create request url
	url := configuration.Config.YomiBaseURL + "/pauth/token"

	// compose json request
	values := map[string]string{
		"client_id":     configuration.Config.ClientID,
		"client_secret": configuration.Config.ClientSecret,
		"grant_type":    "client_credentials",
		"scope":         "/papi/sandbox.lookup,/papi/sandbox.submit",
	}
	jsonValue, _ := json.Marshal(values)

	// make request
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonValue))
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	// parse body to json
	body, err := ioutil.ReadAll(resp.Body)
	var respToken models.Token
	err = json.Unmarshal(body, &respToken)

	// check errors
	if err != nil {
		fmt.Println(err.Error())
	}

	// return access token
	return respToken.AccessToken
}

func CheckYomiHash(hash string) models.Status {
	// get authentication bearer
	bearer := Authenticate()

	// create url
	url := configuration.Config.YomiBaseURL + "/papi/sandbox/hash/" + hash

	// make request
	req, err := http.NewRequest("GET", url, nil)
	req.Header.Set("Authorization", "Bearer "+bearer)
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	// check request status codes
	if resp.StatusCode != 200 {
		return models.Status{
			ID:         "",
			Score:      -1,
			Malware:    "",
			Hash:       "",
			StatusCode: resp.StatusCode,
		}
	}

	// parse body to json
	body, _ := ioutil.ReadAll(resp.Body)
	var respHash models.Hash
	err = json.Unmarshal(body, &respHash)

	// check json parsing
	if err != nil {
		return models.Status{
			ID:         "",
			Score:      -1,
			Malware:    "",
			Hash:       "",
			StatusCode: 500,
		}
	}

	// hash not found
	if len(respHash) == 0 {
		return models.Status{
			ID:         "",
			Score:      -1,
			Malware:    "",
			Hash:       "",
			StatusCode: 404,
		}
	}

	// return hash found info
	return models.Status{
		ID:         "",
		Score:      respHash[0].Score,
		Malware:    respHash[0].Threat.Name,
		Hash:       respHash[0].File.Hash.Sha256,
		StatusCode: 200,
	}

}

func UploadYomiFile(filename string) models.Status {
	// get authentication bearer
	bearer := Authenticate()

	// create url
	url := configuration.Config.YomiBaseURL + "/papi/sandbox"

	// read file
	file, _ := os.Open(filename)
	defer file.Close()

	// create form data
	fileBody := &bytes.Buffer{}
	writer := multipart.NewWriter(fileBody)
	part, _ := writer.CreateFormFile("file", filepath.Base(file.Name()))
	io.Copy(part, file)
	writer.Close()

	// make request
	req, err := http.NewRequest("POST", url, fileBody)
	req.Header.Set("Authorization", "Bearer "+bearer)
	req.Header.Add("Content-Type", writer.FormDataContentType())

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	// check request status codes
	if resp.StatusCode != 200 {
		return models.Status{
			ID:         "",
			Score:      -1,
			Malware:    "",
			Hash:       "",
			StatusCode: resp.StatusCode,
		}
	}

	// parse body to json
	body, _ := ioutil.ReadAll(resp.Body)
	var respSandbox models.Sandbox
	err = json.Unmarshal(body, &respSandbox)

	// check json parsing
	if err != nil {
		return models.Status{
			ID:         "",
			Score:      -1,
			Malware:    "",
			Hash:       "",
			StatusCode: 500,
		}
	}

	// hash submitted but waiting
	if respSandbox.V == 0 || respSandbox.ID == "" {
		return models.Status{
			ID:         "",
			Score:      -1,
			Malware:    "",
			Hash:       "",
			StatusCode: 202,
		}
	}

	// return hash found info
	return models.Status{
		ID:         respSandbox.ID,
		Score:      respSandbox.Score,
		Malware:    respSandbox.Threat.Name,
		Hash:       respSandbox.File.Hash.Sha256,
		StatusCode: 200,
	}
}
