#!/usr/bin/env bash
# Деплой: коммит изменений и push в origin main (учётные данные из .env).
set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

if [[ ! -f .env ]]; then
  echo "Создайте .env в корне проекта с GITHUB_USER и GITHUB_TOKEN (см. .env.example)"
  exit 1
fi

set -a
# shellcheck source=../.env
source .env
set +a

if [[ -z "${GITHUB_USER}" || -z "${GITHUB_TOKEN}" ]]; then
  echo "В .env должны быть заданы GITHUB_USER и GITHUB_TOKEN"
  exit 1
fi

export GITHUB_USER GITHUB_TOKEN
export GIT_ASKPASS="$REPO_ROOT/scripts/git-askpass.sh"

MSG="${1:-Update site}"
git add -A
if git diff --staged --quiet; then
  echo "Нет изменений для коммита."
  exit 0
fi
git commit -m "$MSG"
git push origin main
echo "Деплой отправлен. GitHub Actions соберёт сайт через 1–2 минуты."
