import zipfile
import os

# Thay bằng đường dẫn thật đến thư mục chứa các file zip
zip_folder = r"E:\Sun_Observering_Interferometry\radio2"
output_folder = os.path.join(zip_folder, "extracted")

# Tạo thư mục lưu trữ nếu chưa có
os.makedirs(output_folder, exist_ok=True)

# Lặp qua tất cả file zip trong thư mục
for filename in os.listdir(zip_folder):
    if filename.endswith(".zip"):
        zip_path = os.path.join(zip_folder, filename)
        extract_path = os.path.join(output_folder, filename.replace('.zip', ''))
        os.makedirs(extract_path, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        print(f"✅ Đã giải nén: {filename} → {extract_path}")