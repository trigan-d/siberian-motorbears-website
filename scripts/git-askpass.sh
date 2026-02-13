#!/usr/bin/env bash
# Отдаёт git логин/токен из переменных окружения (вызывается git при push).
# Не коммитить секреты — они только в .env
case "$1" in
  *[Uu]ser*) echo "${GITHUB_USER}" ;;
  *[Pp]ass*) echo "${GITHUB_TOKEN}" ;;
  *) exit 1 ;;
esac
