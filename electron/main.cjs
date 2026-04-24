const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

// 1. สร้างไฟล์ stock.db ไว้ในโฟลเดอร์เดียวกับ main.cjs
const dbPath = path.join(__dirname, 'stock.db');
const db = new sqlite3.Database(dbPath);

// 2. สร้างตารางถ้ายังไม่มี
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE,
    category TEXT,
    type TEXT,
    value TEXT,
    qty INTEGER
  )`);
});

// 3. เปิดช่องทาง (IPC) ให้ React เรียกมาดึงข้อมูล
ipcMain.handle('get-stocks', () => {
  return new Promise((resolve, reject) => {
    db.all('SELECT * FROM stocks', [], (err, rows) => {
      if (err) reject(err);
      resolve(rows);
    });
  });
});

// 4. เปิดช่องทางให้ React ส่งข้อมูลมาบันทึก
ipcMain.handle('add-stock', (event, stockData) => {
  return new Promise((resolve, reject) => {
    const stmt = db.prepare('INSERT INTO stocks (code, category, type, value, qty) VALUES (?, ?, ?, ?, ?)');
    stmt.run(stockData.code, stockData.category, stockData.type, stockData.value, stockData.qty, function(err) {
      if (err) reject(err);
      resolve({ success: true, id: this.lastID });
    });
    stmt.finalize();
  });
});

// 5. ฟังก์ชันสร้างหน้าต่างโปรแกรม (ของเดิม)
function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs') // ชี้ไปที่ไฟล์ preload.cjs ที่เราเปลี่ยนชื่อไว้
    }
  });

  // ชี้ไปที่ Port ของ React (Vite)
  win.loadURL('http://localhost:5173'); 
}

// 6. สั่งให้โปรแกรมทำงาน
app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});