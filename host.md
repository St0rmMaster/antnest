# Хост — Proxmox VE (pve)

**Назначение:** Основной хост виртуализации для продакшн-среды, разворачивание LXC контейнеров

**Железо:** 
- CPU: AMD FX-6300 Six-Core Processor (6 ядер, 3.5GHz)
- RAM: 13Gi (доступно)
- Материнка: Gigabyte 970A-DS3P
- GPU: AMD Radeon RX 460/560D
- Диски: 
  - sda: 3.6TB HDD (/mnt/storage)
  - sdb: 931.5GB SSD (fastpool ZFS)
  - sdc: 223.6GB SSD (система + local-lvm)
  - sdd: 931.5GB SSD (fastpool ZFS)

**Сеть:** 
- LAN IP: 192.168.1.253/24
- Внешний доступ: AT&T модем, проброшены TCP 80/443
- Hair-pin NAT: отсутствует (решено через dnsmasq)

**Хранилища:** 
- **local**: /var/lib/vz (57GB, системные файлы PVE)
- **local-lvm**: thin LVM на sdc3 (130GB, тестовые ВМ)
- **fastpool**: ZFS RAID-0 на sdb1+sdd1 (927GB, основные диски ВМ/LXC)
- **filestorage**: /mnt/storage на sda1 (3.36TB, ISO, шаблоны, бэкапы)
- **tplpool**: /fastpool/lxc-templates (927GB, шаблоны LXC/ISO)

**Службы на хосте:**
- **nginx 1.22.1**: reverse-proxy + certbot сертификаты
  - pve.gramini.org → 127.0.0.1:8006 (Proxmox админка)
  - n8n.gramini.org → 192.168.1.120:5678 (n8n)
  - SSL: /etc/letsencrypt/live/.../fullchain.pem
- **dnsmasq**: split-DNS (address=/n8n.gramini.org/192.168.1.120)
- **PVE-Firewall**: ACCEPT TCP 22,80,443 из любого; остальное DROP

**Известные грабли:**
- Hair-pin NAT отсутствует — решено через dnsmasq split-DNS
- При обновлении ядра могут не подниматься сетевые интерфейсы
- Postgres в хосте мешал контейнерам — удалили пакеты
- Certbot ошибки NXDOMAIN — исправили DNS и путь к fullchain.pem

**Обновлено:** 2024-12-19
