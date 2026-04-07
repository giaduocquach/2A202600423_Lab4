# 2A202600423_Lab4

TravelBuddy AI Agent cho Lab 4, triển khai bằng LangGraph với 3 custom tools:
- `search_flights`
- `search_hotels`
- `calculate_budget`

Mục tiêu của bài: Agent tự quyết định gọi tool theo ngữ cảnh, xử lý chuỗi nhiều bước và trả lời đúng phạm vi du lịch.

## 1. Cấu trúc dự án

```text
.
├── agent.py            # LangGraph agent loop
├── tools.py            # 3 custom tools + mock data
├── system_prompt.txt   # Prompt điều khiển hành vi agent
├── test_api.py         # Kiểm tra kết nối OpenAI API
├── test_results.md     # Log 5 test case theo đề
├── streamlit_app.py    # UI demo với Streamlit
└── README.md
```

## 2. Yêu cầu môi trường

- Python 3.10+
- OpenAI API key hợp lệ

## 3. Cài đặt

```bash
python -m venv .venv
source .venv/bin/activate
pip install langchain langchain-openai langgraph python-dotenv streamlit
```

Tạo file `.env` tại thư mục gốc:

```env
OPENAI_API_KEY=your_openai_key_here
```

## 4. Cách chạy

### 4.1 Sanity check API

```bash
python test_api.py
```

Kỳ vọng: in ra câu trả lời từ model, xác nhận API hoạt động.

### 4.2 Chạy agent CLI

```bash
python agent.py
```

Thoát bằng `quit`, `exit` hoặc `q`.

### 4.3 Chạy giao diện Streamlit (tuỳ chọn demo)

```bash
streamlit run streamlit_app.py
```

## 5. Checklist bám đề Lab 4

- Có đủ 3 tool yêu cầu với xử lý logic và lỗi.
- Agent graph có đầy đủ nodes, edges, tool routing.
- System prompt có persona, rules, toolsinstruction, response_format, constraints.
- Đã ghi nhận đủ 5 test case trong `test_results.md`.

## 6. File nộp theo đề

Theo Assignment, gói nộp gồm 4 file:
- `system_prompt.txt`
- `tools.py`
- `agent.py`
- `test_results.md`

Lệnh tạo file zip nộp:

```bash
zip -q MSSV_Lab4.zip system_prompt.txt tools.py agent.py test_results.md
```

## 7. Ghi chú

- `streamlit_app.py` là phần mở rộng để demo trực quan, không thay đổi logic core của bài.
- Khi chấm theo rubric, ưu tiên chạy `agent.py` và đối chiếu `test_results.md`.