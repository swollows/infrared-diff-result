# src/vendors 비교 결과

원본 경로: `/Users/jonathan/berachain-project/infrared-contracts/src/vendors`

온체인 경로: `/Users/jonathan/berachain-project/infrared_/src/vendors`

## 디렉토리 트리 구조

```
└── 📁 vendors 
    ├── 📄 CustomPausable.sol (동일)
    └── 📄 ERC20PresetMinterPauser.sol (수정됨)
```

## 차이점

### 공통 파일 목록

다음 파일들은 양쪽 버전에 모두 존재합니다:

- 📄 `CustomPausable.sol` (동일)
- 📄 `ERC20PresetMinterPauser.sol` (수정됨)

### 파일 비교 통계

- 삭제된 파일: 0개
- 추가된 파일: 0개
- 수정된 파일: 1개
- 동일한 파일: 1개
- 총 파일 수: 2개

### 파일 내용 차이

```diff
diff --git asrc/vendors (원본)/ERC20PresetMinterPauser.sol bsrc/vendors (온체인)/ERC20PresetMinterPauser.sol
index 73afb6f..840a993 100644
--- asrc/vendors (원본)/ERC20PresetMinterPauser.sol
+++ bsrc/vendors (온체인)/ERC20PresetMinterPauser.sol
@@ -1,4 +1,4 @@
-// SPDX-License-Identifier: BUSL-1.1
+// SPDX-License-Identifier: MIT
 // OpenZeppelin Contracts (last updated v4.5.0)
 // (token/ERC20/presets/ERC20PresetMinterPauser.sol)
 

```
