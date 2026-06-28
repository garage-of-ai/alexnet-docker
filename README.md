![banner](https://github-production-user-asset-6210df.s3.amazonaws.com/146557752/614258480-f0b4be52-d4c6-4107-a553-dc49fbe7ec0c.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20260628%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260628T140849Z&X-Amz-Expires=300&X-Amz-Signature=0eba1ecd6beea0a156b5f73c77e0dbef6e42e1a46ff412e9a5f46c0625547a00&X-Amz-SignedHeaders=host&response-content-type=image%2Fjpeg)

Ôi trời đất ơi, định tìm kiếm gì ở repo này? Tôi quá mệt mỏi để cài đủ thứ trên máy rồi, nên viết tạm cái đóng gói, chạy một lần rồi vứt đi thôi, chứ có gì hay ho ở đây đâu.

## Yêu cầu

- **Docker** — để build image
- **NVIDIA Docker Runtime** (optional) — nếu muốn chạy với GPU
- Không cần cài đặt Python, PyTorch, CUDA trên máy host

## Cách chạy

### Build image

```bash
docker build -t mnist-cnn .
```

### Chạy training

```bash
docker run --gpus all -it -v $(pwd)/checkpoints:/workspace/checkpoints mnist-cnn
# Trong container:
python3 train.py --output_dir ./checkpoints --epochs 5 --batch_size 64
```

### Chạy evaluation

```bash
docker run --gpus all -it -v $(pwd)/checkpoints:/workspace/checkpoints mnist-cnn
# Trong container:
python3 evaluation.py --checkpoint ./checkpoints/model.pt
```

**Lưu ý:** 
- Bỏ `--gpus all` nếu không có GPU (sẽ tự chạy trên CPU)
- `-v` để mount folder checkpoints ra ngoài host (để lưu model)
- `-it` để có interactive shell trong container

## Cấu trúc

```
.
├── CLAUDE.md              # Hướng dẫn dự án
├── README.md              # File này
├── requirements.txt       # Dependencies (torch, torchvision)
├── Dockerfile             # Cấu hình Docker image
├── train.py               # Script huấn luyện
├── evaluation.py          # Script đánh giá mô hình
└── src/
    ├── __init__.py
    ├── model.py           # AlexNet architecture
    ├── data.py            # Load MNIST dataset
    └── trainer.py         # Training loop
```

### Các file chính

- **`train.py`** — Huấn luyện CNN trên MNIST
  - Args: `--output_dir`, `--epochs`, `--batch_size`, `--lr`
  
- **`evaluation.py`** — Đánh giá mô hình trên test set
  - Args: `--checkpoint` (đường dẫn tới model)

- **`src/model.py`** — Kiến trúc AlexNet (adapt cho MNIST 28x28 → 224x224)

- **`src/data.py`** — Load MNIST, transform images, tạo DataLoader

- **`src/trainer.py`** — Training loop, save checkpoint, auto GPU/CPU fallback
