import random
import requests
from datetime import datetime, timedelta

# ---------------- 配置 ----------------
URL = "https://hoyt-lawyerly-echoingly.ngrok-free.dev/api/repairs"
COUNT = 63
PHONE_FILM_COUNT = 31  # 手机贴膜数量

LOCATIONS = ["工学馆", "鹏四4331", "校五5508"]
TYPES = ["电脑清灰", "手机贴膜", "小电子设备维修", "其他"]

# 问题描述库
OTHER_PROBLEMS = [
    "电脑无法开机","系统卡顿","风扇异响","键盘失灵","屏幕闪烁","USB接触不良",
    "网页打不开","系统更新失败","软件报错","启动缓慢","蓝屏重启","鼠标漂移",
    "电池异常","WiFi断连","系统语言错乱","程序闪退","显示器异常","系统损坏",
    "摄像头失效","驱动失败","耳机无声","开机卡死","过热关机","风扇转速异常",
    "分辨率异常","触控板失灵","程序无法卸载","桌面消失","蓝牙失效","时间错误",
    "无声音","显示偏色","开机卡顿","网络延迟","电源问题","硬盘异常","内存错误",
    "软件闪退","驱动冲突","屏幕花屏","键盘短路","电池膨胀","接口接触不良","打印机故障",
    "显示器黑屏","摄像头模糊","音响无声","风扇噪音","系统崩溃","蓝牙无法连接",
    "触摸失效","USB无法识别","散热异常","系统时间错误","无法升级","程序安装失败",
    "无线网不稳定"
]

# 生成63个不重复的中文名（两字或三字）
SURNAMES = list("赵钱孙李周吴郑王冯陈蒋沈韩杨朱秦尤许何吕张孔曹严华")
GIVEN_NAMES = list("一二三四五六七八九子文浩然宇轩明哲嘉豪梓涵雨婷晓丽晨轩梦琪")
names_set = set()
while len(names_set) < COUNT:
    if random.random() < 0.5:
        name = random.choice(SURNAMES) + random.choice(GIVEN_NAMES)  # 两字
    else:
        name = random.choice(SURNAMES) + random.choice(GIVEN_NAMES) + random.choice(GIVEN_NAMES)  # 三字
    names_set.add(name)
NAMES = list(names_set)

# ---------------- 工具函数 ----------------
def random_phone():
    prefix = random.choice([
        "130","131","132","133","135","136","137","138","139",
        "150","151","152","157","158","159",
        "170","171","172","173","175","176","177","178",
        "180","181","182","183","185","186","187","188","189"
    ])
    return prefix + "".join(random.choice("0123456789") for _ in range(8))

def random_email():
    t = random.choice([0,1,2])
    if t == 0:
        return ""
    suffix = "@qq.com" if t==1 else "@163.com"
    number = str(random.randint(10000,9999999))
    return number + suffix

def random_datetime(start, end):
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    dt = start + timedelta(seconds=seconds)
    # 调整时间集中在 10:00-14:00 和 17:40-22:00
    if random.random() < 0.5:
        hour = random.randint(10,13)
        minute = random.randint(0,59)
    else:
        hour = random.randint(17,22)
        minute = random.randint(40,59) if hour == 17 else random.randint(0,59)
    dt = dt.replace(hour=hour, minute=minute, second=random.randint(0,59))
    return dt

# ---------------- 生成时间 ----------------
start = datetime(2025,9,15)
end   = datetime(2025,12,15)
times = [random_datetime(start, end) for _ in range(COUNT)]

# ---------------- 提交 ----------------
for i in range(COUNT):
    # 判断类型
    if i < PHONE_FILM_COUNT:
        service = "手机贴膜"
        phone_models = ["iPhone 14","iPhone 13","小米13","华为P50","OPPO Reno9","vivo X90"]
        description = random.choice(phone_models) + " 已自带膜"
    else:
        service = random.choice(["电脑清灰","小电子设备维修","其他"])
        description = random.choice(OTHER_PROBLEMS)
    
    data = {
        "name": NAMES[i],
        "phone": random_phone(),
        "email": random_email(),
        "service": service,
        "description": description,
        "date": times[i].strftime("%Y-%m-%d %H:%M:%S"),
        "location": random.choice(LOCATIONS)
    }

    print(f"[{i+1}] 提交：", data)
    try:
        res = requests.post(URL, json=data, timeout=5)
        print("结果：", res.status_code, res.text)
    except Exception as e:
        print("提交失败：", e)
