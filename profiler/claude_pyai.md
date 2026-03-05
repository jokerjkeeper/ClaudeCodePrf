# claude_pyai.md — Python AI / LLM / CV 專案配置 Profile

> 本文件為 Python AI（LLM / Computer Vision）專案的 Claude Code 補充規則，需搭配 `CLAUDE.md` 主文件使用。
> 放置於 `profiler/` 目錄下。

---

## 一、專案基礎資訊

```yaml
# ⚠️ 請根據實際專案填寫以下內容
project_type: LLM / CV / MultiModal   # 專案類型
python_version: "3.11"
gpu_framework: PyTorch                 # PyTorch / TensorFlow / JAX
llm_library: transformers              # transformers / vllm / llama-cpp-python / langchain / none
cv_library: ultralytics                # ultralytics / detectron2 / mmdet / timm / none
vector_db: none                        # chromadb / faiss / milvus / qdrant / none
serving: FastAPI                       # FastAPI / Gradio / Streamlit / BentoML / TorchServe
package_manager: uv                    # uv / poetry / pip / conda
experiment_tracking: none              # wandb / mlflow / tensorboard / none
deployment: Docker                     # Docker / ONNX Runtime / TensorRT / Triton
```

---

## 二、專案結構

### 2.1 LLM 應用專案結構

```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py                # 服務入口（FastAPI / Gradio）
│   ├── config.py              # 配置管理（pydantic-settings）
│   ├── api/                   # API 路由層
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── chat.py        # 對話端點
│   │       ├── embeddings.py  # 向量化端點
│   │       └── completions.py # 補全端點
│   ├── chains/                # LLM Chain / Agent 邏輯
│   │   ├── __init__.py
│   │   ├── rag_chain.py       # RAG 管線
│   │   └── agent.py           # Agent 定義
│   ├── prompts/               # Prompt 模板
│   │   ├── system.txt
│   │   └── templates.py
│   ├── services/              # 業務邏輯層
│   │   ├── __init__.py
│   │   ├── llm_service.py     # LLM 調用封裝
│   │   ├── retriever.py       # 檢索服務
│   │   └── embedding.py       # Embedding 服務
│   ├── models/                # 數據模型 / ORM
│   │   └── __init__.py
│   ├── schemas/               # Pydantic 輸入/輸出 schema
│   │   ├── chat.py
│   │   └── response.py
│   └── utils/                 # 工具函數
│       ├── tokenizer.py       # Token 計算
│       └── logger.py
├── data/                      # 數據目錄（不進版控）
│   ├── raw/
│   ├── processed/
│   └── vectorstore/
├── notebooks/                 # 實驗 Notebook
├── scripts/                   # 獨立腳本（數據處理、下載等）
│   ├── download_data.py
│   ├── build_index.py
│   └── evaluate.py
├── tests/
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

### 2.2 CV 專案結構

```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py                # 服務入口
│   ├── config.py
│   ├── api/
│   │   └── v1/
│   │       ├── predict.py     # 推理端點
│   │       └── health.py
│   ├── models/                # 模型定義
│   │   ├── __init__.py
│   │   ├── detector.py        # 檢測模型
│   │   ├── classifier.py      # 分類模型
│   │   └── segmentor.py       # 分割模型
│   ├── services/
│   │   ├── inference.py       # 推理服務
│   │   └── preprocessing.py   # 前處理管線
│   ├── schemas/
│   │   ├── prediction.py
│   │   └── response.py
│   └── utils/
│       ├── visualization.py   # 結果可視化
│       └── image_utils.py     # 圖像工具
├── training/                  # 訓練相關（與服務分離）
│   ├── train.py
│   ├── evaluate.py
│   ├── configs/               # 訓練配置（YAML）
│   │   └── default.yaml
│   ├── datasets/              # Dataset 定義
│   │   └── custom_dataset.py
│   └── augmentations.py       # 數據增強
├── weights/                   # 模型權重（不進版控）
├── data/                      # 數據集（不進版控）
│   ├── images/
│   ├── labels/
│   └── splits/
├── notebooks/
├── scripts/                   # 獨立腳本
│   ├── download_weights.py
│   ├── convert_format.py
│   └── export_onnx.py
├── tests/
├── pyproject.toml
├── Dockerfile
└── .env.example
```

---

## 三、代碼規範

### 3.1 命名規範

```python
# 類名：PascalCase
class TextEmbedder:
    pass

# 函數/方法：snake_case
def load_model(model_path: str) -> nn.Module:
    pass

# 變數：snake_case
batch_size = 32
learning_rate = 1e-4

# 常量：UPPER_SNAKE_CASE
DEFAULT_MODEL_NAME = "gpt-4"
MAX_CONTEXT_LENGTH = 8192
IMAGE_SIZE = (640, 640)

# 模塊名：snake_case
# llm_service.py, custom_dataset.py
```

### 3.2 類型標注

- **所有**函數參數和返回值必須有類型標注
- Tensor 類型使用框架原生類型（`torch.Tensor`、`np.ndarray`）
- 複雜類型使用 `TypeAlias`

```python
import torch
import numpy as np
from numpy.typing import NDArray

ImageArray = NDArray[np.uint8]
BatchTensor = torch.Tensor

def preprocess_image(image: ImageArray, size: tuple[int, int]) -> BatchTensor:
    ...
```

### 3.3 必須遵守的規則

- **禁止在 Claude Code 中直接下載大檔案（模型權重、數據集）**，應製作 Python 腳本放在 `scripts/` 目錄供用戶自行執行
- 模型載入與推理邏輯封裝到 Service 層，路由函數不直接操作模型
- 使用 `logging` 模塊，禁止使用 `print()` 做日誌
- GPU/CPU 設備選擇統一通過配置管理，不 hardcode `cuda:0`
- 大型資料（權重、數據集、向量庫）不進 Git 版控，使用 `.gitignore` 排除
- 環境變數使用 `pydantic-settings` 或 `python-dotenv` 管理
- 禁止 `import *`

---

## 四、模型管理

### 4.1 模型載入模式

```python
# services/model_manager.py
from functools import lru_cache

class ModelManager:
    """統一管理模型的載入與生命週期"""

    def __init__(self):
        self._models: dict[str, Any] = {}

    def load(self, model_name: str, device: str = "auto") -> Any:
        """載入模型，已載入則返回快取"""
        if model_name not in self._models:
            self._models[model_name] = self._do_load(model_name, device)
        return self._models[model_name]

    def unload(self, model_name: str) -> None:
        """釋放模型顯存"""
        if model_name in self._models:
            del self._models[model_name]
            torch.cuda.empty_cache()

@lru_cache()
def get_model_manager() -> ModelManager:
    return ModelManager()
```

### 4.2 設備管理

```python
# utils/device.py
import torch

def get_device(preference: str = "auto") -> torch.device:
    """根據配置和環境自動選擇設備"""
    if preference == "auto":
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            return torch.device("mps")
        return torch.device("cpu")
    return torch.device(preference)
```

### 4.3 權重與大檔案管理

- 模型權重放在 `weights/` 目錄，透過 `scripts/download_weights.py` 下載
- 使用 `.gitignore` 排除：`weights/`、`data/`、`*.pt`、`*.onnx`、`*.bin`、`*.safetensors`
- 下載腳本應包含：進度條、校驗碼驗證、斷點續傳

```python
# scripts/download_weights.py 範例骨架
"""模型權重下載腳本 — 用戶自行執行"""
import argparse
from pathlib import Path
from huggingface_hub import hf_hub_download

def main():
    parser = argparse.ArgumentParser(description="下載模型權重")
    parser.add_argument("--model", required=True, help="模型名稱")
    parser.add_argument("--output", default="weights/", help="輸出目錄")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 下載邏輯
    hf_hub_download(repo_id=args.model, local_dir=str(output_dir))
    print(f"模型已下載至 {output_dir}")

if __name__ == "__main__":
    main()
```

---

## 五、推理服務規範

### 5.1 API 設計

```python
# schemas/prediction.py
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    """推理請求 schema"""
    pass  # 依專案定義

class PredictionResponse(BaseModel):
    """推理回應 schema"""
    pass  # 依專案定義

# schemas/response.py
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None
```

### 5.2 健康檢查端點

```python
@router.get("/health")
async def health_check():
    """服務健康檢查，含 GPU 狀態"""
    gpu_available = torch.cuda.is_available()
    gpu_memory = None
    if gpu_available:
        gpu_memory = {
            "allocated": f"{torch.cuda.memory_allocated() / 1e9:.2f} GB",
            "reserved": f"{torch.cuda.memory_reserved() / 1e9:.2f} GB",
        }
    return {
        "status": "healthy",
        "gpu_available": gpu_available,
        "gpu_memory": gpu_memory,
    }
```

### 5.3 推理效能注意事項

- 使用 `torch.no_grad()` 或 `torch.inference_mode()` 包裹推理邏輯
- 批次推理優先於逐筆處理
- 模型在服務啟動時載入一次，不在每次請求中重新載入
- 大型模型考慮使用量化（INT8 / INT4）降低顯存需求
- 圖片前處理使用高效庫（`cv2`、`Pillow`、`albumentations`）

---

## 六、Prompt 管理（LLM 專案）

### 6.1 Prompt 模板規範

- Prompt 模板存放在 `app/prompts/` 目錄，與程式碼分離
- 使用純文字檔（`.txt`）或 Jinja2 模板，不 hardcode 在程式碼中
- System prompt 和 user prompt 分開管理

```python
# prompts/templates.py
from pathlib import Path

PROMPT_DIR = Path(__file__).parent

def load_prompt(name: str, **kwargs) -> str:
    """載入並格式化 prompt 模板"""
    template = (PROMPT_DIR / f"{name}.txt").read_text(encoding="utf-8")
    return template.format(**kwargs) if kwargs else template
```

### 6.2 RAG 管線注意事項

- Embedding 模型與 LLM 分開管理
- Chunk 大小和 overlap 作為可配置參數
- 檢索結果數量（top_k）可調整
- 記錄每次檢索的 source 文件名與 score，便於調試

---

## 七、數據處理規範

### 7.1 數據管線

- 原始數據放 `data/raw/`，處理後放 `data/processed/`
- 數據轉換腳本放在 `scripts/`，須可重複執行（冪等）
- 大型數據集使用生成器 / DataLoader，避免一次性載入記憶體
- 數據增強配置化，不 hardcode 參數

### 7.2 .gitignore 必須排除項

```gitignore
# 模型權重
weights/
*.pt
*.pth
*.onnx
*.bin
*.safetensors
*.ckpt

# 數據
data/
*.h5
*.hdf5
*.parquet
*.arrow

# 向量庫
vectorstore/
*.faiss

# 實驗追蹤
wandb/
mlruns/
runs/

# 快取
__pycache__/
.cache/
*.pyc
```

---

## 八、測試規範

```python
# 使用 pytest

# 測試文件命名：test_<module>.py
# 測試函數命名：test_<行為描述>

import pytest
import torch

@pytest.fixture
def sample_image() -> torch.Tensor:
    """生成測試用隨機圖片 tensor"""
    return torch.randn(1, 3, 640, 640)

def test_model_output_shape(sample_image):
    """驗證模型輸出形狀正確"""
    model = load_model("test_model")
    output = model(sample_image)
    assert output.shape == (1, 10)  # 依實際需求

@pytest.mark.skipif(not torch.cuda.is_available(), reason="需要 GPU")
def test_gpu_inference(sample_image):
    """GPU 推理測試"""
    ...
```

---

## 九、Docker 部署

### 9.1 GPU Dockerfile 範例

```dockerfile
FROM pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime

WORKDIR /app

# 系統依賴（CV 專案可能需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 9.2 docker-compose GPU 配置

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./weights:/app/weights
      - ./data:/app/data
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    env_file: .env
```

---

## 十、專案指令

| 命令 | 行為 |
|------|------|
| `/init-llm` | 生成 LLM 應用專案骨架（含 RAG 管線、Prompt 管理） |
| `/init-cv` | 生成 CV 專案骨架（含訓練/推理分離結構） |
| `/make-endpoint <name>` | 為指定功能生成推理 API 端點（router、service、schema） |
| `/make-dataset <name>` | 生成自定義 Dataset 類（含數據增強配置） |
| `/make-download <source>` | 生成數據/模型下載腳本（含進度條、校驗） |
| `/export-model <format>` | 生成模型導出腳本（ONNX / TorchScript / TensorRT） |
| `/check-gpu` | 檢查 GPU 環境、CUDA 版本、顯存使用狀況 |
| `/profile-inference` | 對推理管線進行效能分析（延遲、吞吐量、顯存） |
