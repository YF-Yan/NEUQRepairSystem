import sqlite3
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ---------------- 配置 ----------------
DB_FILE = "repair.db"  # 数据库文件路径

# 中文字体配置，防止显示乱码（Windows 常用字体）
rcParams['font.sans-serif'] = ['Microsoft YaHei']
rcParams['axes.unicode_minus'] = False

# ---------------- 连接数据库 ----------------
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# ---------------- 查询所有状态数量 ----------------
cursor.execute("""
    SELECT status, COUNT(*) 
    FROM repairs 
    GROUP BY status
""")
rows = cursor.fetchall()
status_dict = {row[0]: row[1] for row in rows}

statuses = ["pending", "waiting", "rejected", "completed"]
status_counts = [status_dict.get(s, 0) for s in statuses]

# ---------------- 查询已完成的服务类型 ----------------
cursor.execute("""
    SELECT service, COUNT(*) 
    FROM repairs 
    WHERE status='completed'
    GROUP BY service
""")
rows2 = cursor.fetchall()
service_dict = {row[0]: row[1] for row in rows2}

services = ["电脑清灰", "手机贴膜", "小电子设备维修", "其他"]
service_counts = [service_dict.get(s, 0) for s in services]

conn.close()

# ---------------- 绘制饼状图 ----------------
fig, axs = plt.subplots(1, 2, figsize=(14, 7))

# --- 饼图1：所有状态统计 ---
colors1 = ['#2196f3', '#ffcc00', '#f44336', '#4caf50']  # 蓝、黄、红、绿
labels1 = [f"{s} ({c})" for s, c in zip(statuses, status_counts)]
axs[0].pie(status_counts, labels=labels1, autopct='%1.1f%%', startangle=140, colors=colors1, textprops={'fontsize':12})
axs[0].set_title("NEUQ电子设备维修状态统计", fontsize=16)
axs[0].axis('equal')

# --- 饼图2：已完成服务统计 ---
colors2 = ['#4caf50', '#66bb6a', '#81c784', '#a5d6a7']  # 绿色系
labels2 = [f"{s} ({c})" for s, c in zip(services, service_counts)]
axs[1].pie(service_counts, labels=labels2, autopct='%1.1f%%', startangle=140, colors=colors2, textprops={'fontsize':12})
axs[1].set_title("NEUQ电子设备维修完成统计", fontsize=16)
axs[1].axis('equal')

plt.tight_layout()
plt.show()
