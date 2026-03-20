NEUQ_Repair_System/
│
├── server.js # Node.js 后端主程序，负责接口、数据库操作与路由
├── repair.db # SQLite 数据库文件，存储所有申请与管理员信息
├── start_server.bat # 启动脚本，自动运行服务并开启 ngrok 公网链接
│
├── public/ # 前端网页文件目录
│ ├── index.html # 系统入口页面（身份选择界面）
│ ├── client.html # 客户端界面（学生提交与查看申请）
│ ├── admin.html # 后台端界面（管理员管理与统计分析）
│ ├── style.css # 公共样式表，定义颜色、按钮效果、布局等
│ └── script.js # 前端逻辑脚本，与后端 API 交互
│
├── utils/ # 辅助工具目录
│ └── completed_pie_chart.py # 自动统计数据脚本
│
└── README.md # 使用说明与部署文档
