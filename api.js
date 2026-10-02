const express=require("express");
const TelegramBotModule=require("node-telegram-bot-api");
const fs=require("fs");
const path=require("path");
const initSqlJs=require("sql.js");

const TelegramBot=TelegramBotModule.default||TelegramBotModule.TelegramBot||TelegramBotModule;
const app=express();
app.use(express.json());

const PORT=2009;
const BOT_TOKEN="8889141966:AAHNN1JeLeEN80d0RmUBYCv6DkfxHM72Cxw";
const OWNER_USERNAME="SecondAccF";
const OWNER_CHAT=6833144624;
const DB_FILE=path.join(__dirname,"devices.db");

let bot,SQL,db,rich;

async function loadRich(){
  if(!rich)rich=await import("tg-rich-messages");
  return rich;
}

if(!BOT_TOKEN){
  console.error("❌ FLOX_BOT_TOKEN belum diatur.");
  console.error('Jalankan: export FLOX_BOT_TOKEN="TOKEN_BARU"');
  process.exit(1);
}

async function initDatabase(){
  SQL=await initSqlJs({
    locateFile:file=>path.join(path.dirname(require.resolve("sql.js")),file)
  });

  if(fs.existsSync(DB_FILE)){
    db=new SQL.Database(fs.readFileSync(DB_FILE));
    console.log("📂 Database devices.db dimuat.");
  }else{
    db=new SQL.Database();
    console.log("🆕 Membuat devices.db baru.");
  }

  db.run(`
    CREATE TABLE IF NOT EXISTS devices(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      device_key TEXT UNIQUE NOT NULL,
      buyer TEXT NOT NULL,
      seller TEXT NOT NULL,
      model TEXT,
      os TEXT,
      ip TEXT,
      local_ip TEXT,
      hostname TEXT,
      cpu TEXT,
      memory TEXT,
      battery TEXT,
      status TEXT DEFAULT 'pending',
      created_at TEXT,
      updated_at TEXT
    )
  `);

  saveDatabase();
}

function saveDatabase(){
  if(db)fs.writeFileSync(DB_FILE,Buffer.from(db.export()));
}

function dbGet(sql,params=[]){
  const s=db.prepare(sql);
  try{
    s.bind(params);
    return s.step()?s.getAsObject():undefined;
  }finally{s.free();}
}

function dbAll(sql,params=[]){
  const s=db.prepare(sql),rows=[];
  try{
    s.bind(params);
    while(s.step())rows.push(s.getAsObject());
    return rows;
  }finally{s.free();}
}

function dbRun(sql,params=[]){
  db.run(sql,params);
  const changes=dbGet("SELECT changes() AS changes");
  const lastID=dbGet("SELECT last_insert_rowid() AS id");
  const result={
    changes:Number(changes?.changes||0),
    lastID:Number(lastID?.id||0)
  };
  saveDatabase();
  return result;
}

async function telegramRequest(method,body){
  const response=await fetch(
    `https://api.telegram.org/bot${BOT_TOKEN}/${method}`,
    {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify(body)
    }
  );

  let result;
  try{
    result=await response.json();
  }catch{
    throw new Error(`Telegram API memberikan response tidak valid (${response.status})`);
  }

  if(!result.ok)throw new Error(result.description||`Telegram API error (${response.status})`);
  return result.result;
}

function isOwner(msg){
  return String(msg.from?.username||"").toLowerCase()===OWNER_USERNAME.toLowerCase();
}

async function playThinking(chatId,steps=[]){
  const {doc,thinking}=await loadRich();
  const draftId=Math.floor(Math.random()*2147483646)+1;

  if(!steps.length)steps=[
    "🔎 Mengecek perangkat...",
    "📡 Menghubungkan ke database...",
    "📊 Mengambil informasi...",
    "🖼️ Menyiapkan Rich Message...",
    "✅ Siap!"
  ];

  for(const text of steps){
    try{
      const payload=doc(thinking(text)).toInputRichMessage({
        skipEntityDetection:true
      });

      await telegramRequest("sendRichMessageDraft",{
        chat_id:chatId,
        draft_id:draftId,
        rich_message:payload
      });
    }catch(err){
      console.log("⚠️ Thinking error:",err.message);
    }

    await new Promise(r=>setTimeout(r,500));
  }

  return draftId;
}

async function sendRich(chatId,message,options={}){
  const payload=message.toInputRichMessage({
    skipEntityDetection:true
  });

  return telegramRequest("sendRichMessage",{
    chat_id:chatId,
    rich_message:payload,
    ...options
  });
}

async function sendDeviceNotification(deviceKey,buyer,seller,info){
  const {
    doc,heading,paragraph,bold,code,blockquote
  }=await loadRich();

  const model=info.model||info.hostname||"Unknown";
  const os=info.os||"Unknown";
  const ip=info.ip||"Unknown";

  await playThinking(OWNER_CHAT,[
    "🔎 Perangkat baru terdeteksi...",
    "📡 Mengambil informasi perangkat...",
    "📊 Memproses data license...",
    "🖼️ Menyiapkan Rich Message...",
    "✅ Siap!"
  ]);

  const message=doc(
    heading(2,"🆕 Perangkat Baru"),
    paragraph([bold("Perangkat baru memasuki FloX Tools.")]),
    paragraph("👤 USERNAME ↓"),
    blockquote([
      paragraph([bold("Buyer : "),buyer]),
      paragraph([bold("Seller : "),seller])
    ],undefined,{expandable:true}),
    paragraph("📱 DEVICE DETAIL ↓"),
    blockquote([
      paragraph(["📱 Model: ",bold(model)]),
      paragraph(["⚙️ OS: ",os]),
      paragraph(["🔑 Device Key: ",code(deviceKey)]),
      paragraph(["🌐 IP: ",ip])
    ],undefined,{expandable:true}),
    paragraph([bold("🔐 Approve dengan:")]),
    paragraph([code(`/addtools ${deviceKey}`)])
  );

  return sendRich(OWNER_CHAT,message);
}

app.get("/",(req,res)=>{
  res.json({
    status:"online",
    service:"FloX License API",
    port:PORT
  });
});

app.post("/register",async(req,res)=>{
  try{
    const data=req.body||{};
    const deviceKey=data.device_key;
    const buyer=String(data.buyer||"").trim();
    const seller=String(data.seller||"").trim();
    const info=data.device_info||{};

    if(!deviceKey)
      return res.status(400).json({
        status:"error",
        message:"Device Key kosong."
      });

    if(!buyer)
      return res.status(400).json({
        status:"error",
        message:"Buyer kosong."
      });

    const existing=dbGet(
      "SELECT * FROM devices WHERE device_key=?",
      [deviceKey]
    );

    if(existing)
      return res.json({
        status:existing.status,
        device_key:deviceKey
      });

    const now=new Date().toISOString();

    dbRun(`
      INSERT INTO devices(
        device_key,buyer,seller,model,os,ip,local_ip,
        hostname,cpu,memory,battery,status,created_at,updated_at
      )
      VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    `,[
      deviceKey,
      buyer,
      seller,
      info.model||info.hostname||"Unknown",
      info.os||"Unknown",
      info.ip||"Unknown",
      info.local_ip||"Unknown",
      info.hostname||"Unknown",
      info.cpu||"Unknown",
      info.memory||"Unknown",
      JSON.stringify(info.battery||{}),
      "pending",
      now,
      now
    ]);

    try{
      await sendDeviceNotification(deviceKey,buyer,seller,info);
    }catch(err){
      console.error("⚠️ Gagal kirim Rich Message:",err.message);
    }

    res.json({
      status:"pending",
      device_key:deviceKey
    });
  }catch(err){
    console.error("REGISTER ERROR:",err);
    res.status(500).json({
      status:"error",
      message:err.message
    });
  }
});

app.post("/check",async(req,res)=>{
  try{
    const deviceKey=req.body?.device_key;

    if(!deviceKey)
      return res.status(400).json({
        status:"error",
        message:"Device Key kosong."
      });

    const device=dbGet(
      "SELECT * FROM devices WHERE device_key=?",
      [deviceKey]
    );

    if(!device)return res.json({status:"not_found"});

    res.json({
      status:device.status,
      device_key:device.device_key
    });
  }catch(err){
    res.status(500).json({
      status:"error",
      message:err.message
    });
  }
});

app.post("/set-status",async(req,res)=>{
  try{
    const {device_key,status}=req.body||{};

    if(!device_key)
      return res.status(400).json({
        status:"error",
        message:"Device Key kosong."
      });

    if(!["pending","approved","blocked"].includes(status))
      return res.status(400).json({
        status:"error",
        message:"Status tidak valid."
      });

    const result=dbRun(`
      UPDATE devices
      SET status=?,updated_at=?
      WHERE device_key=?
    `,[status,new Date().toISOString(),device_key]);

    if(!result.changes)
      return res.status(404).json({
        status:"not_found"
      });

    res.json({
      status:"success",
      device_status:status
    });
  }catch(err){
    res.status(500).json({
      status:"error",
      message:err.message
    });
  }
});

async function changeStatus(deviceKey,status){
  try{
    const device=dbGet(
      "SELECT * FROM devices WHERE device_key=?",
      [deviceKey]
    );

    if(!device)return {status:"not_found"};

    dbRun(`
      UPDATE devices
      SET status=?,updated_at=?
      WHERE device_key=?
    `,[status,new Date().toISOString(),deviceKey]);

    return {
      status:"success",
      device_status:status
    };
  }catch(err){
    return {
      status:"error",
      message:err.message
    };
  }
}

async function handleStatusCommand(msg,status,type){
  try{
    if(!isOwner(msg))
      return bot.sendMessage(msg.chat.id,"❌ Akses ditolak.");

    const key=msg.text?.split(/\s+/).slice(1).join(" ").trim();

    if(!key)
      return bot.sendMessage(
        msg.chat.id,
        `❌ Format:\n/${type} DEVICE_KEY`
      );

    const steps={
      approved:[
        "🔎 Mencari device...",
        "📡 Memeriksa license...",
        "🔐 Mengaktifkan perangkat...",
        "✅ License disetujui!"
      ],
      blocked:[
        "🔎 Mencari device...",
        "📡 Memeriksa license...",
        "🚫 Memblokir perangkat..."
      ],
      unblock:[
        "🔎 Mencari device...",
        "📡 Memeriksa status...",
        "🔓 Membuka blokir..."
      ]
    };

    await playThinking(msg.chat.id,steps[status==="approved"&&type==="addtools"?"approved":status==="blocked"?"blocked":"unblock"]);

    const result=await changeStatus(
      key,
      status==="unblock"?"approved":status
    );

    if(result.status!=="success")
      return bot.sendMessage(
        msg.chat.id,
        "❌ Device tidak ditemukan."
      );

    const {doc,heading,paragraph,bold,code,blockquote}=await loadRich();

    let message;

    if(type==="addtools"){
      message=doc(
        heading(2,"✅ Device Approved"),
        paragraph([bold("Device berhasil diaktifkan.")]),
        blockquote([
          paragraph(["🔑 Device Key: ",code(key)]),
          paragraph("📊 Status: APPROVED")
        ],undefined,{expandable:true})
      );
    }else if(type==="blocktools"){
      message=doc(
        heading(2,"🚫 Device Blocked"),
        paragraph(["Device ",code(key)," berhasil diblokir."]),
        paragraph(["📊 Status: ",bold("BLOCKED")])
      );
    }else{
      message=doc(
        heading(2,"🔓 Device Unblocked"),
        paragraph(["🔑 Device Key: ",code(key)]),
        paragraph(["📊 Status: ",bold("APPROVED")])
      );
    }

    await sendRich(msg.chat.id,message);
  }catch(err){
    console.error(`${type.toUpperCase()} ERROR:`,err);
  }
}

function registerBotHandlers(){

  bot.onText(/^\/addtools(?:\s+(.+))?$/i,
    msg=>handleStatusCommand(msg,"approved","addtools")
  );

  bot.onText(/^\/blocktools(?:\s+(.+))?$/i,
    msg=>handleStatusCommand(msg,"blocked","blocktools")
  );

  bot.onText(/^\/unblocktools(?:\s+(.+))?$/i,
    msg=>handleStatusCommand(msg,"unblock","unblocktools")
  );

  bot.onText(/^\/listtools$/i,async msg=>{
    try{
      if(!isOwner(msg))
        return bot.sendMessage(msg.chat.id,"❌ Akses ditolak.");

      await playThinking(msg.chat.id,[
        "🔎 Mengambil database...",
        "📊 Menghitung perangkat...",
        "🖼️ Menyiapkan daftar..."
      ]);

      const devices=dbAll(
        "SELECT * FROM devices ORDER BY id DESC"
      );

      if(!devices.length)
        return bot.sendMessage(
          msg.chat.id,
          "📭 Belum ada device."
        );

      const {
        doc,heading,paragraph,bold,code,blockquote
      }=await loadRich();

      const blocks=[
        heading(2,"📱 FloX Tools Devices"),
        paragraph([
          "Total device: ",
          bold(String(devices.length))
        ])
      ];

      for(const device of devices){
        blocks.push(
          blockquote([
            paragraph(["🔑 ",code(device.device_key)]),
            paragraph(["👤 Buyer: ",device.buyer]),
            paragraph(["🏪 Seller: ",device.seller]),
            paragraph([
              "📊 Status: ",
              bold(String(device.status).toUpperCase())
            ])
          ],undefined,{expandable:true})
        );
      }

      await sendRich(msg.chat.id,doc(...blocks));
    }catch(err){
      console.error("LISTTOOLS ERROR:",err);
    }
  });

  bot.onText(/^\/infotools(?:\s+(.+))?$/i,async msg=>{
    try{
      if(!isOwner(msg))
        return bot.sendMessage(msg.chat.id,"❌ Akses ditolak.");

      const key=msg.text?.split(/\s+/).slice(1).join(" ").trim();

      if(!key)
        return bot.sendMessage(
          msg.chat.id,
          "❌ Format:\n/infotools DEVICE_KEY"
        );

      await playThinking(msg.chat.id,[
        "🔎 Mencari device...",
        "📡 Mengambil informasi...",
        "📊 Menyiapkan detail..."
      ]);

      const device=dbGet(
        "SELECT * FROM devices WHERE device_key=?",
        [key]
      );

      if(!device)
        return bot.sendMessage(
          msg.chat.id,
          "❌ Device tidak ditemukan."
        );

      const {
        doc,heading,paragraph,bold,code,blockquote
      }=await loadRich();

      const message=doc(
        heading(2,"📱 Device Information"),

        paragraph([bold("🔑 Device Key")]),

        paragraph(code(device.device_key)),

        paragraph("👤 USERNAME ↓"),

        blockquote([
          paragraph(["Buyer: ",device.buyer]),
          paragraph(["Seller: ",device.seller])
        ],undefined,{expandable:true}),

        paragraph("📱 DEVICE DETAIL ↓"),

        blockquote([
          paragraph(["📱 Model: ",device.model||"Unknown"]),
          paragraph(["⚙️ OS: ",device.os||"Unknown"]),
          paragraph(["🌐 IP: ",device.ip||"Unknown"]),
          paragraph(["📡 Local IP: ",device.local_ip||"Unknown"]),
          paragraph(["🖥️ Hostname: ",device.hostname||"Unknown"]),
          paragraph(["⚙️ CPU: ",device.cpu||"Unknown"]),
          paragraph(["💾 Memory: ",device.memory||"Unknown"]),
          paragraph(["🔋 Battery: ",device.battery||"Unknown"]),
          paragraph([
            "📊 Status: ",
            bold(String(device.status).toUpperCase())
          ])
        ],undefined,{expandable:true})
      );

      await sendRich(msg.chat.id,message);
    }catch(err){
      console.error("INFOTOOLS ERROR:",err);
    }
  });
}

async function start(){
  try{
    console.log("🔄 Menginisialisasi database...");
    await initDatabase();

    console.log("🔄 Menginisialisasi Telegram Bot...");

    bot=new TelegramBot(BOT_TOKEN,{polling:true});
    registerBotHandlers();

    bot.on("polling_error",error=>{
      console.error("Telegram polling error:",error.message);
    });

    app.listen(PORT,"0.0.0.0",()=>{
      console.log(`
╔══════════════════════════════════════╗
║       FloX License API + BOT         ║
╠══════════════════════════════════════╣
║ API  : http://127.0.0.1:${PORT}          ║
║ BOT  : ONLINE                         ║
║ DB   : devices.db                     ║
╚══════════════════════════════════════╝
`);
    });
  }catch(err){
    console.error("❌ Gagal menjalankan FloX License API:",err);
    process.exit(1);
  }
}

start();
