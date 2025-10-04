#!/bin/bash

echo "开始安装RabbitMQ (在线方式)..."

# 设置主机名为pyj
echo "设置主机名为pyj..."
sudo hostnamectl set-hostname pyj
echo "当前主机名: $(hostname)"

# 配置hosts文件，确保主机名解析
echo "配置hosts文件..."
sudo bash -c 'cat >> /etc/hosts << EOF
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4 pyj
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6 pyj
$(hostname -I | awk "{print \$1}") pyj
EOF'

# 安装EPEL仓库（提供一些额外依赖包）
sudo yum install -y epel-release

# 安装Erlang和RabbitMQ的Yum仓库
echo "设置Erlang和RabbitMQ仓库..."
curl -s https://packagecloud.io/install/repositories/rabbitmq/erlang/script.rpm.sh | sudo bash
curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.rpm.sh | sudo bash

# 安装Erlang (RabbitMQ的依赖)
echo "安装Erlang..."
sudo yum install -y erlang

# 安装socat (RabbitMQ的依赖)
echo "安装socat..."
sudo yum install -y socat

# 安装RabbitMQ服务器
echo "安装RabbitMQ Server..."
sudo yum install -y rabbitmq-server

# 启动RabbitMQ服务并设置开机自启
echo "启动RabbitMQ服务..."
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server

# 等待RabbitMQ节点启动完成
echo "等待RabbitMQ节点启动..."
sudo rabbitmqctl wait /var/lib/rabbitmq/mnesia/rabbit@pyj.pid

# 启用管理插件
echo "启用管理插件..."
sudo rabbitmq-plugins enable rabbitmq_management

# 创建arlv2host虚拟主机
echo "创建arlv2host虚拟主机..."
sudo rabbitmqctl add_vhost arlv2host

# 创建arl用户
echo "创建arl用户..."
sudo rabbitmqctl add_user arl arlpassword

# 为arl用户设置arlv2host虚拟主机的权限
echo "设置arl用户在arlv2host虚拟主机的权限..."
sudo rabbitmqctl set_permissions -p arlv2host arl ".*" ".*" ".*"

# 为arl用户设置默认虚拟主机的权限（可选，用于管理界面访问）
echo "设置arl用户在默认虚拟主机的权限..."
sudo rabbitmqctl set_permissions -p "/" arl ".*" ".*" ".*"

# 将arl用户设置为管理员标签
echo "设置arl用户为管理员..."
sudo rabbitmqctl set_user_tags arl administrator

# 重启RabbitMQ服务使配置生效
sudo systemctl restart rabbitmq-server

# 再次等待RabbitMQ节点启动完成
echo "等待RabbitMQ节点重新启动..."
sudo rabbitmqctl wait /var/lib/rabbitmq/mnesia/rabbit@pyj.pid

# 放行防火墙端口（5672: RabbitMQ服务端口, 15672: 管理界面端口）
echo "配置防火墙..."
sudo firewall-cmd --zone=public --add-port=5672/tcp --permanent
sudo firewall-cmd --zone=public --add-port=15672/tcp --permanent
sudo firewall-cmd --reload

echo "=================================================="
echo "RabbitMQ安装完成！"
echo "管理界面: http://$(hostname -I | awk '{print $1}'):15672"
echo "节点名称: rabbit@pyj"
echo "虚拟主机: arlv2host"
echo "用户名: arl"
echo "密码: arlpassword"
echo "=================================================="