const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  // ฟังก์ชันสำหรับส่ง URL ไปหา Main (ของเดิม)
  startDownload: (url) => ipcRenderer.send('start-download', url),
  
  // ฟังก์ชันสำหรับรับสถานะกลับมาอัปเดต UI (ของเดิม)
  onDownloadProgress: (callback) => ipcRenderer.on('download-progress', (_event, value) => callback(value)), // <-- เติมลูกน้ำ (,) ตรงนี้

  // ======== ส่วนที่เพิ่มเข้ามาใหม่สำหรับ Database ========
  getStocks: () => ipcRenderer.invoke('get-stocks'),
  addStock: (data) => ipcRenderer.invoke('add-stock', data)
});