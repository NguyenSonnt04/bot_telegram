# Quy ước phát triển

## Nhánh chính

`main` là nhánh chính và phải luôn ở trạng thái ổn định.

Không triển khai feature trực tiếp trên `main`. Mỗi feature mới phải bắt đầu từ
`main` sạch và được thực hiện trên một nhánh riêng.

## Quy ước đặt tên nhánh

Tên nhánh dùng chữ thường, không dấu và nối từ bằng dấu gạch ngang:

```text
feature/<ten-feature>
fix/<ten-loi>
refactor/<pham-vi>
docs/<noi-dung>
chore/<cong-viec>
```

Ví dụ:

```text
feature/tenant-foundation
feature/sepay-payment
feature/telegram-product-menu
fix/duplicate-payment-webhook
docs/payment-runbook
```

## Bắt đầu một feature

Trước khi tạo nhánh:

1. Xác nhận đang ở `main`.
2. Xác nhận working tree sạch.
3. Cập nhật `main` từ remote khi repository đã có remote.
4. Tạo nhánh `feature/<ten-feature>` từ `main`.

```powershell
git switch main
git status
git switch -c feature/<ten-feature>
```

Không chuyển nhánh hoặc khôi phục file nếu thao tác đó có thể ghi đè thay đổi
chưa commit của người dùng.

## Hoàn thành một feature

Trước khi merge:

1. Chạy các kiểm tra liên quan.
2. Cập nhật tài liệu nếu hành vi hoặc kiến trúc thay đổi.
3. Xác nhận không có secret hoặc file local trong commit.
4. Review toàn bộ diff của nhánh.
5. Merge feature về `main` thông qua pull request khi repository đã có remote.

Không push, merge, rebase lịch sử đã công bố hoặc mở pull request nếu người dùng
chưa yêu cầu hành động đó.
