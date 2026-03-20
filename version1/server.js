const express = require("express");
const cors = require("cors");
const path = require("path");
const sqlite3 = require("sqlite3").verbose();

const app = express();
app.use(cors());
app.use(express.json());

const DB_FILE = path.join(__dirname, "repair.db");
const db = new sqlite3.Database(DB_FILE);

// 初始化数据库
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS repairs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT,
    service TEXT,
    description TEXT,
    date TEXT,
    location TEXT,
    status TEXT,
    reason TEXT,
    createdAt INTEGER,
    completedAt INTEGER
  )`);

  db.run(`CREATE TABLE IF NOT EXISTS admins (
    user TEXT PRIMARY KEY,
    pass TEXT
  )`);

  db.run(`INSERT OR IGNORE INTO admins(user, pass) VALUES(?, ?)`, ["202312420","335177Ff"]);
});

// ------------------- API -------------------

// 获取所有维修记录
app.get("/api/repairs", (req, res) => {
  db.all("SELECT * FROM repairs ORDER BY date DESC", (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

// 提交维修申请
app.post("/api/repairs", (req, res) => {
  const r = req.body;
  db.run(
    `INSERT INTO repairs (name,phone,email,service,description,date,location,status,reason,createdAt)
     VALUES (?,?,?,?,?,?,?,?,?,?)`,
    [r.name, r.phone, r.email, r.service, r.description, r.date, r.location, "pending", "", Date.now()],
    function (err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ id: this.lastID });
    }
  );
});

// 接受申请 → waiting
app.post("/api/repairs/:id/accept", (req, res) => {
  db.run("UPDATE repairs SET status='waiting' WHERE id=?", [req.params.id], function(err){
    if(err) return res.status(500).json({error: err.message});
    res.json({ok:true});
  });
});

// 驳回申请
app.post("/api/repairs/:id/reject", (req,res)=>{
  const reason = req.body.reason||"";
  db.run("UPDATE repairs SET status='rejected', reason=? WHERE id=?", [reason, req.params.id], function(err){
    if(err) return res.status(500).json({error:err.message});
    res.json({ok:true});
  });
});

// 完成维修
app.post("/api/repairs/:id/complete", (req,res)=>{
  db.run("UPDATE repairs SET status='completed', completedAt=? WHERE id=?", [Date.now(), req.params.id], function(err){
    if(err) return res.status(500).json({error:err.message});
    res.json({ok:true});
  });
});

// 隐藏客户端显示
app.post("/api/repairs/:id/hide", (req,res)=>{
  db.run("UPDATE repairs SET status='hidden' WHERE id=?", [req.params.id], function(err){
    if(err) return res.status(500).json({error:err.message});
    res.json({ok:true});
  });
});

// 删除记录
app.delete("/api/repairs/:id", (req,res)=>{
  db.run("DELETE FROM repairs WHERE id=?", [req.params.id], function(err){
    if(err) return res.status(500).json({error:err.message});
    res.json({ok:true});
  });
});

// 管理员登录
app.post("/api/admin/login", (req,res)=>{
  const {user,pass}=req.body;
  db.get("SELECT * FROM admins WHERE user=? AND pass=?", [user,pass], (err,row)=>{
    if(err) return res.status(500).json({error:err.message});
    if(row) res.json({ok:true});
    else res.status(401).json({ok:false,msg:"账号或密码错误"});
  });
});

// 前端静态页面
app.use(express.static(path.join(__dirname,"public")));
app.get("/", (req,res)=>res.sendFile(path.join(__dirname,"public","index.html")));

const PORT = 3000;
app.listen(PORT, "0.0.0.0", ()=>console.log(`✅ Server running at http://localhost:${PORT}`));
