#!/bin/bash
# Nginx 安装配置脚本 for CentOS 8
# 版本: 2.0 - 修复 SELinux 问题

set -e  # 遇到错误立即退出

# 安装 Nginx
echo "安装 Nginx..."
dnf install -y epel-release
dnf install -y nginx

# 创建必要的目录结构
mkdir -p /etc/ssl/certs /var/log/nginx /opt/web/frontend

# 生成 SSL 证书
echo "生成 SSL 证书..."
openssl genrsa -out /etc/ssl/certs/arl_web.key 2048 2>/dev/null

cat > /tmp/arl_ssl.conf << EOF
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
prompt = no
[req_distinguished_name]
C = CN
ST = State
L = City
O = Organization
CN = ARL Web
[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = localhost
IP.1 = 127.0.0.1
EOF

openssl req -new -key /etc/ssl/certs/arl_web.key -out /tmp/arl_web.csr -config /tmp/arl_ssl.conf
openssl x509 -req -days 365 -in /tmp/arl_web.csr -signkey /etc/ssl/certs/arl_web.key -out /etc/ssl/certs/arl_web.crt

# 下载 dhparam.pem
echo "下载 DH parameters..."
curl -s https://ssl-config.mozilla.org/ffdhe2048.txt -o /etc/ssl/certs/dhparam.pem

# 设置证书权限
chmod 600 /etc/ssl/certs/arl_web.key
chmod 644 /etc/ssl/certs/arl_web.crt /etc/ssl/certs/dhparam.pem

# 修复 SELinux 上下文
echo "配置 SELinux..."
if command -v semanage >/dev/null 2>&1; then
    # 安装 SELinux 管理工具
    dnf install -y policycoreutils-python-utils
    
    # 设置 SSL 证书文件的 SELinux 上下文
    semanage fcontext -a -t etc_t "/etc/ssl/certs/arl_web.key"
    semanage fcontext -a -t etc_t "/etc/ssl/certs/arl_web.crt"
    semanage fcontext -a -t etc_t "/etc/ssl/certs/dhparam.pem"
    
    # 恢复上下文
    restorecon -Rv /etc/ssl/certs/
    
    # 允许 Nginx 访问网络
    setsebool -P httpd_can_network_connect 1
    
    echo "SELinux 已配置"
else
    # 如果 semanage 不可用，临时禁用 SELinux
    echo "警告: semanage 不可用，临时禁用 SELinux"
    setenforce 0
    # 建议永久禁用（可选，生产环境不推荐）
    sed -i 's/SELINUX=enforcing/SELINUX=permissive/g' /etc/selinux/config
fi

# 创建 ARL Nginx 配置
echo "创建 Nginx 配置..."
cat > /etc/nginx/conf.d/arl.conf << 'EOF'
server {
    listen 5003 ssl http2;
    server_name _;
    ssl_certificate /etc/ssl/certs/arl_web.crt;
    ssl_certificate_key /etc/ssl/certs/arl_web.key;
    ssl_session_timeout 1d;
    ssl_session_cache shared:MozSSL:10m;
    ssl_session_tickets off;
    ssl_dhparam /etc/ssl/certs/dhparam.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    add_header Strict-Transport-Security "max-age=63072000" always;
    access_log /var/log/nginx/arl.access.log;
    error_log /var/log/nginx/arl.error.log;
    root /opt/web/frontend;

    location / {
        try_files $uri $uri/ /index.html;
        index index.html index.htm;
    }

    location /api/ {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:5013/api/;
    }

    location /swaggerui/ {
        proxy_set_header X-Real-IP $remote_addr;
        proxy_pass http://127.0.0.1:5013/swaggerui/;
    }

    error_page 497 https://$http_host;
}
EOF

# 创建默认首页（避免 403 错误）
echo "创建默认页面..."
cat > /opt/web/frontend/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>ARL System</title>
</head>
<body>
    <h1>ARL System</h1>
    <p>Nginx is running correctly.</p>
    <p>ARL frontend will be deployed here.</p>
</body>
</html>
EOF

# 设置目录权限
chown -R nginx:nginx /opt/web/frontend
chmod 755 /opt/web/frontend /opt/web/frontend/index.html

# 验证 Nginx 配置
echo "验证 Nginx 配置..."
nginx -t

if [ $? -ne 0 ]; then
    echo "Nginx 配置验证失败，请检查配置文件"
    exit 1
fi

# 配置防火墙
if systemctl is-active --quiet firewalld; then
    echo "配置防火墙..."
    firewall-cmd --permanent --add-service=http
    firewall-cmd --permanent --add-service=https
    firewall-cmd --permanent --add-port=5003/tcp
    firewall-cmd --reload
    echo "防火墙已配置"
fi

# 启动并启用 Nginx 服务
echo "启动 Nginx 服务..."
systemctl enable nginx
systemctl start nginx

# 等待服务启动
sleep 3

# 验证服务状态
if systemctl is-active --quiet nginx; then
    echo "✓ Nginx 服务运行正常"
else
    echo "✗ Nginx 服务启动失败"
    echo "检查日志: journalctl -u nginx -n 50"
    exit 1
fi

# 验证端口监听
if netstat -tlnp | grep nginx | grep 5003 > /dev/null; then
    echo "✓ Nginx 正在监听 5003 端口"
else
    echo "✗ Nginx 未在 5003 端口监听"
    echo "检查配置: nginx -T | grep 5003"
fi

# 清理临时文件
rm -f /tmp/arl_web.csr /tmp/arl_ssl.conf

echo "========================================"
echo "Nginx 安装完成!"
echo "ARL 访问地址: https://$(hostname -I | awk '{print $1}'):5003"
echo ""
echo "服务管理命令:"
echo "启动: systemctl start nginx"
echo "停止: systemctl stop nginx"
echo "重启: systemctl restart nginx"
echo "状态: systemctl status nginx"
echo "重载配置: nginx -s reload"
echo ""
echo "如果无法访问，请检查:"
echo "1. SELinux 状态: sestatus"
echo "2. 防火墙状态: firewall-cmd --list-all"
echo "3. Nginx 日志: tail -f /var/log/nginx/arl.error.log"
echo "========================================"