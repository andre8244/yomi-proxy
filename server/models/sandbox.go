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

package models

import "time"

type Sandbox struct {
	File struct {
		Hash struct {
			Sha256 string `json:"sha256"`
		} `json:"hash"`
		Filename string `json:"filename"`
		Filetype string `json:"filetype"`
		Size     int    `json:"size"`
		Score    int    `json:"score"`
	} `json:"file"`
	Threat struct {
		Signatures []string `json:"signatures"`
		Tags       []string `json:"tags"`
		Details    struct {
			MalwareClasses []string `json:"malwareClasses"`
		} `json:"details"`
		Name      string `json:"name"`
		Category  string `json:"category"`
		Signature string `json:"signature"`
	} `json:"threat"`
	Ticket                string    `json:"ticket"`
	Closed                bool      `json:"closed"`
	FalsePositive         bool      `json:"falsePositive"`
	Safe                  string    `json:"safe"`
	ID                    string    `json:"_id"`
	Score                 float64   `json:"score"`
	Date                  time.Time `json:"date"`
	Customer              string    `json:"customer"`
	Reseller              string    `json:"reseller"`
	SLADate               time.Time `json:"slaDate"`
	Reports               []string  `json:"reports"`
	V                     int       `json:"__v"`
	AnalysisCompletedDate time.Time `json:"analysisCompletedDate"`
}
