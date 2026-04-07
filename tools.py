from __future__ import annotations

import re
import unicodedata
from typing import Optional

from langchain_core.tools import tool


# Mock data cho bài lab.
FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1_450_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "08:30",
            "arrival": "09:50",
            "price": 890_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "11:00",
            "arrival": "12:20",
            "price": 1_200_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "14:00",
            "arrival": "15:20",
            "price": 2_800_000,
            "class": "business",
        },
    ],
    ("Hà Nội", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "07:00",
            "arrival": "09:15",
            "price": 2_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "10:00",
            "arrival": "12:15",
            "price": 1_350_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "16:00",
            "arrival": "18:15",
            "price": 1_100_000,
            "class": "economy",
        },
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "08:10",
            "price": 1_600_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "07:30",
            "arrival": "09:40",
            "price": 950_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "12:00",
            "arrival": "14:10",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "18:00",
            "arrival": "20:10",
            "price": 3_200_000,
            "class": "business",
        },
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "09:00",
            "arrival": "10:20",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "13:00",
            "arrival": "14:20",
            "price": 780_000,
            "class": "economy",
        },
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "08:00",
            "arrival": "09:00",
            "price": 1_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "15:00",
            "arrival": "16:00",
            "price": 650_000,
            "class": "economy",
        },
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {
            "name": "Muong Thanh Luxury",
            "stars": 5,
            "price_per_night": 1_800_000,
            "area": "Mỹ Khê",
            "rating": 4.5,
        },
        {
            "name": "Sala Danang Beach",
            "stars": 4,
            "price_per_night": 1_200_000,
            "area": "Mỹ Khê",
            "rating": 4.3,
        },
        {
            "name": "Fivitel Danang",
            "stars": 3,
            "price_per_night": 650_000,
            "area": "Sơn Trà",
            "rating": 4.1,
        },
        {
            "name": "Memory Hostel",
            "stars": 2,
            "price_per_night": 250_000,
            "area": "Hải Châu",
            "rating": 4.6,
        },
        {
            "name": "Christina's Homestay",
            "stars": 2,
            "price_per_night": 350_000,
            "area": "An Thượng",
            "rating": 4.7,
        },
    ],
    "Phú Quốc": [
        {
            "name": "Vinpearl Resort",
            "stars": 5,
            "price_per_night": 3_500_000,
            "area": "Bãi Dài",
            "rating": 4.4,
        },
        {
            "name": "Sol by Melia",
            "stars": 4,
            "price_per_night": 1_500_000,
            "area": "Bãi Trường",
            "rating": 4.2,
        },
        {
            "name": "Lahana Resort",
            "stars": 3,
            "price_per_night": 800_000,
            "area": "Dương Đông",
            "rating": 4.0,
        },
        {
            "name": "9Station Hostel",
            "stars": 2,
            "price_per_night": 200_000,
            "area": "Dương Đông",
            "rating": 4.5,
        },
    ],
    "Hồ Chí Minh": [
        {
            "name": "Rex Hotel",
            "stars": 5,
            "price_per_night": 2_800_000,
            "area": "Quận 1",
            "rating": 4.3,
        },
        {
            "name": "Liberty Central",
            "stars": 4,
            "price_per_night": 1_400_000,
            "area": "Quận 1",
            "rating": 4.1,
        },
        {
            "name": "Cochin Zen Hotel",
            "stars": 3,
            "price_per_night": 550_000,
            "area": "Quận 3",
            "rating": 4.4,
        },
        {
            "name": "The Common Room",
            "stars": 2,
            "price_per_night": 180_000,
            "area": "Quận 1",
            "rating": 4.6,
        },
    ],
}

CITY_ALIASES = {
    "ha noi": "Hà Nội",
    "hanoi": "Hà Nội",
    "hn": "Hà Nội",
    "da nang": "Đà Nẵng",
    "danang": "Đà Nẵng",
    "dn": "Đà Nẵng",
    "ho chi minh": "Hồ Chí Minh",
    "hcm": "Hồ Chí Minh",
    "tphcm": "Hồ Chí Minh",
    "sai gon": "Hồ Chí Minh",
    "saigon": "Hồ Chí Minh",
    "phu quoc": "Phú Quốc",
    "pq": "Phú Quốc",
}

ALL_CITIES = sorted(
    {
        city
        for route in FLIGHTS_DB
        for city in route
    }
    | set(HOTELS_DB.keys())
)


def _normalize_text(text: str) -> str:
    text = text.strip().lower().replace("đ", "d")
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"\s+", " ", text)
    return text


def _resolve_city(city: str) -> Optional[str]:
    key = _normalize_text(city)
    if key in CITY_ALIASES:
        return CITY_ALIASES[key]
    for known_city in ALL_CITIES:
        if _normalize_text(known_city) == key:
            return known_city
    return None


def _format_vnd(amount: int) -> str:
    return f"{amount:,.0f}".replace(",", ".") + "đ"


@tool
def search_flights(origin: str, destination: str) -> str:
    """Tìm chuyến bay giữa hai thành phố.

    Args:
        origin: Thành phố khởi hành. Ví dụ: Hà Nội, Hồ Chí Minh.
        destination: Thành phố đến. Ví dụ: Đà Nẵng, Phú Quốc.

    Returns:
        Danh sách chuyến bay đã format dễ đọc.
    """
    origin_city = _resolve_city(origin)
    destination_city = _resolve_city(destination)

    if not origin_city or not destination_city:
        return (
            "Không nhận diện được thành phố. "
            f"Các thành phố hỗ trợ: {', '.join(ALL_CITIES)}."
        )

    if origin_city == destination_city:
        return "Điểm đi và điểm đến đang giống nhau. Vui lòng nhập 2 thành phố khác nhau."

    flights = FLIGHTS_DB.get((origin_city, destination_city))
    note = ""

    if not flights:
        flights = FLIGHTS_DB.get((destination_city, origin_city))
        if flights:
            note = (
                f"Không có dữ liệu chiều {origin_city} -> {destination_city}. "
                f"Hiển thị chiều ngược {destination_city} -> {origin_city} để tham khảo.\n"
            )

    if not flights:
        return f"Không tìm thấy chuyến bay từ {origin_city} đến {destination_city}."

    flights = sorted(flights, key=lambda x: x["price"])
    lines = [
        f"Danh sách chuyến bay {origin_city} -> {destination_city}:" if not note else note.strip(),
    ]

    for idx, flight in enumerate(flights, start=1):
        lines.append(
            (
                f"{idx}. {flight['airline']} | {flight['departure']} - {flight['arrival']} | "
                f"{flight['class']} | {_format_vnd(flight['price'])}"
            )
        )

    best = flights[0]
    lines.append(
        "Gợi ý vé tiết kiệm: "
        f"{best['airline']} lúc {best['departure']} ({_format_vnd(best['price'])})."
    )
    return "\n".join(lines)


@tool
def search_hotels(city: str, max_price_per_night: int = 999_999_999) -> str:
    """Tìm khách sạn theo thành phố và mức giá tối đa mỗi đêm.

    Args:
        city: Thành phố cần tìm khách sạn.
        max_price_per_night: Ngân sách tối đa mỗi đêm (VND).

    Returns:
        Danh sách khách sạn phù hợp theo rating giảm dần.
    """
    city_name = _resolve_city(city)
    if not city_name or city_name not in HOTELS_DB:
        return (
            f"Không tìm thấy dữ liệu khách sạn cho '{city}'. "
            f"Các thành phố hỗ trợ: {', '.join(HOTELS_DB.keys())}."
        )

    if max_price_per_night <= 0:
        return "max_price_per_night phải lớn hơn 0."

    hotels = [
        hotel
        for hotel in HOTELS_DB[city_name]
        if hotel["price_per_night"] <= max_price_per_night
    ]
    hotels.sort(key=lambda h: (-h["rating"], h["price_per_night"]))

    if not hotels:
        return (
            f"Không tìm thấy khách sạn tại {city_name} với giá dưới "
            f"{_format_vnd(max_price_per_night)}/đêm. Hãy tăng ngân sách."
        )

    lines = [
        (
            f"Khách sạn tại {city_name} (<= {_format_vnd(max_price_per_night)}/đêm), "
            "xếp theo rating giảm dần:"
        )
    ]

    for idx, hotel in enumerate(hotels, start=1):
        lines.append(
            (
                f"{idx}. {hotel['name']} | {hotel['stars']} sao | "
                f"{hotel['area']} | {_format_vnd(hotel['price_per_night'])}/đêm | "
                f"rating {hotel['rating']:.1f}"
            )
        )

    highlight = hotels[0]
    lines.append(
        "Gợi ý nổi bật: "
        f"{highlight['name']} ({highlight['rating']:.1f}⭐, {_format_vnd(highlight['price_per_night'])}/đêm)."
    )
    return "\n".join(lines)


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính ngân sách còn lại sau khi trừ các khoản chi.

    Args:
        total_budget: Tổng ngân sách ban đầu (VND).
        expenses: Chuỗi chi phí dạng 'ten_khoan:so_tien, khoan_2:so_tien'.

    Returns:
        Bảng chi phí và phần ngân sách còn lại.
    """
    if total_budget <= 0:
        return "total_budget phải lớn hơn 0."

    try:
        pairs = [chunk.strip() for chunk in expenses.split(",") if chunk.strip()]
        if not pairs:
            return "Chuỗi expenses đang rỗng. Ví dụ hợp lệ: ve_may_bay:890000, khach_san:650000"

        parsed_items: list[tuple[str, int]] = []

        for pair in pairs:
            if ":" not in pair:
                return (
                    "Sai định dạng expenses. Mỗi khoản phải có dạng tên:số_tiền, "
                    f"nhưng nhận được '{pair}'."
                )

            name, raw_amount = pair.split(":", 1)
            name = name.strip().replace("_", " ")
            if not name:
                return "Tên khoản chi không được để trống."

            clean_amount = (
                raw_amount.strip()
                .lower()
                .replace("vnd", "")
                .replace("đ", "")
                .replace(".", "")
                .replace(",", "")
                .replace("_", "")
                .replace(" ", "")
            )

            if not clean_amount.isdigit():
                return (
                    "Số tiền không hợp lệ ở khoản "
                    f"'{name}'. Hãy dùng số nguyên dương, ví dụ 1250000."
                )

            amount = int(clean_amount)
            parsed_items.append((name, amount))

        total_expense = sum(amount for _, amount in parsed_items)
        remaining = total_budget - total_expense

        lines = ["Bảng chi phí:"]
        for name, amount in parsed_items:
            lines.append(f"- {name}: {_format_vnd(amount)}")

        lines.extend(
            [
                "---",
                f"Tổng chi: {_format_vnd(total_expense)}",
                f"Ngân sách: {_format_vnd(total_budget)}",
                f"Còn lại: {_format_vnd(remaining)}",
            ]
        )

        if remaining < 0:
            lines.append(f"Vượt ngân sách {_format_vnd(-remaining)}! Cần điều chỉnh.")

        return "\n".join(lines)

    except Exception as exc:  # pragma: no cover
        return f"Lỗi khi xử lý expenses: {exc}"
