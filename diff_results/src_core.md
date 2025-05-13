# src/core 비교 결과

원본 경로: `/Users/jonathan/berachain-project/infrared-contracts/src/core`

온체인 경로: `/Users/jonathan/berachain-project/infrared_/src/core`

## 디렉토리 트리 구조

```
└── 📁 core 
    ├── 📄 InfraredDistributor.sol (추가됨)
    ├── 📄 InfraredBGT.sol (수정됨)
    ├── 📄 InfraredUpgradeable.sol (수정됨)
    ├── 📄 InfraredVault.sol (동일)
    ├── 📄 MultiRewards.sol (동일)
    ├── 📁 libraries 
    │   ├── 📄 ConfigTypes.sol (수정됨)
    │   ├── 📄 RewardsLib.sol (동일)
    │   ├── 📄 ValidatorManagerLib.sol (동일)
    │   ├── 📄 ValidatorTypes.sol (수정됨)
    │   └── 📄 VaultManagerLib.sol (동일)
    └── 📁 upgrades 
        ├── 📄 BribeCollectorV1_2.sol (추가됨)
        ├── 📄 InfraredV1_2.sol (동일)
        ├── 📄 InfraredV1_3.sol (동일)
        └── 📄 InfraredV1_4.sol (동일)
```

## 차이점

### 추가된 파일 목록

다음 파일들은 온체인 버전에만 존재하고 원본에는 없습니다:

- 📄 `InfraredDistributor.sol` (추가됨)

### 공통 파일 목록

다음 파일들은 양쪽 버전에 모두 존재합니다:

- 📄 `InfraredBGT.sol` (수정됨)
- 📄 `InfraredUpgradeable.sol` (수정됨)
- 📄 `InfraredVault.sol` (동일)
- 📄 `MultiRewards.sol` (동일)
- 📁 `libraries/`
- 📁 `upgrades/`

### 파일 비교 통계

- 삭제된 파일: 0개
- 추가된 파일: 1개
- 수정된 파일: 2개
- 동일한 파일: 2개
- 총 파일 수: 5개

- 📄 `upgrades/BribeCollectorV1_2.sol` (추가됨)

### 파일 내용 차이

```diff
diff --git asrc/core (원본)/InfraredBGT.sol bsrc/core (온체인)/InfraredBGT.sol
index 478f3bb..d52927c 100644
--- asrc/core (원본)/InfraredBGT.sol
+++ bsrc/core (온체인)/InfraredBGT.sol
@@ -1,4 +1,4 @@
-// SPDX-License-Identifier: BUSL-1.1
+// SPDX-License-Identifier: MIT
 pragma solidity 0.8.26;
 
 import {ERC20PresetMinterPauser} from "../vendors/ERC20PresetMinterPauser.sol";
diff --git asrc/core (온체인)/InfraredDistributor.sol bsrc/core (온체인)/InfraredDistributor.sol
new file mode 100644
index 0000000..b3f212c
--- /dev/null
+++ bsrc/core (온체인)/InfraredDistributor.sol
@@ -0,0 +1,183 @@
+// SPDX-License-Identifier: MIT
+pragma solidity 0.8.26;
+
+import {ERC20} from "@solmate/tokens/ERC20.sol";
+import {SafeTransferLib} from "@solmate/utils/SafeTransferLib.sol";
+import {InfraredUpgradeable} from "src/core/InfraredUpgradeable.sol";
+import {IInfrared} from "src/interfaces/IInfrared.sol";
+import {IInfraredDistributor} from "src/interfaces/IInfraredDistributor.sol";
+import {Errors} from "src/utils/Errors.sol";
+
+/// @title InfraredDistributor
+/// @dev Distributes rewards to validators.
+/// @dev Validator pubkeys are mapped to an EVM address and the pool of rewards from which they claim is porportional to the number of validators.
+/// - for example, if there are 10 validators and 100 tokens are notified, each validator can claim 10 tokens.
+contract InfraredDistributor is InfraredUpgradeable, IInfraredDistributor {
+    using SafeTransferLib for ERC20;
+
+    /// @inheritdoc IInfraredDistributor
+    ERC20 public token;
+
+    /// @inheritdoc IInfraredDistributor
+    uint256 public amountsCumulative;
+
+    uint256 private residualAmount;
+
+    mapping(bytes32 pubkeyHash => Snapshot) internal _snapshots;
+
+    mapping(bytes32 pubkeyHash => address) internal _validators;
+
+    /// Reserve storage slots for future upgrades for safety
+    uint256[40] private __gap;
+
+    function initialize(address _infrared, address _gov, address _token)
+        external
+        initializer
+    {
+        if (
+            _infrared == address(0) || _gov == address(0)
+                || _token == address(0)
+        ) {
+            revert Errors.ZeroAddress();
+        }
+
+        token = ERC20(_token);
+
+        // claim amounts calculated via differences so absolute amount not relevant
+        amountsCumulative++;
+
+        // grant admin access roles
+        _grantRole(DEFAULT_ADMIN_ROLE, _gov);
+        _grantRole(GOVERNANCE_ROLE, _gov);
+
+        // init upgradeable components
+        __InfraredUpgradeable_init(_infrared);
+    }
+
+    /// @inheritdoc IInfraredDistributor
+    function add(bytes calldata pubkey, address validator)
+        external
+        onlyInfrared
+    {
+        if (_validators[keccak256(pubkey)] != address(0)) {
+            revert Errors.ValidatorAlreadyExists();
+        }
+        _validators[keccak256(pubkey)] = validator;
+
+        Snapshot storage s = _snapshots[keccak256(pubkey)];
+        uint256 _amountsCumulative = amountsCumulative;
+
+        s.amountCumulativeLast = _amountsCumulative;
+        s.amountCumulativeFinal = 0;
+
+        emit Added(pubkey, validator, _amountsCumulative);
+    }
+
+    /// @inheritdoc IInfraredDistributor
+    function remove(bytes calldata pubkey) external onlyInfrared {
+        address validator = _validators[keccak256(pubkey)];
+        if (validator == address(0)) revert Errors.ValidatorDoesNotExist();
+
+        uint256 _amountsCumulative = amountsCumulative;
+        if (_amountsCumulative == 0) revert Errors.ZeroAmount();
+
+        Snapshot storage s = _snapshots[keccak256(pubkey)];
+        // Add check to prevent re-removal of already removed validators
+        if (s.amountCumulativeFinal != 0) {
+            revert Errors.ValidatorAlreadyRemoved();
+        }
+
+        s.amountCumulativeFinal = _amountsCumulative;
+
+        emit Removed(pubkey, validator, _amountsCumulative);
+    }
+
+    /// @inheritdoc IInfraredDistributor
+    function purge(bytes calldata pubkey) external onlyGovernor {
+        address validator = _validators[keccak256(pubkey)];
+        if (validator == address(0)) revert Errors.ValidatorDoesNotExist();
+
+        Snapshot memory s = _snapshots[keccak256(pubkey)];
+        if (s.amountCumulativeLast != s.amountCumulativeFinal) {
+            revert Errors.ClaimableRewardsExist();
+        }
+
+        delete _snapshots[keccak256(pubkey)];
+        delete _validators[keccak256(pubkey)];
+
+        emit Purged(pubkey, validator);
+    }
+
+    /// @inheritdoc IInfraredDistributor
+    function notifyRewardAmount(uint256 amount) external {
+        if (amount == 0) revert Errors.ZeroAmount();
+
+        uint256 num = infrared.numInfraredValidators();
+        if (num == 0) revert Errors.InvalidValidator();
+
+        unchecked {
+            uint256 sharePerValidator = amount / num;
+            uint256 residual = amount % num; // Calculate residual amount
+
+            // Accumulate the residual for future use
+            residualAmount += residual;
+
+            // If residual exceeds `num`, distribute it to validators
+            if (residualAmount >= num) {
+                uint256 extraShare = residualAmount / num;
+                sharePerValidator += extraShare;
+                residualAmount = residualAmount % num; // Update residual with leftover
+            }
+
+            amountsCumulative += sharePerValidator;
+        }
+        token.safeTransferFrom(msg.sender, address(this), amount);
+
+        emit Notified(amount, num);
+    }
+
+    /// @inheritdoc IInfraredDistributor
+    function claim(bytes calldata pubkey, address recipient) external {
+        address validator = _validators[keccak256(pubkey)];
+        if (validator != msg.sender) revert Errors.InvalidValidator();
+
+        Snapshot memory s = _snapshots[keccak256(pubkey)];
+
+        uint256 fin = s.amountCumulativeFinal == 0
+            ? amountsCumulative
+            : s.amountCumulativeFinal;
+
+        // Check if there are any unclaimed rewards
+        if (s.amountCumulativeLast == fin) revert Errors.NoRewardsToClaim();
+
+        uint256 amount;
+        unchecked {
+            amount = fin - s.amountCumulativeLast;
+        }
+
+        s.amountCumulativeLast = fin;
+        _snapshots[keccak256(pubkey)] = s;
+
+        if (amount > 0) token.safeTransfer(recipient, amount);
+        emit Claimed(pubkey, validator, recipient, amount);
+    }
+
+    /// @inheritdoc IInfraredDistributor
+    function getSnapshot(bytes calldata pubkey)
+        external
+        view
+        returns (uint256 amountCumulativeLast, uint256 amountCumulativeFinal)
+    {
+        Snapshot memory s = _snapshots[keccak256(pubkey)];
+        return (s.amountCumulativeLast, s.amountCumulativeFinal);
+    }
+
+    /// @inheritdoc IInfraredDistributor
+    function getValidator(bytes calldata pubkey)
+        external
+        view
+        returns (address)
+    {
+        return _validators[keccak256(pubkey)];
+    }
+}
diff --git asrc/core (원본)/InfraredUpgradeable.sol bsrc/core (온체인)/InfraredUpgradeable.sol
index d4259d2..7b4aea8 100644
--- asrc/core (원본)/InfraredUpgradeable.sol
+++ bsrc/core (온체인)/InfraredUpgradeable.sol
@@ -1,4 +1,4 @@
-// SPDX-License-Identifier: BUSL-1.1
+// SPDX-License-Identifier: MIT
 pragma solidity 0.8.26;
 
 import {Errors, Upgradeable} from "src/utils/Upgradeable.sol";
diff --git asrc/core (원본)/libraries/ConfigTypes.sol bsrc/core (온체인)/libraries/ConfigTypes.sol
index 259568f..50e2bc8 100644
--- asrc/core (원본)/libraries/ConfigTypes.sol
+++ bsrc/core (온체인)/libraries/ConfigTypes.sol
@@ -1,4 +1,4 @@
-// SPDX-License-Identifier: BUSL-1.1
+// SPDX-License-Identifier: MIT
 pragma solidity ^0.8.0;
 
 library ConfigTypes {
diff --git asrc/core (원본)/libraries/ValidatorTypes.sol bsrc/core (온체인)/libraries/ValidatorTypes.sol
index ac305b7..5ddd2ff 100644
--- asrc/core (원본)/libraries/ValidatorTypes.sol
+++ bsrc/core (온체인)/libraries/ValidatorTypes.sol
@@ -1,4 +1,4 @@
-// SPDX-License-Identifier: BUSL-1.1
+// SPDX-License-Identifier: MIT
 pragma solidity ^0.8.0;
 
 library ValidatorTypes {
diff --git asrc/core (온체인)/upgrades/BribeCollectorV1_2.sol bsrc/core (온체인)/upgrades/BribeCollectorV1_2.sol
new file mode 100644
index 0000000..8148373
--- /dev/null
+++ bsrc/core (온체인)/upgrades/BribeCollectorV1_2.sol
@@ -0,0 +1,112 @@
+// SPDX-License-Identifier: BUSL-1.1
+pragma solidity 0.8.26;
+
+import {ERC20} from "@solmate/tokens/ERC20.sol";
+import {SafeTransferLib} from "@solmate/utils/SafeTransferLib.sol";
+
+import {InfraredUpgradeable} from "src/core/InfraredUpgradeable.sol";
+import {Errors} from "src/utils/Errors.sol";
+
+import {IBribeCollector} from "src/interfaces/IBribeCollector.sol";
+
+/**
+ * @title BribeCollector v1.2
+ * @notice The Bribe Collector contract is responsible for collecting bribes from Berachain rewards vaults and
+ * auctioning them for a Payout token which then is distributed among Infrared validators.
+ * @dev This contract is forked from Berachain POL which is forked from Uniswap V3 Factory Owner contract.
+ * https://github.com/uniswapfoundation/UniStaker/blob/main/src/V3FactoryOwner.sol
+ */
+contract BribeCollectorV1_2 is InfraredUpgradeable, IBribeCollector {
+    using SafeTransferLib for ERC20;
+
+    /// @notice Payout token, required to be WBERA token as its unwrapped and used to compound rewards in the `iBera` system.
+    address public payoutToken;
+
+    /// @notice Payout amount is a constant value that is paid by the caller of the `claimFees` function.
+    uint256 public payoutAmount;
+
+    // Reserve storage slots for future upgrades for safety
+    uint256[40] private __gap;
+
+    /*´:°•.°+.*•´.*:˚.°*.˚•´.°:°•.°•.*•´.*:˚.°*.˚•´.°:°•.°+.*•´.*:*/
+    /*                       ADMIN FUNCTIONS                      */
+    /*.•°:°.´+˚.*°.˚:*.´•*.+°.•°:´*.´•*.•°.•°:°.´:•˚°.*°.˚:*.´+°.•*/
+
+    /// @notice Set the payout amount for the bribe collector.
+    /// @param _newPayoutAmount updated payout amount
+    function setPayoutAmount(uint256 _newPayoutAmount) external onlyGovernor {
+        if (_newPayoutAmount == 0) revert Errors.ZeroAmount();
+        emit PayoutAmountSet(payoutAmount, _newPayoutAmount);
+        payoutAmount = _newPayoutAmount;
+    }
+
+    /*´:°•.°+.*•´.*:˚.°*.˚•´.°:°•.°•.*•´.*:˚.°*.˚•´.°:°•.°+.*•´.*:*/
+    /*                       WRITE FUNCTIONS                      */
+    /*.•°:°.´+˚.*°.˚:*.´•*.+°.•°:´*.´•*.•°.•°:°.´:•˚°.*°.˚:*.´+°.•*/
+
+    /// @inheritdoc IBribeCollector
+    function claimFees(
+        address _recipient,
+        address[] calldata _feeTokens,
+        uint256[] calldata _feeAmounts
+    ) external {
+        if (_feeTokens.length != _feeAmounts.length) {
+            revert Errors.InvalidArrayLength();
+        }
+        if (_recipient == address(0)) revert Errors.ZeroAddress();
+
+        uint256 senderBalance = ERC20(payoutToken).balanceOf(msg.sender);
+        if (senderBalance < payoutAmount) {
+            revert Errors.InsufficientBalance();
+        }
+
+        // transfer price of claiming tokens (payoutAmount) from the sender to this contract
+        ERC20(payoutToken).safeTransferFrom(
+            msg.sender,
+            address(this),
+            payoutAmount
+        );
+        // set the allowance of the payout token to the infrared contract to be sent to
+        // validator distribution contract
+        ERC20(payoutToken).safeApprove(
+            address(infrared),
+            ERC20(payoutToken).balanceOf(address(this))
+        );
+        // Callback into infrared post auction to split amount to vaults and protocol
+        infrared.collectBribes(
+            payoutToken,
+            ERC20(payoutToken).balanceOf(address(this))
+        );
+        // payoutAmount will be transferred out at this point
+
+        // For all the specified fee tokens, transfer them to the recipient.
+        for (uint256 i; i < _feeTokens.length; i++) {
+            address feeToken = _feeTokens[i];
+            uint256 feeAmount = _feeAmounts[i];
+            if (feeToken == payoutToken) {
+                revert Errors.InvalidFeeToken();
+            }
+
+            if (!infrared.whitelistedRewardTokens(feeToken)) {
+                revert Errors.FeeTokenNotWhitelisted();
+            }
+
+            uint256 contractBalance = ERC20(feeToken).balanceOf(address(this));
+            if (feeAmount > contractBalance) {
+                revert Errors.InsufficientFeeTokenBalance();
+            }
+            ERC20(feeToken).safeTransfer(_recipient, feeAmount);
+            emit FeesClaimed(msg.sender, _recipient, feeToken, feeAmount);
+        }
+    }
+
+    function sweepPayoutToken() external {
+        uint256 balance = ERC20(payoutToken).balanceOf(address(this));
+        if (balance == 0) revert Errors.InsufficientBalance();
+        // set the allowance of the payout token to the infrared contract to be sent to
+        // validator distribution contract
+        ERC20(payoutToken).safeApprove(address(infrared), balance);
+        // Callback into infrared split amount to vaults and protocol
+        infrared.collectBribes(payoutToken, balance);
+    }
+}

```
