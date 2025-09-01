# Пример карточки сервиса

### telegram-notifier

**Назначение:** Telegram-бот для отправки уведомлений о состоянии инфраструктуры и алертов от систем мониторинга

**Расположение:** 
- Контейнер: lxc-102-bots
- URL: N/A (только Telegram API)

**Интерфейсы/Порты:** 
- 8080/HTTP — webhook для приема уведомлений от внешних систем
- 443/HTTPS — исходящие запросы к Telegram API

**Данные:** 
- `/opt/telegram-bot/data` — база данных пользователей (SQLite)
- `/opt/telegram-bot/logs` — логи работы бота
- `/opt/telegram-bot/config` — конфигурационные файлы

**Зависимости:** 
- Telegram Bot API — отправка сообщений
- Grafana — получение алертов через webhook
- Prometheus — получение метрик через API
- SQLite — хранение настроек пользователей

**Конфигурация/переменные:** 
- Основная конфигурация: `/opt/telegram-bot/config/bot.yml`
- Секреты: vault://bots/telegram-notifier (токен бота, API ключи)

**Мониторинг/здоровье:** 
- Проверка: `curl -f http://localhost:8080/health`
- Метрики: Prometheus endpoint на `/metrics`
- Логи: `journalctl -u telegram-bot -f`

## Операции

### Обновление
1. Создать бэкап базы данных: `cp /opt/telegram-bot/data/bot.db /opt/telegram-bot/data/bot.db.backup.$(date +%Y%m%d)`
2. Остановить сервис: `systemctl stop telegram-bot`
3. Обновить код: `cd /opt/telegram-bot && git pull origin main`
4. Установить зависимости: `pip install -r requirements.txt`
5. Применить миграции: `python manage.py migrate`
6. Запустить сервис: `systemctl start telegram-bot`
7. Проверить health check: `curl -f http://localhost:8080/health`

### Бэкап/восстановление
1. Остановить бот: `systemctl stop telegram-bot`
2. Создать бэкап БД: `tar -czf telegram-bot-$(date +%Y%m%d).tar.gz /opt/telegram-bot/data`
3. Создать бэкап конфигурации: `cp -r /opt/telegram-bot/config /backup/telegram-bot-config-$(date +%Y%m%d)`
4. Для восстановления: остановить сервис
5. Восстановить данные: `tar -xzf telegram-bot-YYYYMMDD.tar.gz -C /`
6. Восстановить конфигурацию: `cp -r /backup/telegram-bot-config-YYYYMMDD /opt/telegram-bot/config`
7. Запустить и проверить: `systemctl start telegram-bot && curl -f http://localhost:8080/health`

### Проверка после действий
- HTTP 200 на `/health` endpoint
- Отправка тестового сообщения в служебный чат
- Проверка логов на отсутствие ошибок за последние 5 минут
- Проверка подключения к Telegram API
- Проверка получения webhook'ов от Grafana

**Известные грабли:**
- При обновлении Python зависимостей может сломаться виртуальное окружение — пересоздать venv
- Telegram API иногда блокирует запросы при превышении rate limit — добавлены задержки
- SQLite база может заблокироваться при одновременных операциях — использовать WAL режим
- Webhook endpoint может не отвечать после обновления nginx — проверить proxy_pass конфигурацию

**Обновлено:** 2024-12-19

---

*Это пример полностью заполненной карточки сервиса с детальным runbook. Обратите внимание на конкретные команды и проверки.*
