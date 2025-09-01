# Контейнеры LXC

## lxc-110-databases

**Роль:** Сервер баз данных PostgreSQL 17 для всех сервисов

**Расположение:** 
- Хост: Proxmox VE (pve)
- IP: 192.168.1.110/24 (veth110i0)

**Ресурсы:** 
- Шаблон: debian-12-standard
- Storage: tppool

**Сеть/Порты:** 
- 5432 → PostgreSQL (доступ из 192.168.1.0/24)
- 22 → SSH

**Данные/тома:** 
- /var/lib/postgresql/17/main — данные PostgreSQL
- /etc/postgresql/17/main — конфигурация

**Сервисы внутри:** 
- postgresql-17 (active)
- postgresql-client-17

**Конфигурация PostgreSQL:**
- listen_addresses = '192.168.1.110,localhost'
- pg_hba: host all all 192.168.1.0/24 scram-sha-256
- Firewall: ACCEPT TCP 5432 из 192.168.1.0/24

**Базы данных:**
- appdb (owner: appuser)
- n8n (owner: n8nuser) 
- germanbot (owner: germanbot)
- cardiobot (owner: cardiobot)
- mamontov (owner: mamontovuser)

**Пароль root:** см. secrets.md
**Snapshot:** pg_initial_setup

**Известные грабли:**
- listen_addresses требует restart вместо reload
- Проблемы прав владельца после pg_restore — исправлять через ALTER OWNER и GRANT

**Обновлено:** 2024-12-19

---

## lxc-120-n8n

**Роль:** Контейнер для Docker-приложений (n8n, боты, Kimai, Taiga)

**Расположение:** 
- Хост: Proxmox VE (pve)
- IP: 192.168.1.120/24 (veth120i0)

**Ресурсы:** 
- Шаблон: debian-12-standard
- Storage: tppool
- Доп-фичи: nesting=1, keyctl=1, unprivileged

**Сеть/Порты:** 
- 5678 → n8n веб-интерфейс
- 8080 → Kimai (8080:8001)
- 9000 → Taiga (9000:80)
- 3333 → n8n-mcp HTTP API
- 22 → SSH

**Данные/тома:** 
- /opt/kimai — Kimai docker-compose стек
- /opt/taiga-full — Taiga docker-compose стек  
- /opt/n8n-mcp — n8n MCP bridge скрипты
- /root/*.env — переменные окружения для ботов
- Docker volumes: n8n_data, kimai_files, taiga-*

**Сервисы внутри:** 
- Docker Engine 28.03
- n8n (контейнер)
- Kimai + MariaDB (контейнеры)
- Taiga + PostgreSQL + RabbitMQ (контейнеры)
- Telegram-боты: German, Cardio, Mamontov (контейнеры)

**Конфигурация:**
- Firewall: ACCEPT TCP 5678 из 192.168.1.0/24

**Пароль root:** см. secrets.md
**Snapshot:** n8n_ok_http5678

**Известные грабли:**
- Docker-порт проброшен неверно — проверять порты в docker run
- Отсутствующие .env файлы — проверять перед запуском
- SECURE_COOKIE=true требует HTTPS — изменили на false

**Обновлено:** 2024-12-19

---

## lxc-130-service

**Роль:** Дополнительный сервисный контейнер

**Расположение:** 
- Хост: Proxmox VE (pve)  
- IP: 192.168.1.130/24

**Ресурсы:** 
- Шаблон: debian-12-standard
- Storage: tppool

**Сеть/Порты:** 
- 22 → SSH

**Данные/тома:** 
- стандартная файловая система

**Сервисы внутри:** 
- базовая система Debian

**Пароль root:** см. secrets.md

**Известные грабли:**
- N/A

**Обновлено:** 2024-12-19

---

## lxc-140-gigabot

**Роль:** Контейнер для GigaBot

**Расположение:** 
- Хост: Proxmox VE (pve)
- IP: 192.168.1.140/24

**Ресурсы:** 
- Шаблон: debian-12-standard
- Storage: tppool

**Сеть/Порты:** 
- 22 → SSH

**Данные/тома:** 
- конфигурация и данные GigaBot

**Сервисы внутри:** 
- GigaBot

**Пароль root:** см. secrets.md

**Известные грабли:**
- N/A

**Обновлено:** 2024-12-19

---

## lxc-150-mcp-taiga

**Роль:** Taiga MCP Bridge для интеграции с Claude AI

**Расположение:** 
- Хост: Proxmox VE (pve)
- IP: 192.168.1.150/24

**Ресурсы:** 
- Шаблон: debian-12-standard
- Storage: tppool

**Сеть/Порты:** 
- 8000 → HTTP-SSE сервер MCP
- 22 → SSH

**Данные/тома:** 
- /opt/pytaiga-mcp — проект MCP bridge
- /opt/pytaiga-mcp/.venv — виртуальное окружение Python
- /opt/pytaiga-mcp/.env — конфигурация

**Сервисы внутри:** 
- pytaiga-mcp (Python HTTP-SSE сервер)
- systemd служба taiga-mcp (опционально)

**Пароль root:** см. secrets.md

**Известные грабли:**
- "Тишина" в консоли — установить LOG_FILE=/dev/stdout в .env
- HTTP 307 при обращении к /sse/ — использовать /sse без слэша
- --sse аргумент игнорируется — патч в src/server.py

**Обновлено:** 2024-12-19

---

## lxc-160-cloud

**Роль:** Nextcloud сервер для файлового хранилища

**Расположение:** 
- Хост: Proxmox VE (pve)
- IP: 192.168.1.160/24

**Ресурсы:** 
- Шаблон: debian-12-standard
- Storage: tppool

**Сеть/Порты:** 
- 80 → HTTP веб-интерфейс Nextcloud
- 443 → HTTPS (если настроен)
- 22 → SSH

**Данные/тома:** 
- Nextcloud данные и конфигурация
- MariaDB данные

**Сервисы внутри:** 
- Nextcloud
- MariaDB

**Пароль root:** см. secrets.md

**Известные грабли:**
- N/A

**Обновлено:** 2024-12-19
