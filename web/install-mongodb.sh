#!/bin/bash
# MongoDB 安装脚本 for CentOS 8 - 修复版（支持重启后自动启动）

# 配置 MongoDB 4.0 仓库
cat > /etc/yum.repos.d/mongodb-org-4.0.repo << EOF
[mongodb-org-4.]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/8/mongodb-org/4.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-4.0.asc
EOF

# 安装 MongoDB
dnf install -y mongodb-org-server mongodb-org-shell

if [ $? -ne 0 ]; then
    echo "MongoDB 安装失败，请检查网络连接和代理设置"
    exit 1
fi

# 创建数据目录并设置权限
mkdir -p /var/lib/mongo /var/log/mongodb /var/run/mongodb
chown -R mongod:mongod /var/lib/mongo /var/log/mongodb /var/run/mongodb
chmod 755 /var/lib/mongo /var/log/mongodb /var/run/mongodb

# 配置 MongoDB（使用 fork 模式以兼容 systemd）
cat > /etc/mongod.conf << EOF
storage:
  dbPath: /var/lib/mongo
  journal:
    enabled: true
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log
  logRotate: reopen
net:
  port: 27017
  bindIp: 0.0.0.0
processManagement:
  fork: true
  pidFilePath: /var/run/mongodb/mongod.pid
security:
  authorization: disabled
EOF

# 修复 SELinux 上下文（如果启用了 SELinux）
if command -v semanage >/dev/null 2>&1; then
    semanage fcontext -a -t mongod_var_lib_t "/var/lib/mongo(/.*)?"
    semanage fcontext -a -t mongod_log_t "/var/log/mongodb(/.*)?"
    restorecon -Rv /var/lib/mongo /var/log/mongodb
else
    # 临时禁用 SELinux（重启后恢复）
    setenforce 0
fi

# 创建正确的 systemd 服务文件
cat > /usr/lib/systemd/system/mongod.service << 'EOF'
[Unit]
Description=MongoDB Database Server
Documentation=https://docs.mongodb.org/manual
After=network.target

[Service]
User=mongod
Group=mongod
Environment="OPTIONS=-f /etc/mongod.conf"
EnvironmentFile=-/etc/sysconfig/mongod
ExecStart=/usr/bin/mongod $OPTIONS
ExecStartPre=/usr/bin/mkdir -p /var/run/mongodb
ExecStartPre=/usr/bin/chown mongod:mongod /var/run/mongodb
ExecStartPre=/usr/bin/chmod 0755 /var/run/mongodb
PermissionsStartOnly=true
PIDFile=/var/run/mongodb/mongod.pid
Type=forking
# file size
LimitFSIZE=infinity
# cpu time
LimitCPU=infinity
# virtual memory size
LimitAS=infinity
# open files
LimitNOFILE=64000
# processes/threads
LimitNPROC=64000
# locked memory
LimitMEMLOCK=infinity
# total threads (user+kernel)
TasksMax=infinity
TasksAccounting=false

[Install]
WantedBy=multi-user.target
EOF

# 重新加载 systemd 并启用服务
systemctl daemon-reload
systemctl enable mongod

# 启动 MongoDB 服务
echo "启动 MongoDB 服务..."
systemctl start mongod

# 等待启动
for i in {1..30}; do
    if systemctl is-active --quiet mongod; then
        echo "MongoDB 启动成功"
        break
    fi
    echo "等待 MongoDB 启动... ($i/30)"
    sleep 2
done

# 检查 MongoDB 是否运行
if ! systemctl is-active --quiet mongod; then
    echo "MongoDB systemd 服务启动失败，尝试直接启动..."
    
    # 尝试直接启动
    sudo -u mongod mongod --config /etc/mongod.conf --fork --logpath /var/log/mongodb/mongod.log
    sleep 5
fi

# 检查 MongoDB 端口是否监听
if netstat -tlnp | grep 27017 > /dev/null; then
    echo "MongoDB 正在运行，端口 27017 已监听"
else
    echo "MongoDB 启动失败，请检查："
    echo "1. 磁盘空间: df -h"
    echo "2. 内存情况: free -h"
    echo "3. 查看详细日志: journalctl -u mongod -n 50"
    echo "4. 查看 MongoDB 日志: tail -50 /var/log/mongodb/mongod.log"
    exit 1
fi

# 初始化 ARL 数据库和用户
echo "正在初始化 ARL 数据库..."

# 增加等待时间确保 MongoDB 完全启动
sleep 8

# 使用更健壮的数据库初始化方式
mongo --verbose --eval "
print('开始初始化 ARL 数据库...');

// 方法1：先创建数据库，再使用
print('1. 创建 arl 数据库...');
db = db.getSiblingDB('arl');
print('当前数据库: ' + db.getName());

// 确保数据库被创建（通过插入数据）
print('2. 创建 user 集合并插入数据...');
try {
    // 先删除已存在的集合（如果有）
    db.user.drop();
    print(' - 清理旧 user 集合完成');
} catch (e) {
    print(' - 无需清理旧集合: ' + e);
}

// 插入数据来真正创建集合
var insertResult = db.user.insert({
    username: 'pyj',
    password: '$(echo -n 'arlsalt!@#pyj@admin' | md5sum | cut -d' ' -f1)',
    created_at: new Date(),
    role: 'administrator'
});

print('3. 验证创建结果:');
print(' - 插入结果: ' + JSON.stringify(insertResult));
print(' - 数据库名称: ' + db.getName());
print(' - 集合列表: ' + JSON.stringify(db.getCollectionNames()));
print(' - User 集合文档数量: ' + db.user.count());

// 显示创建的用户数据
print('4. 用户数据详情:');
db.user.find().forEach(function(doc) {
    printjson(doc);
});

print('5. 最终验证 - 所有数据库:');
db.getSiblingDB('admin').adminCommand({listDatabases: 1}).databases.forEach(function(d) {
    if (d.name === 'arl') {
        print('   ✓ ' + d.name + ' 数据库已创建 (大小: ' + d.sizeOnDisk + ' bytes)');
    }
});

print('ARL 数据库初始化完成！');
"

# 配置防火墙
if systemctl is-active --quiet firewalld; then
    firewall-cmd --permanent --add-port=27017/tcp
    firewall-cmd --reload
    echo "防火墙已配置，开放 27017 端口"
fi

# 验证 systemd 服务状态
echo "验证 MongoDB 系统服务状态..."
systemctl status mongod --no-pager

# 确认开机启动已启用
if systemctl is-enabled mongod >/dev/null 2>&1; then
    echo "✓ MongoDB 已配置为开机自动启动"
else
    echo "✗ MongoDB 开机自动启动配置失败，请手动执行: systemctl enable mongod"
fi

echo "========================================"
echo "MongoDB 安装完成!"
echo "连接信息:"
echo "主机: $(hostname -I | awk '{print $1}') 或 127.0.0.1"
echo "端口: 27017" 
echo "数据库: arl"
echo "认证: 无"
echo ""
echo "ARL 登录账号:"
echo "用户名: pyj"
echo "密码: pyj@admin"
echo ""
echo "管理命令:"
echo "启动: systemctl start mongod"
echo "停止: systemctl stop mongod"
echo "状态: systemctl status mongod"
echo "重启: systemctl restart mongod"
echo "查看日志: journalctl -u mongod -f"
echo ""
echo "然后使用: mongo 127.0.0.1/arl"
echo "========================================"