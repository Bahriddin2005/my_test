# Deployment Checklist

## Before Deployment
- [ ] Update ALLOWED_HOSTS in settings.py with your domain
- [ ] Set DEBUG = False
- [ ] Create .env file with secure SECRET_KEY
- [ ] Update domain names in nginx.conf
- [ ] Update server IP in deploy.sh

## Server Setup
- [ ] Run: `bash server_setup.sh`
- [ ] Configure domain DNS to point to server IP
- [ ] Run: `bash deploy.sh`

## SSL Setup
- [ ] Run: `sudo certbot --nginx -d your-domain.com -d www.your-domain.com`
- [ ] Test SSL: `sudo certbot renew --dry-run`

## Final Checks
- [ ] Test website: `curl -I https://your-domain.com`
- [ ] Check services: `sudo systemctl status mytest nginx`
- [ ] Monitor logs: `sudo journalctl -f -u mytest`

## Maintenance Commands
```bash
# Restart services
sudo systemctl restart mytest nginx

# Update code
git pull origin main
sudo systemctl restart mytest

# Check logs
sudo journalctl -u mytest -f
sudo tail -f /var/log/nginx/error.log
```