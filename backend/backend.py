import sys
import json
import time

def start_download(url):
    # จำลองการดาวน์โหลดไฟล์ (สมมติว่าใช้เวลาโหลด)
    for i in range(10, 101, 30):
        time.sleep(1)
        # ส่งสถานะ % กลับไปให้ Node.js
        print(json.dumps({"status": "downloading", "progress": i}))
        sys.stdout.flush() # สำคัญมาก! ต้องใส่เพื่อให้ข้อมูลส่งออกไปทันที ไม่ค้างในบัฟเฟอร์

    print(json.dumps({"status": "completed", "url": url}))
    sys.stdout.flush()

if __name__ == "__main__":
    # รับ URL ที่ส่งมาจาก Node.js ผ่าน Argument
    input_url = sys.argv[1] 
    start_download(input_url)