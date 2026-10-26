# dut-core-math-utils

[![CI Test Suite](https://github.com/Khoa35734/CatUIA/actions/workflows/ci.yml/badge.svg)](https://github.com/Khoa35734/CatUIA/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Thư viện toán học và đại số cơ bản dành cho sinh viên kỹ nghệ phần mềm DUT, phục vụ bài thực hành **Quản lý phụ thuộc, khóa phiên bản và robot điều phối tự động (Package Dependency Management)**.

## Mục lục

- [Tổng quan](#tổng-quan)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [Kiểm thử](#kiểm-thử)
- [Đóng gói Artifact](#đóng-gói-artifact)
- [Bảo vệ chuỗi cung ứng với Dependabot](#bảo-vệ-chuỗi-cung-ứng-với-dependabot)
- [Giấy phép](#giấy-phép)

---

## Tổng quan

Dự án minh họa các khái niệm cốt lõi trong kỹ nghệ phần mềm hiện đại:
1. **Manifest (`package.json`)**: Định danh gói phần mềm, khai báo phiên bản và phụ thuộc theo chuẩn Semantic Versioning (SemVer).
2. **Lockfile (`package-lock.json`)**: Đóng băng đồ thị phụ thuộc với mã băm toàn vẹn mật mã (`integrity sha512`) và liên kết nguồn (`resolved`), đảm bảo tính tái lập 100% với `npm ci`.
3. **Artifact Packaging (`npm pack`)**: Tạo gói phân phối chuẩn `.tgz` sạch sẽ, chỉ bao gồm các thành phần phân phối được định nghĩa qua `files`.
4. **Dry-run Publishing (`npm publish --dry-run`)**: Giả lập phát hành an toàn lên npm registry mà không đẩy mã lên kho công khai.
5. **Automated Supply-Chain Security (Dependabot)**: Robot tự động giám sát các phụ thuộc (`npm`, `github-actions`), phát hiện lỗ hổng đã biết (CVE/GHSA) và tạo Pull Request tự động vá lỗi kèm nhãn `security-patch`.

---

## Cài đặt

Cài đặt bằng npm:

```bash
npm install dut-core-math-utils
```

Để cài đặt môi trường phát triển với tính tái lập chuẩn xác từ Lockfile:

```bash
git clone https://github.com/Khoa35734/CatUIA.git
cd CatUIA
npm ci
```

---

## Sử dụng

```javascript
const { add } = require('dut-core-math-utils');

console.log(add(5, 7)); // Output: 12
console.log(add(-3, 8)); // Output: 5
```

---

## Kiểm thử

Chạy bộ kiểm thử tự động với Node.js:

```bash
npm test
```

---

## Đóng gói Artifact

Đóng gói thư viện thành tarball `.tgz`:

```bash
npm pack
```

Giả lập phát hành:

```bash
npm publish --dry-run
```

---

## Bảo vệ chuỗi cung ứng với Dependabot

Cấu hình tại `.github/dependabot.yml`:
- **Ecosystems**: `npm` (quét hàng tuần, tối đa 3 PRs đang mở, nhãn `security-patch`) và `github-actions` (quét hàng tháng).
- **Mục tiêu**: Tự động phát hiện và đề xuất cập nhật khi các gói phụ thuộc (như `lodash@4.17.15`) gặp lỗ hổng bảo mật.

---

## Giấy phép

Phát hành dưới giấy phép [MIT](LICENSE).
