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

package cache

import (
	"github.com/nethesis/yomi-proxy/server/configuration"

	"github.com/go-redis/redis"
)

var cache *redis.Client

func Instance() *redis.Client {
	if cache == nil {
		cache := Init()
		return cache
	}
	return cache
}

func Init() *redis.Client {
	client := redis.NewClient(&redis.Options{
		Addr:     configuration.Config.RedisAddress,
		Password: configuration.Config.RedisPassword,
		DB:       0,
	})
	return client
}
