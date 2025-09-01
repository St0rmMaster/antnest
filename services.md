# Сервисы и боты

## postgresql-main

**Назначение:** Основная база данных PostgreSQL 17 для всех сервисов проекта

**Расположение:** 
- Контейнер: lxc-110-databases
- IP: 192.168.1.110:5432

**Интерфейсы/Порты:** 
- 5432/TCP — подключения к БД из сети 192.168.1.0/24

**Данные:** 
- Данные: /var/lib/postgresql/17/main
- Конфигурация: /etc/postgresql/17/main/postgresql.conf
- Аутентификация: /etc/postgresql/17/main/pg_hba.conf

**Зависимости:** 
- Нет внешних зависимостей

**Конфигурация:** 
- listen_addresses = '192.168.1.110,localhost'
- pg_hba: host all all 192.168.1.0/24 scram-sha-256
- Секреты: см. secrets.md

**Мониторинг:** 
- Проверка: `pg_isready -h 192.168.1.110`
- Статус: `systemctl status postgresql`

## Операции

### Обновление
1. Создать logical dump: `pg_dumpall -h 192.168.1.110 > backup_$(date +%Y%m%d).sql`
2. Остановить сервис: `systemctl stop postgresql`
3. Обновить пакет: `apt update && apt upgrade postgresql-17`
4. Запустить сервис: `systemctl start postgresql`
5. Проверить подключение: `pg_isready -h 192.168.1.110`

### Бэкап/восстановление
1. Logical dump всех БД: `pg_dumpall -h 192.168.1.110 > full_backup_$(date +%Y%m%d).sql`
2. Dump отдельной БД: `pg_dump -h 192.168.1.110 dbname > dbname_$(date +%Y%m%d).sql`
3. Восстановление: `psql -h 192.168.1.110 < backup_file.sql`

**Известные грабли:**
- listen_addresses требует restart вместо reload
- Проблемы прав владельца после pg_restore — исправлять через ALTER OWNER и GRANT

**Обновлено:** 2024-12-19

---

## nginx-proxy

**Назначение:** Reverse-proxy на хосте PVE для маршрутизации внешнего трафика к сервисам

**Расположение:** 
- Контейнер: хост PVE (192.168.1.253)
- Домены: pve.gramini.org, n8n.gramini.org

**Интерфейсы/Порты:** 
- 80/HTTP → автоматическое перенаправление на HTTPS
- 443/HTTPS → основные vhost'ы

**Данные:** 
- Конфигурация: /etc/nginx/sites-available/
- SSL сертификаты: /etc/letsencrypt/live/*/fullchain.pem
- Логи: /var/log/nginx/

**Зависимости:** 
- certbot (Let's Encrypt сертификаты)
- dnsmasq (split-DNS)

**Конфигурация:** 
- pve.gramini.org → 127.0.0.1:8006 (Proxmox админка)
- n8n.gramini.org → 192.168.1.120:5678 (n8n)
- Секреты: N/A

**Мониторинг:** 
- Проверка: `curl -I https://pve.gramini.org`
- Статус: `systemctl status nginx`

## Операции

### Обновление
1. Создать бэкап конфигурации: `cp -r /etc/nginx /etc/nginx.backup.$(date +%Y%m%d)`
2. Обновить пакет: `apt update && apt upgrade nginx`
3. Проверить конфигурацию: `nginx -t`
4. Перезагрузить конфигурацию: `systemctl reload nginx`
5. Проверить доступность: `curl -I https://pve.gramini.org`

### Бэкап/восстановление
1. Бэкап конфигурации: `tar -czf nginx-config-$(date +%Y%m%d).tar.gz /etc/nginx`
2. Бэкап SSL сертификатов: `tar -czf ssl-certs-$(date +%Y%m%d).tar.gz /etc/letsencrypt`
3. Восстановление: `tar -xzf nginx-config-YYYYMMDD.tar.gz -C /`

**Известные грабли:**
- Hair-pin NAT отсутствует — решено через dnsmasq split-DNS
- Certbot ошибки NXDOMAIN — проверить DNS и порты
- Путь к сертификату должен быть fullchain.pem, не cert.pem

**Обновлено:** 2024-12-19

---

## n8n-automation

**Назначение:** Платформа автоматизации workflow'ов и интеграций

**Расположение:** 
- Контейнер: lxc-120-n8n
- URL: https://n8n.gramini.org (внешний), http://192.168.1.120:5678 (внутренний)

**Интерфейсы/Порты:** 
- 5678/HTTP — веб-интерфейс n8n
- 3333/HTTP — n8n MCP bridge API

**Данные:** 
- Docker volume: n8n_data → /home/node/.n8n
- Конфигурация: переменные окружения в docker run

**Зависимости:** 
- PostgreSQL (192.168.1.110:5432, БД n8n)
- nginx-proxy (для внешнего доступа)

**Конфигурация:** 
- DB_TYPE=postgresdb
- DB_POSTGRESDB_HOST=192.168.1.110
- N8N_EDITOR_BASE_URL=https://n8n.gramini.org
- Секреты: см. secrets.md

**Мониторинг:** 
- Проверка: `curl -f http://192.168.1.120:5678/healthz`
- Docker статус: `docker ps | grep n8n`

## Операции

### Обновление
1. Создать бэкап БД: `pg_dump -h 192.168.1.110 n8n > n8n_backup_$(date +%Y%m%d).sql`
2. Остановить контейнер: `docker stop n8n`
3. Удалить старый контейнер: `docker rm n8n`
4. Запустить новую версию: `docker run -d --name n8n ... n8nio/n8n:latest`
5. Проверить доступность: `curl -f http://192.168.1.120:5678/healthz`

### Бэкап/восстановление
1. Остановить контейнер: `docker stop n8n`
2. Бэкап volume: `docker run --rm -v n8n_data:/data -v $(pwd):/backup alpine tar czf /backup/n8n_data_$(date +%Y%m%d).tar.gz /data`
3. Бэкап БД: `pg_dump -h 192.168.1.110 n8n > n8n_db_$(date +%Y%m%d).sql`

**Известные грабли:**
- Docker-порт проброшен неверно — проверять 5678:5678 в docker run
- SECURE_COOKIE=true требует HTTPS — установлено false для HTTP

**Обновлено:** 2024-12-19

---

## kimai-timetracker

**Назначение:** Система учёта рабочего времени и тайм-трекинг для проектов

**Расположение:** 
- Контейнер: lxc-120-n8n
- URL: http://192.168.1.120:8080 (внутренний)

**Интерфейсы/Порты:** 
- 8080/HTTP → 8001 (Kimai веб-интерфейс)

**Данные:** 
- Docker compose: /opt/kimai/docker-compose.yml
- MariaDB данные: volume db_data
- Файлы Kimai: volume kimai_files → /opt/kimai/var/data

**Зависимости:** 
- MariaDB 11 (внутри Docker stack)

**Конфигурация:** 
- DATABASE_URL=mysql://kimai:password@db/kimai
- APP_ENV=prod
- Секреты: см. secrets.md

**Мониторинг:** 
- Проверка: `curl -f http://192.168.1.120:8080`
- Docker статус: `docker compose ps` в /opt/kimai

## Операции

### Обновление
1. Создать бэкап БД: `docker compose exec db mysqldump -u root -p kimai > kimai_backup_$(date +%Y%m%d).sql`
2. Остановить стек: `cd /opt/kimai && docker compose down`
3. Обновить образы: `docker compose pull`
4. Запустить стек: `docker compose up -d`

### Бэкап/восстановление
1. Остановить стек: `cd /opt/kimai && docker compose down`
2. Бэкап volumes: `docker run --rm -v kimai_db_data:/data -v $(pwd):/backup alpine tar czf /backup/kimai_db_$(date +%Y%m%d).tar.gz /data`
3. Восстановление: обратная операция с tar xzf

**Известные грабли:**
- Порт 8080:8001 в docker-compose — проверять маппинг

**Обновлено:** 2024-12-19

---

## taiga-projectmanager

**Назначение:** Система управления проектами и задачами (Agile/Scrum)

**Расположение:** 
- Контейнер: lxc-120-n8n
- URL: http://192.168.1.120:9000 (внутренний)

**Интерфейсы/Порты:** 
- 9000/HTTP → 80 (Taiga веб-интерфейс через nginx-gateway)
- 8000/HTTP — REST API (внутренний)
- 8888/HTTP — WebSocket events (внутренний)

**Данные:** 
- Docker compose: /opt/taiga-full/docker-compose.yml
- Конфигурация: /opt/taiga-full/.env
- PostgreSQL данные: volume taiga-db-data
- Статика: volume taiga-static-data
- Медиа: volume taiga-media-data

**Зависимости:** 
- PostgreSQL 12 (внутри Docker stack)
- RabbitMQ (2 экземпляра для async и events)
- Nginx gateway (внутри stack)

**Конфигурация:** 
- TAIGA_DOMAIN=192.168.1.120:9000
- POSTGRES_HOST=taiga-db
- EMAIL_HOST=smtp.gmail.com
- Секреты: см. secrets.md

**Мониторинг:** 
- Проверка: `curl -f http://192.168.1.120:9000`
- Docker статус: `docker compose ps` в /opt/taiga-full

## Операции

### Обновление
1. Создать бэкап БД: `cd /opt/taiga-full && docker compose exec taiga-db pg_dump -U taiga taiga > taiga_backup_$(date +%Y%m%d).sql`
2. Остановить стек: `docker compose down`
3. Обновить образы: `docker compose pull`
4. Запустить стек: `docker compose up -d`

### Бэкап/восстановление
1. Остановить стек: `cd /opt/taiga-full && docker compose down`
2. Бэкап БД: `docker run --rm -v taiga-full_taiga-db-data:/data -v $(pwd):/backup alpine tar czf /backup/taiga_db_$(date +%Y%m%d).tar.gz /data`
3. Восстановление: обратная операция с tar xzf

**Известные грабли:**
- 502 Bad Gateway после рестарта taiga-back — перезапустить taiga-gateway
- 403 ACCESS_REFUSED в RabbitMQ — обновить пароли в контейнерах
- Статика не обновляется — удалить том taiga-static-data и пересоздать

**Обновлено:** 2024-12-19

---

## telegram-bots

**Назначение:** Telegram боты для различных проектов (German, Cardio, Mamontov)

**Расположение:** 
- Контейнер: lxc-120-n8n
- Боты работают через Docker контейнеры

**Интерфейсы/Порты:** 
- Исходящие HTTPS подключения к Telegram API

**Данные:** 
- Конфигурация: /root/*.env файлы
- Данные ботов в соответствующих БД PostgreSQL

**Зависимости:** 
- PostgreSQL (192.168.1.110) — БД germanbot, cardiobot, mamontov
- Telegram Bot API
- GitHub (для auto-deploy через PAT)

**Конфигурация:** 
- Переменные окружения в /root/german.env, /root/cardio.env, /root/mamontov.env
- Секреты: см. secrets.md

**Мониторинг:** 
- Docker статус: `docker ps | grep bot`
- Проверка логов: `docker logs bot_name`

## Операции

### Обновление
1. Создать бэкап БД ботов: `pg_dump -h 192.168.1.110 germanbot > germanbot_backup_$(date +%Y%m%d).sql`
2. Остановить контейнеры ботов: `docker stop german_bot cardio_bot mamontov_bot`
3. Обновить образы: `docker pull latest_image`
4. Запустить обновлённые контейнеры

### Бэкап/восстановление
1. Бэкап БД каждого бота: `pg_dump -h 192.168.1.110 botname > botname_$(date +%Y%m%d).sql`
2. Бэкап конфигураций: `cp /root/*.env /backup/`
3. Восстановление БД: `psql -h 192.168.1.110 botname < botname_backup.sql`

**Известные грабли:**
- Отсутствующие .env файлы — проверять перед запуском Docker
- GitHub PAT токены могут истекать

**Обновлено:** 2024-12-19

---

## taiga-mcp-bridge

**Назначение:** MCP (Model Context Protocol) мост для интеграции Taiga с Claude AI

**Расположение:** 
- Контейнер: lxc-150-mcp-taiga
- URL: http://192.168.1.150:8000/sse (HTTP-SSE endpoint)

**Интерфейсы/Порты:** 
- 8000/HTTP — SSE сервер для MCP коммуникации

**Данные:** 
- Проект: /opt/pytaiga-mcp
- Виртуальное окружение: /opt/pytaiga-mcp/.venv
- Конфигурация: /opt/pytaiga-mcp/.env
- Логи: stdout (LOG_FILE=/dev/stdout)

**Зависимости:** 
- Taiga API (http://192.168.1.120:9000/api/v1)
- Python 3.x + виртуальное окружение

**Конфигурация:** 
- TAIGA_API_URL=http://192.168.1.120:9000/api/v1
- TAIGA_TRANSPORT=sse
- TAIGA_USERNAME=master
- Секреты: см. secrets.md

**Мониторинг:** 
- Проверка: `curl -v -N http://192.168.1.150:8000/sse`
- Статус: `systemctl status taiga-mcp` (если используется systemd)

## Операции

### Обновление
1. Остановить сервис: `systemctl stop taiga-mcp` или Ctrl+C
2. Обновить код: `cd /opt/pytaiga-mcp && git pull`
3. Активировать venv: `source .venv/bin/activate`
4. Обновить зависимости: `uv pip install -r requirements.txt`
5. Запустить сервис: `systemctl start taiga-mcp` или `./run.sh --sse`

### Бэкап/восстановление
1. Бэкап проекта: `tar -czf pytaiga-mcp_$(date +%Y%m%d).tar.gz /opt/pytaiga-mcp`
2. Восстановление: `tar -xzf pytaiga-mcp_YYYYMMDD.tar.gz -C /opt/`
3. Пересоздать venv: `cd /opt/pytaiga-mcp && ./install.sh`

**Известные грабли:**
- "Тишина" в консоли — установить LOG_FILE=/dev/stdout в .env
- HTTP 307 при обращении к /sse/ — использовать /sse без конечного слэша
- --sse аргумент игнорируется — патч в src/server.py

**Обновлено:** 2024-12-19

---

## nextcloud-storage

**Назначение:** Облачное файловое хранилище и синхронизация

**Расположение:** 
- Контейнер: lxc-160-cloud
- URL: http://192.168.1.160 (внутренний)

**Интерфейсы/Порты:** 
- 80/HTTP — веб-интерфейс Nextcloud
- 443/HTTPS — защищённый доступ (если настроен)

**Данные:** 
- Данные Nextcloud: конфигурация и файлы пользователей
- MariaDB данные: база данных Nextcloud

**Зависимости:** 
- MariaDB (внутри контейнера)

**Конфигурация:** 
- Секреты: см. secrets.md

**Мониторинг:** 
- Проверка: `curl -f http://192.168.1.160`

## Операции

### Обновление
1. Создать бэкап данных и БД
2. Остановить службы Nextcloud
3. Обновить пакеты: `apt update && apt upgrade`
4. Запустить службы

### Бэкап/восстановление
1. Остановить Nextcloud
2. Бэкап данных: `tar -czf nextcloud_data_$(date +%Y%m%d).tar.gz /var/www/nextcloud/data`
3. Бэкап БД: `mysqldump -u ncuser -p nextcloud > nextcloud_db_$(date +%Y%m%d).sql`

**Известные грабли:**
- N/A

**Обновлено:** 2024-12-19
