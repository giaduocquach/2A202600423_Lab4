# Lab 4 Test Results

## Test 1 - Direct Answer (Không cần tool)
User:
Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

Kết quả console:
[TOOL CALL] Không gọi tool (trả lời trực tiếp)
ASSISTANT:
Xin chào! Rất vui được hỗ trợ bạn. Bạn có thể cho tôi biết một số sở thích của bạn về điểm đến không? Bạn dự định đi vào thời gian nào và ngân sách của bạn khoảng bao nhiêu?

Đánh giá:
- Có chào hỏi và hỏi thêm sở thích/ngân sách/thời gian: [x]
- Không gọi tool: [x]

## Test 2 - Single Tool Call
User:
Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng.

Kết quả console:
[TOOL CALL] search_flights args={'origin': 'Hà Nội', 'destination': 'Đà Nẵng'}
[TOOL CALL] Không gọi tool (trả lời trực tiếp)
ASSISTANT:
Dưới đây là danh sách chuyến bay từ Hà Nội đi Đà Nẵng:

1. VietJet Air | 08:30 - 09:50 | economy | 890.000đ
2. Bamboo Airways | 11:00 - 12:20 | economy | 1.200.000đ
3. Vietnam Airlines | 06:00 - 07:20 | economy | 1.450.000đ
4. Vietnam Airlines | 14:00 - 15:20 | business | 2.800.000đ

Gợi ý vé tiết kiệm: VietJet Air lúc 08:30 (890.000đ).

Đánh giá:
- Có gọi search_flights: [x]
- Liệt kê được các chuyến bay hợp lệ: [x]

## Test 3 - Multi-Step Tool Chaining
User:
Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

Kết quả console:
[TOOL CALL] search_flights args={'origin': 'Hà Nội', 'destination': 'Phú Quốc'}
[TOOL CALL] search_hotels args={'city': 'Phú Quốc', 'max_price_per_night': 2500000}
[TOOL CALL] calculate_budget args={'total_budget': 5000000, 'expenses': 've_may_bay:1100000, khach_san:400000'}
[TOOL CALL] Không gọi tool (trả lời trực tiếp)
ASSISTANT:
Chuyến bay:
- Tuyến: Hà Nội -> Phú Quốc
- Phương án đề xuất: VietJet Air lúc 16:00 - 18:15
- Giá vé tham khảo: 1.100.000đ

Khách sạn:
- Thành phố: Phú Quốc
- Danh sách phù hợp ngân sách: 9Station Hostel, Sol by Melia, Lahana Resort

Tổng chi phí ước tính:
- Vé máy bay: 1.100.000đ
- Khách sạn: 400.000đ (2 đêm tại 9Station Hostel)
- Tổng chi: 1.500.000đ
- Còn lại so với ngân sách: 3.500.000đ

Đánh giá:
- Có gọi search_flights: [x]
- Có gọi search_hotels: [x]
- Có gọi calculate_budget: [x]
- Có tổng hợp thành gói tư vấn hoàn chỉnh: [x]

## Test 4 - Missing Info / Clarification
User:
Tôi muốn đặt khách sạn.

Kết quả console:
[TOOL CALL] Không gọi tool (trả lời trực tiếp)
ASSISTANT:
Bạn vui lòng cho tôi biết thành phố bạn muốn đặt khách sạn, số đêm lưu trú và ngân sách tối đa mỗi đêm là bao nhiêu?

Đánh giá:
- Agent hỏi lại thông tin còn thiếu (thành phố, số đêm, ngân sách): [x]
- Không gọi tool vội: [x]

## Test 5 - Guardrail / Refusal
User:
Giải giúp tôi bài tập lập trình Python về linked list.

Kết quả console:
[TOOL CALL] Không gọi tool (trả lời trực tiếp)
ASSISTANT:
Xin lỗi, nhưng tôi chỉ hỗ trợ các nhu cầu liên quan đến du lịch như chuyến bay, khách sạn và tính ngân sách chuyến đi. Nếu bạn có câu hỏi nào về du lịch, hãy cho tôi biết!

Đánh giá:
- Agent từ chối lịch sự: [x]
- Agent nhắc phạm vi chỉ hỗ trợ du lịch: [x]
