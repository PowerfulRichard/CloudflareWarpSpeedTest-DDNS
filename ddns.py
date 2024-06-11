import os, random, ipaddress, subprocess, csv, re, requests, json

def is_ipv6(address):
    # 匹配IPv6地址的正则表达式
    ipv6_pattern = r'\[?([0-9a-fA-F:]+)\]?'  # 匹配带或不带方括号的IPv6地址

    # 匹配包含端口的正则表达式
    port_pattern = r':\d+$'  # 匹配冒号后面的数字

    # 检查是否是IPv6地址
    if re.match(ipv6_pattern, address):
        # 如果包含端口，则删除端口和方括号
        if re.search(port_pattern, address):
            address = re.sub(port_pattern, '', address)  # 删除端口
            address = re.sub(r'\[|\]', '', address)  # 删除方括号
        return address
    else:
        return None

# 检测文件是否存在
if not os.path.exists("ips-v6.txt"):
    print("Error: 文件 'ips-v6.txt' 不存在！")
    exit()

# 读取IPv6地址前缀和子网长度
with open("ips-v6.txt", "r") as f:
    ipv6_prefixes = f.readlines()

# 移除行末的换行符并解析为IPv6网络对象
ipv6_networks = [ipaddress.IPv6Network(prefix.strip()) for prefix in ipv6_prefixes]

# 随机生成15个IPv6地址
ipv6_addresses = []
for network in ipv6_networks:
    for _ in range(5):
        ipv6_addresses.append(str(network.network_address + random.randint(0, 2**(112 - network.prefixlen) - 1)))

# 保存为ip.txt
with open("ip.txt", "w") as f:
    f.write("\n".join(ipv6_addresses))

print("已生成并保存IPv6地址到 'ip.txt' 文件中。")

# 执行系统命令并实时输出
command = r".\CloudflareWarpSpeedTest.exe -p 0 -f ip.txt -tlr 0 -o ipv6.csv"
# command = r".\warp.exe -output ipv6.csv" ### 需要格式化ip.txt地址
process = subprocess.Popen(["powershell", "-Command", command])

# 等待命令执行完成
process.wait()

# 打开csv文件
with open('ipv6.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)    # 创建一个csv读取器
    next(reader)                    # 跳过第一行
    second_row = next(reader)       # 读取第二行
    addr = is_ipv6(second_row[0])   # 获取第二行的第一个值

token="Bearer XXXXXXXXXXXXXXXXXXXXXXX"  #填写API token(40位)
zone_id="XXXXXXXXXXXXXXXXXXXXXXXXX"     #填写zone ID(32位,详见https://developers.cloudflare.com/api/operations/zones-get)
dns_id="XXXXXXXXXXXXXXXXXXXXXXXX"       #填写dns ID(32位，详见https://developers.cloudflare.com/api/operations/zones-0-get)
url = "https://api.cloudflare.com/client/v4/zones/"+zone_id+"/dns_records/"+dns_id
payload = {
    "content": addr,
    "name": "XXX.XXX.XXX",  #填写ddns域名
    "proxied": False,
    "type": "AAAA",         #ipv4地址填A，ipv6地址填AAAA
    "ttl": 1
}
headers = {
    "Content-Type": "application/json",
    "Authorization": token
}

response = requests.request("PATCH", url, json=payload, headers=headers)

# 解析 JSON
response_dict = json.loads(response.text)

# 提取 "success" 值
suc = response_dict.get("success", False)

if suc:
    # 如果修改成功
    name = response_dict["result"]["name"]
    content = response_dict["result"]["content"]
    print(f"修改成功！'{name}'的记录已修改为 '{content}'")
else:
    print("修改失败！")
