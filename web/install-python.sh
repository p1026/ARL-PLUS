#!/bin/bash
# ARL 系统环境配置脚本 - CentOS专用 Python 3.8

RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
RESET='\033[0m'

echo -e "${BLUE}ARL 系统环境配置脚本 - CentOS Python 3.8${RESET}"
echo "===================================================="

# 检查系统
if [ ! -f /etc/redhat-release ]; then
    echo -e "${RED}错误：此脚本仅适用于 CentOS 系统${RESET}"
    exit 1
fi

# 安装系统依赖
echo -e "${YELLOW}安装系统依赖...${RESET}"
yum install -y epel-release
yum groupinstall -y "Development Tools"
yum install -y python38 python38-devel openssl-devel libffi-devel gcc-c++ make krb5-devel wget curl git

# 安装 Python 3.8
if ! command -v python3.8 &> /dev/null; then
    echo -e "${YELLOW}安装 Python 3.8...${RESET}"
    yum install -y python38
    if [ -f /usr/bin/python38 ] && [ ! -f /usr/bin/python3.8 ]; then
        ln -s /usr/bin/python38 /usr/bin/python3.8
    fi
else
    echo -e "${GREEN}Python 3.8 已安装: $(python3.8 --version 2>&1)${RESET}"
fi

# 安装 pip3.8
echo -e "${YELLOW}安装 pip3.8...${RESET}"
wget -q https://bootstrap.pypa.io/pip/3.8/get-pip.py -O get-pip.py
python3.8 get-pip.py
rm -f get-pip.py

# 升级 pip 到最新版本
echo -e "${YELLOW}升级 pip 到最新版本...${RESET}"
pip3.8 install --upgrade pip

# 设置目录权限
echo -e "${YELLOW}设置 /opt/web/app/tools 目录及子目录下所有文件可执行权限...${RESET}"
if [ -d "/opt/web/app/tools" ]; then
    find /opt/web/app/tools -type f -exec chmod +x {} \;
    echo -e "${GREEN}/opt/web/app/tools 目录及子目录下所有文件已设置为可执行${RESET}"
else
    echo -e "${YELLOW}目录 /opt/web/app/tools 不存在，跳过权限设置${RESET}"
fi

# 解决xray报错：创建 libpcap 库软链接
echo -e "${YELLOW}设置 libpcap 库软链接...${RESET}"
if [ -f "/usr/lib64/libpcap.so.1.9.1" ]; then
    cd /usr/lib64 || {
        echo -e "${RED}无法进入 /usr/lib64 目录${RESET}"
        exit 1
    }
    if ln -s libpcap.so.1.9.1 libpcap.so.0.8 2>/dev/null; then
        echo -e "${GREEN}libpcap 软链接已创建: libpcap.so.1.9.1 -> libpcap.so.0.8${RESET}"
    else
        echo -e "${YELLOW}软链接可能已存在，跳过创建${RESET}"
    fi
else
    echo -e "${YELLOW}文件 /usr/lib64/libpcap.so.1.9.1 不存在，跳过软链接创建${RESET}"
fi

# 安装 nmap
echo -e "${YELLOW}安装 nmap...${RESET}"
yum install -y nmap
if command -v nmap &> /dev/null; then
    echo -e "${GREEN}nmap 安装成功: $(nmap --version 2>&1 | head -n 1)${RESET}"
else
    echo -e "${RED}nmap 安装失败${RESET}"
fi

# 验证环境
echo -e "${YELLOW}环境验证...${RESET}"
echo "Python: $(python3.8 --version 2>&1)"
echo "Pip: $(pip3.8 --version)"

echo -e "${GREEN}系统环境配置完成！${RESET}"
echo -e "${YELLOW}注意：已移除自动安装 pip 软件包的功能${RESET}"