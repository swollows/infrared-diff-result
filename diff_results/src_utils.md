# src/utils 비교 결과

원본 경로: `/Users/jonathan/berachain-project/infrared-contracts/src/utils`

온체인 경로: `/Users/jonathan/berachain-project/infrared_/src/utils`

## 디렉토리 트리 구조

```
└── 📁 utils 
    ├── 📄 DataTypes.sol (수정됨)
    ├── 📄 Errors.sol (동일)
    ├── 📄 InfraredVaultDeployer.sol (동일)
    └── 📄 Upgradeable.sol (수정됨)
```

## 차이점

### 공통 파일 목록

다음 파일들은 양쪽 버전에 모두 존재합니다:

- 📄 `DataTypes.sol` (수정됨)
- 📄 `Errors.sol` (동일)
- 📄 `InfraredVaultDeployer.sol` (동일)
- 📄 `Upgradeable.sol` (수정됨)

### 파일 비교 통계

- 삭제된 파일: 0개
- 추가된 파일: 0개
- 수정된 파일: 2개
- 동일한 파일: 2개
- 총 파일 수: 4개

### 파일 내용 차이

```diff
diff --git asrc/utils (원본)/DataTypes.sol bsrc/utils (온체인)/DataTypes.sol
index c61f3a1..189f3ee 100644
--- asrc/utils (원본)/DataTypes.sol
+++ bsrc/utils (온체인)/DataTypes.sol
@@ -1,4 +1,4 @@
-// SPDX-License-Identifier: BUSL-1.1
+// SPDX-License-Identifier: MIT
 pragma solidity ^0.8.0;
 
 import {EnumerableSet} from
diff --git asrc/utils (원본)/Upgradeable.sol bsrc/utils (온체인)/Upgradeable.sol
index 84c7024..74fcb81 100644
--- asrc/utils (원본)/Upgradeable.sol
+++ bsrc/utils (온체인)/Upgradeable.sol
@@ -1,4 +1,4 @@
-// SPDX-License-Identifier: BUSL-1.1
+// SPDX-License-Identifier: MIT
 pragma solidity 0.8.26;
 
 import {AccessControlUpgradeable} from

```
