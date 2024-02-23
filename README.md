## 介绍
使用[CloudflareWarpSpeedTest](https://github.com/peanut996/CloudflareWarpSpeedTest)工具优选WARP IP后自动DDNS到Cloudflare

## 软件依赖
* Python（测试版本为3.9）
* requests库（安装python后执行`pip install requests`）
* [peanut996/CloudflareWarpSpeedTest](https://github.com/peanut996/CloudflareWarpSpeedTest/releases)测速工具
* IPv6网络连接

## 配置
1. 修改`ddns.py`第35行range(n)中n的值可以修改生成/测速ip地址数量，生成数量为2n
2. 根据[官方文档](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)生成API令牌，填入第59行的token变量处，注意变量前缀`Bearer `不可删除
3. 根据[API文档](https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids/)查看ddns域名的`zone_id`和`dns_id`，填入第60,61行
4. 在65行填入`dns_id`对应的域名

## 使用
1. 确保`ddns.py`已按照`配置`中的提示修改，
2. 单次运行`python ddns.py`
3. 如需定时运行，可将`单次运行命令`填入系统定时操作中，脚本会自动覆盖上一次的数据

## 链接
* [peanut996/CloudflareWarpSpeedTest](https://github.com/peanut996/CloudflareWarpSpeedTest)
* [XIU2/CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest)
* [CloudFlare文档](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-patch-dns-record)
