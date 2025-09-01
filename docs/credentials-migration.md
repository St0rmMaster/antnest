# Миграция учётных данных в Vault

> ⚠️ **ВАЖНО**: Этот файл содержит чувствительную информацию и должен быть удалён после переноса всех секретов в хранитель (Vault или аналог).

## Структура хранилища секретов

Рекомендуемая структура путей в Vault:

```
vault://
├── databases/
│   └── postgresql/
│       ├── appuser-password
│       ├── n8nuser-password  
│       ├── germanbot-password
│       ├── cardiobot-password
│       └── mamontovuser-password
├── containers/
│   ├── lxc-110-root-password
│   ├── lxc-120-root-password
│   ├── lxc-130-root-password
│   ├── lxc-140-root-password
│   ├── lxc-150-root-password
│   └── lxc-160-root-password
├── n8n/
│   ├── admin-password
│   ├── db-password
│   └── api-key
├── kimai/
│   ├── db-root-password
│   ├── db-user-password
│   └── admin-password
├── taiga/
│   ├── db-password
│   ├── admin-password
│   ├── secret-key
│   ├── rabbitmq-password
│   └── email-password
├── taiga-mcp/
│   ├── taiga-username
│   ├── taiga-password
│   └── auth-token
├── telegram-bots/
│   ├── german-bot-token
│   ├── cardio-bot-token
│   ├── mamontov-bot-token
│   └── github-pat-tokens
└── nextcloud/
    ├── admin-password
    ├── db-password
    └── db-root-password
```

## Данные для миграции

### Контейнеры LXC (root пароли)
- **lxc-110-databases**: `GgQ-4p9-zG3-XZk`
- **lxc-120-apps**: `h4j-VLN-NdN-Avj`
- **lxc-130-service**: `w32-SQU-3TY-BeW`
- **lxc-140-gigabot**: `Z2T-djm-5Aw-QST`
- **lxc-150-mcp-taiga**: [не указан в исходном документе]
- **lxc-160-cloud**: `afx-Tjc-jVc-6b3`

### PostgreSQL (192.168.1.110:5432)
- **appuser**: `S3cureLONGPass!`
- **n8nuser**: `N8nDBPass!`
- **germanbot**: `StrongGermanPass!`
- **cardiobot**: `StrongCardioPass!`
- **mamontovuser**: `MamontovDBPass!`

### n8n
- **Basic Auth**: admin / `djx-ExM-s6A-jVy1!`
- **API Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkYTVhYWEwZC1jYjNiLTRlODItYmIzZS03OTRjMGI0OWNjZDAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU0NzgwODAxfQ._hkE50LwSiqvU48Vd8hunutZWDFU3dAy7KvjCbi8rzQ`
- **MCP Auth Token**: `56981a88168527130cc9a76bb72e5dda7dad6cd44e94a533ad8aa079ad688fbe`

### Kimai
- **MariaDB User**: kimai
- **MariaDB Password**: `Rv9gH_Wp5K3q2DLXc4` (исправлено: `R*v9gH!Wp5K3q2D#LXc4`)
- **MariaDB Root Password**: `1zG8nQ2Va3sL7Yu` (исправлено: `1zG@8nQ2$Va3sL7!Yu`)
- **Admin Email**: konstantin@rmosd.com
- **Admin Password**: `A4guE7sM2xN9Qr5p` (исправлено: `A4g%uE7!sM2#xN9@Qr5p`)

### Taiga
- **PostgreSQL User**: taiga
- **PostgreSQL Password**: `Taiga186!DbPass`
- **RabbitMQ User**: taiga
- **RabbitMQ Password**: `TaigaMqPass!`
- **Secret Key**: `8hw*rkdL0h0&3ntO9cDd^m64yx9bg9s+`
- **Django Superuser**: master / `rXb-8dz-bR3-DQv`
- **Email**: konstantin@rmosd.com / [app-password нужно получить]

### Taiga MCP Bridge
- **Taiga Username**: master
- **Taiga Password**: `rXb-8dz-bR3-DQv`

### Nextcloud (lxc-160)
- **MariaDB User**: ncuser
- **MariaDB Password**: `Maria149DB54StrongPass27`
- **Admin User**: root
- **Admin Password**: `gbW-xK5-Cx8-mLc`

### Telegram Боты
- **Токены ботов**: [требуется получить из переменных окружения в /root/*.env]
- **GitHub PAT**: [требуется получить из конфигураций auto-deploy]

## План миграции

1. **Установить и настроить Vault** (или аналог)
2. **Создать структуру секретов** согласно схеме выше
3. **Перенести все пароли** из этого документа в Vault
4. **Обновить конфигурации сервисов** для использования vault:// ссылок
5. **Протестировать подключения** всех сервисов
6. **Удалить этот файл** после успешной миграции

## Команды для проверки

После миграции проверить доступность всех сервисов:

```bash
# PostgreSQL
pg_isready -h 192.168.1.110

# n8n
curl -f http://192.168.1.120:5678/healthz

# Kimai  
curl -f http://192.168.1.120:8080

# Taiga
curl -f http://192.168.1.120:9000

# Taiga MCP
curl -v -N http://192.168.1.150:8000/sse

# Nextcloud
curl -f http://192.168.1.160
```

## Статус миграции

- [ ] Vault установлен и настроен
- [ ] Структура секретов создана
- [ ] Пароли контейнеров перенесены
- [ ] PostgreSQL credentials перенесены
- [ ] n8n credentials перенесены  
- [ ] Kimai credentials перенесены
- [ ] Taiga credentials перенесены
- [ ] Taiga MCP credentials перенесены
- [ ] Nextcloud credentials перенесены
- [ ] Telegram bot tokens перенесены
- [ ] Конфигурации обновлены
- [ ] Тестирование завершено
- [ ] Файл удалён

---

**Создано:** 2024-12-19  
**⚠️ УДАЛИТЬ ПОСЛЕ МИГРАЦИИ СЕКРЕТОВ**
