# 🌐 Gebruiker Toegang - Snipe-IT Purchase Order Tool

## Toegang tot de PO Tool

### Optie 1: IP-adres (Direct)
```
http://192.168.211.22:5001
```

### Optie 2: Lokale naam (Aanbevolen)
Voor gebruikers die een makkelijk te onthouden naam willen:

**Windows hosts file aanpassen:**
1. Open Notepad als **Administrator**
2. Open bestand: `C:\Windows\System32\drivers\etc\hosts`
3. Voeg deze regel toe:
   ```
   192.168.211.22    po-tool-prod.local
   ```
4. Sla het bestand op

**Daarna toegang via:**
```
http://po-tool-prod.local:5001
```

## ⚠️ Belangrijk
- Gebruik altijd **http://** (niet https://)
- Vergeet de poort **:5001** niet
- De tool werkt alleen binnen het bedrijfsnetwerk

## 🔧 Voor IT Beheerders

### Service beheer:
```bash
# Status controleren
sudo systemctl status snipe-po-tool

# Herstarten na configuratie wijzigingen
sudo systemctl restart snipe-po-tool

# Logs bekijken
sudo journalctl -u snipe-po-tool -f
```

### Configuratie:
```bash
sudo nano /opt/snipe-po-tool/.env
```

Na wijzigingen altijd herstarten:
```bash
sudo systemctl restart snipe-po-tool
```
