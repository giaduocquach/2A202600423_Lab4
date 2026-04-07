from __future__ import annotations

import html
import os
import re
import unicodedata
from datetime import datetime
from typing import Any

import streamlit as st
from langchain_core.messages import HumanMessage

from agent import format_message_content, graph


st.set_page_config(
    page_title="TravelBuddy",
    page_icon="TB",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap');

    :root {
        --bg: #f3f4f6;
        --surface: #ffffff;
        --surface-soft: #f8fafc;
        --line: #d9dee7;
        --text: #1f2937;
        --muted: #6b7280;
        --brand: #0f766e;
        --brand-soft: #e8f7f3;
        --user-bg: #ecf2ff;
        --assistant-bg: #ffffff;
        --ok: #0f9d58;
        --warn: #b45309;
    }

    .stApp {
        font-family: "Source Sans 3", sans-serif;
        background: linear-gradient(180deg, #f8f9fb, var(--bg));
        color: var(--text) !important;
    }

    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stBottomBlockContainer"],
    [data-testid="stMain"],
    section.main,
    footer {
        background: var(--bg) !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
        border-bottom: 0 !important;
    }

    .stApp,
    .stApp p,
    .stApp li,
    .stApp span,
    .stApp label,
    .stApp [data-testid="stMarkdownContainer"],
    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stMetricLabel"],
    .stApp [data-testid="stMetricValue"] {
        color: var(--text) !important;
    }

    h1, h2, h3, h4 {
        font-family: "Manrope", sans-serif;
        letter-spacing: -0.02em;
        color: var(--text) !important;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid var(--line);
        background: #ffffff;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1180px;
        padding-top: 0.9rem;
        padding-bottom: 7.4rem;
    }

    .header-wrap {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
        padding: 14px 16px;
        margin-bottom: 10px;
    }

    .chip {
        display: inline-block;
        margin: 0 6px 8px 0;
        padding: 4px 9px;
        border-radius: 999px;
        border: 1px solid #c5e7df;
        background: var(--brand-soft);
        color: #0d6a5e !important;
        font-size: 12px;
        font-weight: 700;
    }

    .title {
        margin: 0;
        font-size: 28px;
        line-height: 1.1;
    }

    .subtitle {
        margin: 7px 0 0 0;
        color: var(--muted) !important;
        font-size: 15px;
    }

    .panel {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
        padding: 11px 12px;
        margin-bottom: 10px;
    }

    .panel-note {
        margin: 4px 0 0 0;
        color: var(--muted) !important;
        font-size: 13px;
    }

    .empty-box {
        border: 1px dashed #c6d2e1;
        border-radius: 12px;
        background: #fbfcff;
        color: var(--muted) !important;
        padding: 14px;
    }

    .timeline-step {
        border: 1px solid #dde4ef;
        border-radius: 8px;
        background: #ffffff;
        padding: 8px 9px;
        margin-bottom: 7px;
        font-size: 14px;
    }

    .status-ok {
        color: var(--ok) !important;
        font-weight: 700;
    }

    .status-warn {
        color: var(--warn) !important;
        font-weight: 700;
    }

    [data-testid="stChatMessage"] {
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 8px 10px;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.06);
        background: var(--assistant-bg);
    }

    [data-testid="stChatMessage"]:has([aria-label="user avatar"]) {
        background: var(--user-bg);
        border-left: 5px solid #2563eb;
    }

    [data-testid="stChatMessage"]:has([aria-label="assistant avatar"]) {
        border-left: 5px solid var(--brand);
    }

    [data-testid="stChatMessage"] table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin: 0.6rem 0 0.45rem 0;
        border: 1px solid #d5deea;
        border-radius: 10px;
        overflow: hidden;
        font-size: 14px;
        table-layout: fixed;
    }

    [data-testid="stChatMessage"] thead th {
        background: #ecfdf5;
        color: #065f46 !important;
        font-weight: 700;
        border-bottom: 1px solid #cfe4dc;
        padding: 10px 11px;
        text-align: left;
        white-space: normal;
    }

    [data-testid="stChatMessage"] tbody td {
        padding: 9px 11px;
        border-bottom: 1px solid #edf2f7;
        border-right: 1px solid #edf2f7;
        vertical-align: top;
        word-break: break-word;
    }

    [data-testid="stChatMessage"] tbody tr td:last-child,
    [data-testid="stChatMessage"] thead tr th:last-child {
        border-right: none;
    }

    [data-testid="stChatMessage"] tbody tr:last-child td {
        border-bottom: none;
    }

    [data-testid="stChatMessage"] tbody tr:nth-child(even) td {
        background: #fafcff;
    }

    [data-testid="stChatMessage"] th:nth-child(1),
    [data-testid="stChatMessage"] td:nth-child(1) {
        width: 27%;
    }

    [data-testid="stChatMessage"] th:nth-child(2),
    [data-testid="stChatMessage"] td:nth-child(2) {
        width: 13%;
    }

    [data-testid="stChatMessage"] th:nth-child(3),
    [data-testid="stChatMessage"] td:nth-child(3) {
        width: 18%;
    }

    [data-testid="stChatMessage"] th:nth-child(4),
    [data-testid="stChatMessage"] td:nth-child(4) {
        width: 24%;
    }

    [data-testid="stChatMessage"] th:nth-child(5),
    [data-testid="stChatMessage"] td:nth-child(5) {
        width: 18%;
    }

    .msg-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
        color: var(--muted) !important;
        font-size: 12px;
    }

    .msg-meta .role {
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #334155 !important;
    }

    .tool-line {
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        font-size: 12px;
        color: #122334 !important;
        background: var(--surface-soft);
        border: 1px solid #dde5f0;
        border-radius: 8px;
        padding: 6px 7px;
        margin-bottom: 6px;
    }

    .tool-line:last-child {
        margin-bottom: 0;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid var(--line);
        background: #ffffff;
        color: var(--text) !important;
        font-weight: 600;
        transition: all 0.15s ease;
    }

    .stButton > button:hover {
        background: #f8fafc;
        border-color: #c6cfdb;
        color: #111827 !important;
    }

    .stButton > button[kind="primary"] {
        background: #16a34a;
        border-color: #16a34a;
        color: #ffffff !important;
        font-weight: 700;
    }

    .stButton > button[kind="primary"]:hover {
        background: #15803d;
        border-color: #15803d;
        color: #ffffff !important;
    }

    pre, code {
        color: #111827 !important;
    }

    div[data-testid="stChatInput"] {
        position: fixed;
        left: clamp(1rem, 24vw, 23rem);
        right: 1.5rem;
        bottom: 0.95rem;
        z-index: 999;
        background: rgba(255, 255, 255, 0.98);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 0.45rem 0.55rem;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
        backdrop-filter: blur(4px);
        overflow: hidden;
    }

    div[data-testid="stChatInput"] > div {
        background: #ffffff !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    div[data-testid="stChatInput"] textarea,
    div[data-testid="stChatInput"] input {
        background: #ffffff !important;
        color: #111827 !important;
        border: 1px solid var(--line) !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }

    div[data-testid="stChatInput"]:focus-within,
    div[data-testid="stChatInput"] textarea:focus,
    div[data-testid="stChatInput"] input:focus {
        border-color: #b7c2d3 !important;
        box-shadow: none !important;
        outline: none !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder,
    div[data-testid="stChatInput"] input::placeholder {
        color: #6b7280 !important;
        opacity: 1 !important;
    }

    div[data-testid="stChatInput"] button {
        background: var(--brand) !important;
        color: #ffffff !important;
        border: 1px solid var(--brand) !important;
        border-radius: 10px !important;
    }

    div[data-testid="stChatInput"] button:hover {
        background: #0b675f !important;
        border-color: #0b675f !important;
        color: #ffffff !important;
    }

    div[data-testid="stChatInput"]::before,
    div[data-testid="stChatInput"]::after {
        display: none !important;
    }

    [data-testid="stChatInput"] * {
        border-bottom-color: var(--line) !important;
    }

    [data-testid="stChatInput"] div[data-baseweb="base-input"],
    [data-testid="stChatInput"] div[data-baseweb="textarea"],
    [data-testid="stChatInput"] div[data-baseweb="textarea"] > div {
        background: #ffffff !important;
        box-shadow: none !important;
        border-radius: 10px !important;
    }

    @media (max-width: 1200px) {
        div[data-testid="stChatInput"] {
            left: 1rem;
            right: 1rem;
        }
    }

    @media (max-width: 960px) {
        .title {
            font-size: 23px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


QUICK_PROMPTS = [
    ("Tìm chuyến bay", "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"),
    (
        "Tư vấn trọn gói",
        "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
    ),
    ("Đặt khách sạn", "Tôi muốn đặt khách sạn"),
    ("Kiểm thử guardrail", "Giải giúp tôi bài tập lập trình Python về linked list"),
]
TOOL_ORDER = ["search_flights", "search_hotels", "calculate_budget"]


def _now() -> str:
    return datetime.now().strftime("%H:%M:%S")


def _normalize_text(text: str) -> str:
    text = text.strip().lower().replace("đ", "d")
    text = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def _infer_intent_and_expected_tools(user_text: str) -> tuple[str, list[str]]:
    text = _normalize_text(user_text)
    has_flight = any(k in text for k in ["chuyen bay", "ve may bay", "dat ve", "bay"])
    has_hotel = any(k in text for k in ["khach san", "dat phong", "homestay", "resort"])
    has_budget = any(k in text for k in ["budget", "ngan sach", "chi phi", "con lai", "trieu"])
    has_nights = "dem" in text
    has_plan = any(k in text for k in ["tu van", "goi y", "len ke hoach", "chuyen di"])

    full_trip = (has_plan and (has_budget or has_nights)) or (has_flight and has_hotel)
    if full_trip:
        return "Tư vấn chuyến đi trọn gói", TOOL_ORDER.copy()
    if has_flight:
        return "Tìm chuyến bay", ["search_flights"]
    if has_hotel:
        return "Tìm khách sạn", ["search_hotels"]
    if has_budget:
        return "Tính ngân sách", ["calculate_budget"]
    return "Hỏi đáp chung", []


def _is_expected_order(called_names: list[str], expected_order: list[str]) -> bool:
    expected_index = 0
    for name in called_names:
        if expected_index < len(expected_order) and name == expected_order[expected_index]:
            expected_index += 1
    return expected_index == len(expected_order)


def _evaluate_tool_coverage(user_text: str, calls: list[dict[str, Any]]) -> dict[str, Any]:
    intent, expected = _infer_intent_and_expected_tools(user_text)
    called_all = [str(call.get("name", "")) for call in calls]
    called_core = [name for name in called_all if name in TOOL_ORDER]

    missing = [name for name in expected if name not in set(called_core)]
    if not expected:
        return {
            "intent": intent,
            "expected": expected,
            "called": called_core,
            "status": "Lượt này không bắt buộc gọi tool.",
            "level": "ok",
        }

    if not called_core:
        return {
            "intent": intent,
            "expected": expected,
            "called": called_core,
            "status": "Chưa gọi tool ở lượt này.",
            "level": "warn",
        }

    if not missing:
        if expected == TOOL_ORDER and not _is_expected_order(called_core, TOOL_ORDER):
            return {
                "intent": intent,
                "expected": expected,
                "called": called_core,
                "status": "Đã đủ tool nhưng thứ tự chưa tối ưu theo quy trình chuẩn.",
                "level": "warn",
            }
        return {
            "intent": intent,
            "expected": expected,
            "called": called_core,
            "status": "Đã gọi đầy đủ tool theo ngữ cảnh.",
            "level": "ok",
        }

    return {
        "intent": intent,
        "expected": expected,
        "called": called_core,
        "status": f"Thiếu tool: {', '.join(missing)}.",
        "level": "warn",
    }


def _build_reasoning_steps(user_text: str, calls: list[dict[str, Any]]) -> list[str]:
    check = _evaluate_tool_coverage(user_text, calls)
    expected_text = ", ".join(check["expected"]) if check["expected"] else "Không bắt buộc"
    called_text = ", ".join(check["called"]) if check["called"] else "Không gọi tool"

    steps = [
        f"Nhận diện ý định: {check['intent']}",
        f"Xác định tool cần dùng: {expected_text}",
        f"Tool thực tế đã gọi: {called_text}",
    ]

    if check["expected"] == TOOL_ORDER and check["called"]:
        if _is_expected_order(check["called"], TOOL_ORDER):
            steps.append("Thứ tự gọi tool đúng quy trình chuẩn.")
        else:
            steps.append("Thứ tự gọi tool chưa khớp hoàn toàn quy trình chuẩn.")

    steps.append(f"Kết luận: {check['status']}")
    return steps


def _auto_tableize_markdown(content: str) -> str:
    def _normalize_inline_table_block(text: str) -> str:
        normalized_lines: list[str] = []

        for raw_line in str(text).replace("\r\n", "\n").split("\n"):
            line = raw_line.strip()
            if "|---" not in line or line.count("|") < 6:
                normalized_lines.append(raw_line)
                continue

            first_pipe_idx = line.find("|")
            if first_pipe_idx < 0:
                normalized_lines.append(raw_line)
                continue

            prefix = line[:first_pipe_idx].strip()
            table_part = line[first_pipe_idx:].strip()

            # Split collapsed boundaries like "| ... || ... |" or "| ... |   | ... |".
            table_part = re.sub(r"\|\s*\|", "|\n|", table_part)
            # Ensure markdown separator row stays isolated when glued to the first data row.
            table_part = re.sub(r"((?:\|\s*:?-{3,}:?\s*)+\|)\s*(?=\|)", r"\1\n", table_part)

            if prefix:
                normalized_lines.append(prefix)
                normalized_lines.append("")

            for tbl_line in table_part.split("\n"):
                clean = tbl_line.strip()
                if clean:
                    normalized_lines.append(clean)

        return "\n".join(normalized_lines)

    lines = _normalize_inline_table_block(content).split("\n")
    output: list[str] = []
    i = 0

    def _strip_list_prefix(raw: str) -> str:
        text = raw.strip()
        text = re.sub(r"^[-*]\s+", "", text)
        text = re.sub(r"^\d+[.)]\s*", "", text)
        return text

    def _split_pipe_cells(raw: str) -> list[str]:
        text = _strip_list_prefix(raw)
        if text.startswith("|") and text.endswith("|"):
            text = text[1:-1]
        cells = [part.strip() for part in text.split("|")]
        return [cell for cell in cells if cell]

    def _is_separator_line(raw: str) -> bool:
        cells = _split_pipe_cells(raw)
        return len(cells) >= 2 and all(re.fullmatch(r":?-{3,}:?", c) for c in cells)

    def _is_pipe_row(raw: str) -> bool:
        if "|" not in raw:
            return False
        cells = _split_pipe_cells(raw)
        if len(cells) < 3:
            return False
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
            return False
        return True

    def _choose_headers(sample_row: list[str]) -> list[str]:
        col_count = len(sample_row)
        if col_count == 5:
            return ["Khách sạn", "Hạng sao", "Khu vực", "Giá", "Rating"]
        if col_count == 4:
            return ["Mục 1", "Mục 2", "Mục 3", "Mục 4"]
        return [f"Cột {idx}" for idx in range(1, col_count + 1)]

    def _render_table(rows: list[list[str]]) -> list[str]:
        headers = _choose_headers(rows[0])
        col_count = len(headers)
        out: list[str] = []
        out.append("| " + " | ".join(headers) + " |")
        out.append("|" + "|".join(["---"] * col_count) + "|")
        for row in rows:
            safe_row = [cell.replace("|", "\\|") for cell in row]
            out.append("| " + " | ".join(safe_row) + " |")
        return out

    while i < len(lines):
        line = lines[i]

        # Keep explicit markdown tables as-is (header + separator + rows).
        if _is_pipe_row(line) and i + 1 < len(lines) and _is_separator_line(lines[i + 1]):
            header_cells = _split_pipe_cells(line)
            col_count = len(header_cells)
            output.append("| " + " | ".join(header_cells) + " |")
            output.append("|" + "|".join(["---"] * col_count) + "|")
            i += 2
            while i < len(lines) and _is_pipe_row(lines[i]):
                row = _split_pipe_cells(lines[i])
                if len(row) != col_count:
                    break
                safe_row = [cell.replace("|", "\\|") for cell in row]
                output.append("| " + " | ".join(safe_row) + " |")
                i += 1
            continue

        # Auto-convert consecutive pipe rows when no explicit separator exists.
        if _is_pipe_row(line):
            pipe_block: list[list[str]] = []
            j = i
            while j < len(lines) and _is_pipe_row(lines[j]):
                row = _split_pipe_cells(lines[j])
                if not pipe_block or len(row) == len(pipe_block[0]):
                    pipe_block.append(row)
                    j += 1
                    continue
                break

            if len(pipe_block) >= 2 and len(pipe_block[0]) >= 3:
                output.extend(_render_table(pipe_block))
                i = j
                continue

        if re.match(r"^\s*[-*]\s+", line) and "|" not in line:
            block: list[str] = []
            j = i
            while j < len(lines) and re.match(r"^\s*[-*]\s+", lines[j]) and "|" not in lines[j]:
                block.append(lines[j])
                j += 1

            rows: list[tuple[str, str]] = []
            all_colon = True
            for bullet in block:
                body = re.sub(r"^\s*[-*]\s+", "", bullet).strip()
                if ":" not in body:
                    all_colon = False
                    break
                key, value = body.split(":", 1)
                rows.append((key.strip(), value.strip()))

            if all_colon and len(rows) >= 2:
                if any((not value) for _, value in rows):
                    output.extend(block)
                    i = j
                    continue
                output.append("| Hạng mục | Chi tiết |")
                output.append("|---|---|")
                for key, value in rows:
                    safe_key = key.replace("|", "\\|")
                    safe_value = value.replace("|", "\\|")
                    output.append(f"| {safe_key} | {safe_value} |")
            else:
                output.extend(block)

            i = j
            continue

        output.append(line)
        i += 1

    return "\n".join(output)


def _init_state() -> None:
    defaults: dict[str, Any] = {
        "graph_messages": [],
        "chat_log": [],
        "tool_history": [],
        "pending_prompt": "",
        "queued_prompt": "",
        "is_processing": False,
        "show_tool_details": True,
        "session_start": datetime.now(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _reset_session() -> None:
    st.session_state.graph_messages = []
    st.session_state.chat_log = []
    st.session_state.tool_history = []
    st.session_state.pending_prompt = ""
    st.session_state.queued_prompt = ""
    st.session_state.is_processing = False
    st.session_state.session_start = datetime.now()


def _append_turn(role: str, content: str, tool_calls: list[dict[str, Any]] | None = None) -> None:
    st.session_state.chat_log.append(
        {
            "role": role,
            "content": content,
            "tool_calls": tool_calls or [],
            "time": _now(),
        }
    )


def _run_agent_turn(user_text: str) -> tuple[str, list[dict[str, Any]]]:
    prev_len = len(st.session_state.graph_messages)
    result = graph.invoke({"messages": st.session_state.graph_messages + [HumanMessage(content=user_text)]})
    new_messages = result["messages"]

    calls: list[dict[str, Any]] = []
    for msg in new_messages[prev_len:]:
        tool_calls = getattr(msg, "tool_calls", None)
        if tool_calls:
            for call in tool_calls:
                calls.append(
                    {
                        "name": call.get("name", ""),
                        "args": call.get("args", {}),
                    }
                )

    st.session_state.graph_messages = new_messages
    return format_message_content(new_messages[-1].content), calls


def _latest_turn_pair() -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    log = st.session_state.chat_log
    for idx in range(len(log) - 1, 0, -1):
        if log[idx]["role"] == "assistant" and log[idx - 1]["role"] == "user":
            return log[idx - 1], log[idx]
    return None, None


def _render_header() -> None:
    st.markdown(
        """
        <div class="header-wrap">
            <span class="chip">TravelBuddy</span>
            <span class="chip">Phong cách chatbot hiện đại</span>
            <span class="chip">Hiển thị đầy đủ tool calls</span>
            <h1 class="title">TravelBuddy Chat Console</h1>
            <p class="subtitle">Giao diện tập trung vào trải nghiệm hội thoại, giảm nhiễu màu và giữ đầy đủ thông tin theo dõi kỹ thuật.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_metrics() -> None:
    total_user = sum(1 for item in st.session_state.chat_log if item["role"] == "user")
    total_assistant = sum(1 for item in st.session_state.chat_log if item["role"] == "assistant")
    total_calls = len(st.session_state.tool_history)
    elapsed = int((datetime.now() - st.session_state.session_start).total_seconds() // 60)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Lượt người dùng", total_user)
    c2.metric("Lượt trợ lý", total_assistant)
    c3.metric("Tool calls", total_calls)
    c4.metric("Thời lượng", f"{elapsed} phút")


def _render_messages() -> None:
    if not st.session_state.chat_log:
        st.markdown(
            """
            <div class="empty-box">Chưa có hội thoại. Chọn mẫu truy vấn bên trái hoặc nhập câu hỏi ở thanh chat phía dưới.</div>
            """,
            unsafe_allow_html=True,
        )
        return

    for item in st.session_state.chat_log:
        role = item.get("role", "assistant")
        role_name = "Bạn" if role == "user" else "TravelBuddy"
        avatar = "🧑" if role == "user" else "🤖"

        with st.chat_message("user" if role == "user" else "assistant", avatar=avatar):
            st.markdown(
                f"<div class='msg-meta'><span class='role'>{html.escape(role_name)}</span><span>{html.escape(item.get('time', '--:--:--'))}</span></div>",
                unsafe_allow_html=True,
            )
            # Markdown render giúp hiển thị đúng in đậm, bullet và bảng.
            content = str(item.get("content", ""))
            if role == "assistant":
                content = _auto_tableize_markdown(content)
            st.markdown(content)

            calls = item.get("tool_calls") or []
            if st.session_state.show_tool_details and calls:
                with st.expander(f"Tool calls ({len(calls)})", expanded=False):
                    for call_idx, call in enumerate(calls, start=1):
                        name = html.escape(str(call.get("name", "")))
                        args = html.escape(str(call.get("args", {})))
                        st.markdown(
                            f"<div class='tool-line'>{call_idx}. {name}({args})</div>",
                            unsafe_allow_html=True,
                        )

    if st.session_state.is_processing and st.session_state.queued_prompt:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(
                f"<div class='msg-meta'><span class='role'>TravelBuddy</span><span>{html.escape(_now())}</span></div>",
                unsafe_allow_html=True,
            )
            st.markdown("Đang phân tích yêu cầu và gọi tool phù hợp...")


def _render_inspector() -> None:
    st.markdown(
        """
        <div class="panel">
            <h4>Bảng điều khiển</h4>
            <p class="panel-note">Theo dõi quá trình xử lý và kiểm tra độ đầy đủ của tool calls theo từng lượt.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.is_processing and st.session_state.queued_prompt:
        live_prompt = str(st.session_state.queued_prompt)
        live_steps = _build_reasoning_steps(live_prompt, [])

        st.markdown("### Trình tự xử lý gần nhất")
        st.markdown(
            "<div class='timeline-step'>Trạng thái: <span class='status-warn'>Đang xử lý câu hỏi mới...</span></div>",
            unsafe_allow_html=True,
        )

        st.markdown("### Quá trình tư duy (tóm tắt)")
        st.caption("Hiển thị tức thì định hướng xử lý theo ý định ngay sau khi bấm gửi.")
        for idx, step in enumerate(live_steps, start=1):
            st.markdown(
                f"<div class='timeline-step'>{idx}. {html.escape(step)}</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            """
            <div class="empty-box">Tool calls sẽ xuất hiện ngay khi agent thực thi xong lượt hiện tại.</div>
            """,
            unsafe_allow_html=True,
        )
        return

    user_item, assistant_item = _latest_turn_pair()
    if user_item and assistant_item:
        calls = assistant_item.get("tool_calls") or []
        check = _evaluate_tool_coverage(str(user_item.get("content", "")), calls)
        steps = _build_reasoning_steps(str(user_item.get("content", "")), calls)
        status_class = "status-ok" if check["level"] == "ok" else "status-warn"

        st.markdown("### Trình tự xử lý gần nhất")
        st.markdown(
            f"<div class='timeline-step'>Trạng thái: <span class='{status_class}'>{html.escape(check['status'])}</span></div>",
            unsafe_allow_html=True,
        )

        st.markdown("### Quá trình tư duy (tóm tắt)")
        st.caption("Dựa trên dấu hiệu ý định và hành vi gọi tool, không hiển thị suy luận nội bộ chi tiết của mô hình.")
        for idx, step in enumerate(steps, start=1):
            st.markdown(
                f"<div class='timeline-step'>{idx}. {html.escape(step)}</div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class="empty-box">Chưa có đủ dữ liệu để hiển thị trình tự xử lý.</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Lịch sử tool calls")
    if st.session_state.tool_history:
        for event in st.session_state.tool_history[-10:][::-1]:
            stamp = html.escape(str(event["time"]))
            name = html.escape(str(event["name"]))
            args = html.escape(str(event["args"]))
            st.markdown(
                f"<div class='tool-line'>{stamp} | {name}({args})</div>",
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            """
            <div class="empty-box">Chưa có dữ liệu tool calls trong phiên này.</div>
            """,
            unsafe_allow_html=True,
        )


_init_state()


with st.sidebar:
    st.title("TravelBuddy")
    st.caption("Điều khiển phiên")

    if os.getenv("OPENAI_API_KEY"):
        st.success("OpenAI API: Sẵn sàng")
    else:
        st.warning("OpenAI API: Chưa thấy key")

    st.toggle("Hiển thị chi tiết tool calls", key="show_tool_details")

    st.markdown("### Mẫu truy vấn")
    for idx, (label, prompt) in enumerate(QUICK_PROMPTS, start=1):
        if st.button(label, key=f"quick_prompt_{idx}", use_container_width=True):
            st.session_state.pending_prompt = prompt

    st.markdown("### Quản lý")
    if st.button("Tạo phiên mới", use_container_width=True, type="primary"):
        _reset_session()
        st.rerun()


st.markdown("### TravelBuddy Chat")


chat_col, info_col = st.columns([2.35, 1.0], gap="large")

with chat_col:
    _render_messages()

with info_col:
    _render_inspector()


typed_prompt = st.chat_input("Nhập yêu cầu du lịch của bạn...")
incoming_prompt = typed_prompt or st.session_state.pending_prompt

if incoming_prompt and not st.session_state.is_processing:
    st.session_state.pending_prompt = ""
    st.session_state.queued_prompt = incoming_prompt
    st.session_state.is_processing = True
    _append_turn("user", incoming_prompt)
    st.rerun()

if st.session_state.is_processing and st.session_state.queued_prompt:
    prompt_to_run = st.session_state.queued_prompt
    with st.spinner("TravelBuddy đang xử lý..."):
        answer, calls = _run_agent_turn(prompt_to_run)

    _append_turn("assistant", answer, calls)
    for call in calls:
        st.session_state.tool_history.append(
            {
                "time": _now(),
                "name": call.get("name", ""),
                "args": call.get("args", {}),
            }
        )

    st.session_state.queued_prompt = ""
    st.session_state.is_processing = False

    st.rerun()