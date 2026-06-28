![banner](https://github-production-user-asset-6210df.s3.amazonaws.com/146557752/614258480-f0b4be52-d4c6-4107-a553-dc49fbe7ec0c.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20260628%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260628T140849Z&X-Amz-Expires=300&X-Amz-Signature=0eba1ecd6beea0a156b5f73c77e0dbef6e42e1a46ff412e9a5f46c0625547a00&X-Amz-SignedHeaders=host&response-content-type=image%2Fjpeg)

Không có gì đặc biệt ở đây cả. Chỉ có một người quá mệt mỏi với việc cài đặt đủ thứ thư viện rồi xảy ra xung đột với cuda, nên viết tạm cái mẫu docker đóng gói lại dự án huấn luyện mô hình học sâu bằng pytorch trên gpu, để chạy một lần rồi xóa đi cho tiện.

## Cấu trúc dự án

```
alexnet-docker/
├── README.md              
├── requirements.txt       # Cài đặt các thư viện python cần thiết
├── Dockerfile             # Kịch bản docker sẵn sàng để đóng gói
├── train.py               # Đoạn mã huấn luyện
├── evaluation.py          # Đoạn mã đánh giá mô hình sau khi huấn luyện
└── src/
    ├── __init__.py
    ├── model.py           # Chứa kiến trúc AlexNet
    ├── data.py            # Tải dataset MNIST
    └── trainer.py         # Hàm lặp huấn luyện
```
File quan trọng nhất ở đây là `Dockerfile`, thứ nhì là `requirements.txt` vì đã được định nghĩa trong dockerfile. Các file còn lại chỉ mang tính minh hoa, muốn cấu trúc như thế nào là do nhu cầu, miễn là điền đủ thư viện cần cài vào requirements.txt kia. 
## Yêu cầu chạy

- Cần cài **Docker** về máy nếu muốn chạy bằng docker
- Không cần cài đặt sẵn Python, PyTorch, CUDA trên máy cục bộ, vì vốn dĩ đó là mục đích dùng docker.

## Cách chạy trên Docker

Trước hết, hãy khởi động Docker trên máy bạn.
Mở terminal trỏ đến đúng thư mục repo này và thực hiện các bước dưới đây.

### Bước 1: Build docker
Lệnh này sẽ giúp bạn build image thành một docker tên là mnist-cnn khi đang đứng ở thư mục chứa Dockerfile.

```bash
docker build -t mnist-cnn .
```

### Bước 2: Chạy docker

Lệnh này sẽ giúp bạn chạy container bạn vừa build.
```bash
docker run --gpus all -it -v $(pwd)/checkpoints:/workspace/checkpoints mnist-cnn
```

Nếu bạn dùng windows thì dùng lệnh này:
```bash
docker run --gpus all -it -v ${PWD}/checkpoints:/workspace/checkpoints mnist-cnn
```

Nếu không có gì sai sót lớn, sau khi chạy lệnh trên khả năng cao bạn sẽ chui vào môi trường bên trong container.

### Bước 3: Huấn luyện

Sau khi vào trong container, ta sẽ tiến hành làm việc với terminal của container đó.
Chạy lệnh sau thì sẽ thực hiện quá trình huấn luyện.
```bash
python3 train.py --output_dir ./checkpoints --epochs 5 --batch_size 64
```
Bạn có thể sửa nơi lưu checkpoint, số epoch hay kích thước batch ngay trên câu lệnh.
Quá trình huấn luyện bao gồm tải dữ liệu nếu chưa có, thực hiện vòng lặp huấn luyện và lưu checkpoint.
### Bước 4: Chạy evaluation
Bạn vẫn ở trong container sau khi huấn luyện xong.
Chạy lệnh sau thì sẽ thực hiện việc đánh giá mô hình được huấn luyện.
```bash
python3 evaluation.py --checkpoint ./checkpoints/model.pt
```

**Lưu ý:** 
- `--gpus all` dùng để phát hiện và dùng gpu của máy.
- `-v` để tự động đồng bộ thư mục checkpoints từ container ra ngoài máy.
- `-it` để có interactive shell trong container.


