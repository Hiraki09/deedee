import { useState, useEffect } from 'react';

function App() {
  const [stocks, setStocks] = useState([]);

  // ดึงข้อมูลตอนเปิดหน้าเว็บ
  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    const data = await window.electronAPI.getStocks();
    setStocks(data);
  };

  const handleSave = async () => {
    // 1. สุ่มตัวเลขมาต่อท้ายรหัส เพื่อให้รหัสไม่ซ้ำกันเวลาเรากดปุ่มรัวๆ
    const randomNum = Math.floor(Math.random() * 1000); 
    const testCode = `R-10K-CF-${randomNum}`;

    const newItem = {
      code: testCode, // ใช้รหัสที่สุ่มขึ้นมาใหม่
      category: "Resistor",
      type: "Carbon Film",
      value: "10K",
      qty: 50
    };
    
    // 2. ใช้ try...catch เพื่อดักจับ Error กรณีพัง จะได้ไม่ไปแดงใน Terminal
    try {
      await window.electronAPI.addStock(newItem);
      alert(`บันทึกสำเร็จ! (รหัส: ${testCode})`);
      fetchStocks(); // โหลดข้อมูลใหม่มาแสดง
    } catch (error) {
      alert('บันทึกไม่สำเร็จ: รหัสสินค้านี้มีอยู่ในระบบแล้ว!');
      console.error(error);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Stock System</h1>
      <button onClick={handleSave}>ทดสอบเพิ่มข้อมูล</button>
      
      <ul>
        {stocks.map(item => (
          <li key={item.id}>
            {item.code} | {item.category} | จำนวน: {item.qty}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;