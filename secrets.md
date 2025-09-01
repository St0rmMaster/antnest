# Секреты и пароли

## Контейнеры LXC (root)
- **lxc-110-databases**: GgQ-4p9-zG3-XZk
- **lxc-120-n8n**: h4j-VLN-NdN-Avj  
- **lxc-130**: w32-SQU-3TY-BeW
- **lxc-140-gigabot**: Z2T-djm-5Aw-QST
- **lxc-150-mcp-taiga**: [не указан]
- **lxc-160-cloud**: afx-Tjc-jVc-6b3

## PostgreSQL (192.168.1.110:5432)
- **appuser**: S3cureLONGPass!
- **n8nuser**: N8nDBPass!
- **germanbot**: StrongGermanPass!
- **cardiobot**: StrongCardioPass!
- **mamontovuser**: MamontovDBPass!

## n8n
- **basic-auth**: admin / djx-ExM-s6A-jVy1!
- **api-key**: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkYTVhYWEwZC1jYjNiLTRlODItYmIzZS03OTRjMGI0OWNjZDAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzU0NzgwODAxfQ._hkE50LwSiqvU48Vd8hunutZWDFU3dAy7KvjCbi8rzQ
- **mcp-auth-token**: 56981a88168527130cc9a76bb72e5dda7dad6cd44e94a533ad8aa079ad688fbe

## Kimai
- **mariadb-user**: kimai
- **mariadb-password**: R*v9gH!Wp5K3q2D#LXc4
- **mariadb-root**: 1zG@8nQ2$Va3sL7!Yu
- **admin-email**: konstantin@rmosd.com
- **admin-password**: A4g%uE7!sM2#xN9@Qr5p

## Taiga
- **postgres-user**: taiga
- **postgres-password**: Taiga186!DbPass
- **rabbitmq-user**: taiga
- **rabbitmq-password**: TaigaMqPass!
- **secret-key**: 8hw*rkdL0h0&3ntO9cDd^m64yx9bg9s+
- **django-superuser**: master / rXb-8dz-bR3-DQv
- **email**: konstantin@rmosd.com
- **email-password**: [app-password нужно получить]

## Taiga MCP Bridge
- **taiga-username**: master
- **taiga-password**: rXb-8dz-bR3-DQv

## Nextcloud (lxc-160)
- **mariadb-user**: ncuser
- **mariadb-password**: Maria149DB54StrongPass27
- **admin-user**: root
- **admin-password**: gbW-xK5-Cx8-mLc

## Telegram боты
- **german-bot-token**: [из /root/german.env]
- **cardio-bot-token**: [из /root/cardio.env]
- **mamontov-bot-token**: [из /root/mamontov.env]
- **github-pat**: [для auto-deploy]

## Строки подключения
- **PostgreSQL n8n**: postgresql://n8nuser:N8nDBPass!@192.168.1.110:5432/n8n
- **Kimai MariaDB**: mysql://kimai:R*v9gH!Wp5K3q2D#LXc4@db/kimai?charset=utf8mb4&serverVersion=11
