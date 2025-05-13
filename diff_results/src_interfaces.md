# src/interfaces 비교 결과

원본 경로: `/Users/jonathan/berachain-project/infrared-contracts/src/interfaces`

온체인 경로: `/Users/jonathan/berachain-project/infrared_/src/interfaces`

## 디렉토리 트리 구조

```
└── 📁 interfaces 
    ├── 📄 IInfraredBERAClaimor.sol (추가됨)
    ├── 📄 IInfraredBERADepositor.sol (추가됨)
    ├── 📄 IInfraredBERAFeeReceivor.sol (추가됨)
    ├── 📄 IInfraredBERAWithdrawor.sol (추가됨)
    ├── 📄 IBerachainBGT.sol (동일)
    ├── 📄 IBerachainBGTStaker.sol (동일)
    ├── 📄 IBribeCollector.sol (동일)
    ├── 📄 IERC20Mintable.sol (동일)
    ├── 📄 IInfrared.sol (동일)
    ├── 📄 IInfraredBERA.sol (동일)
    ├── 📄 IInfraredBGT.sol (동일)
    ├── 📄 IInfraredDistributor.sol (동일)
    ├── 📄 IInfraredGovernanceToken.sol (동일)
    ├── 📄 IInfraredUpgradeable.sol (동일)
    ├── 📄 IInfraredVault.sol (동일)
    ├── 📄 IMultiRewards.sol (동일)
    ├── 📄 IWBERA.sol (동일)
    └── 📁 upgrades 
        ├── 📄 IInfraredV1_2.sol (동일)
        ├── 📄 IInfraredV1_3.sol (동일)
        └── 📄 IInfraredV1_4.sol (동일)
```

## 차이점

### 추가된 파일 목록

다음 파일들은 온체인 버전에만 존재하고 원본에는 없습니다:

- 📄 `IInfraredBERAClaimor.sol` (추가됨)
- 📄 `IInfraredBERADepositor.sol` (추가됨)
- 📄 `IInfraredBERAFeeReceivor.sol` (추가됨)
- 📄 `IInfraredBERAWithdrawor.sol` (추가됨)

### 공통 파일 목록

다음 파일들은 양쪽 버전에 모두 존재합니다:

- 📄 `IBerachainBGT.sol` (동일)
- 📄 `IBerachainBGTStaker.sol` (동일)
- 📄 `IBribeCollector.sol` (동일)
- 📄 `IERC20Mintable.sol` (동일)
- 📄 `IInfrared.sol` (동일)
- 📄 `IInfraredBERA.sol` (동일)
- 📄 `IInfraredBGT.sol` (동일)
- 📄 `IInfraredDistributor.sol` (동일)
- 📄 `IInfraredGovernanceToken.sol` (동일)
- 📄 `IInfraredUpgradeable.sol` (동일)
- 📄 `IInfraredVault.sol` (동일)
- 📄 `IMultiRewards.sol` (동일)
- 📄 `IWBERA.sol` (동일)
- 📁 `upgrades/`

### 파일 비교 통계

- 삭제된 파일: 0개
- 추가된 파일: 4개
- 수정된 파일: 0개
- 동일한 파일: 13개
- 총 파일 수: 17개

### 파일 내용 차이

```diff
diff --git asrc/interfaces (온체인)/IInfraredBERAClaimor.sol bsrc/interfaces (온체인)/IInfraredBERAClaimor.sol
new file mode 100644
index 0000000..1b1aaca
--- /dev/null
+++ bsrc/interfaces (온체인)/IInfraredBERAClaimor.sol
@@ -0,0 +1,20 @@
+// SPDX-License-Identifier: MIT
+pragma solidity ^0.8.0;
+
+interface IInfraredBERAClaimor {
+    event Queue(address indexed receiver, uint256 amount, uint256 claim);
+    event Sweep(address indexed receiver, uint256 amount);
+
+    /// @notice Outstanding BERA claims for a receiver
+    /// @param receiver The address of the claims receiver
+    function claims(address receiver) external view returns (uint256);
+
+    /// @notice Queues a new BERA claim for a receiver
+    /// @dev Only callable by the InfraredBERAWithdrawor contract
+    /// @param receiver The address of the claims receiver
+    function queue(address receiver) external payable;
+
+    /// @notice Sweeps oustanding BERA claims for a receiver to their address
+    /// @param receiver The address of the claims receiver
+    function sweep(address receiver) external;
+}
diff --git asrc/interfaces (온체인)/IInfraredBERADepositor.sol bsrc/interfaces (온체인)/IInfraredBERADepositor.sol
new file mode 100644
index 0000000..63497d4
--- /dev/null
+++ bsrc/interfaces (온체인)/IInfraredBERADepositor.sol
@@ -0,0 +1,48 @@
+// SPDX-License-Identifier: MIT
+pragma solidity ^0.8.0;
+
+interface IInfraredBERADepositor {
+    /// @notice Emitted when BERA is queued for deposit
+    /// @param amount The amount of BERA queued
+    event Queue(uint256 amount);
+
+    /// @notice Emitted when a deposit is executed to the deposit contract
+    /// @param pubkey The validator's public key
+    /// @param amount The amount of BERA deposited
+    event Execute(bytes pubkey, uint256 amount);
+
+    /// @notice the main InfraredBERA contract address
+    function InfraredBERA() external view returns (address);
+
+    /// @notice the queued amount of BERA to be deposited
+    function reserves() external view returns (uint256);
+
+    /// @notice Queues a deposit by sending BERA to this contract and storing the amount
+    /// in the pending deposits acculimator
+    function queue() external payable;
+
+    /// @notice Executes a deposit to the deposit contract for the specified pubkey and amount
+    /// @param pubkey The pubkey of the validator to deposit for
+    /// @param amount The amount of BERA to deposit
+    /// @dev Only callable by the keeper
+    /// @dev Only callable if the deposits are enabled
+    function execute(bytes calldata pubkey, uint256 amount) external;
+
+    /// @notice Initialize the contract (replaces the constructor)
+    /// @param _gov Address for admin / gov to upgrade
+    /// @param _keeper Address for keeper
+    /// @param ibera The initial IBERA address
+    /// @param _depositContract The ETH2 (Berachain) Deposit Contract Address
+    function initialize(
+        address _gov,
+        address _keeper,
+        address ibera,
+        address _depositContract
+    ) external;
+
+    /// @notice The Deposit Contract Address for Berachain
+    function DEPOSIT_CONTRACT() external view returns (address);
+
+    /// @notice https://eth2book.info/capella/part2/deposits-withdrawals/withdrawal-processing/
+    function ETH1_ADDRESS_WITHDRAWAL_PREFIX() external view returns (uint8);
+}
diff --git asrc/interfaces (온체인)/IInfraredBERAFeeReceivor.sol bsrc/interfaces (온체인)/IInfraredBERAFeeReceivor.sol
new file mode 100644
index 0000000..2446c8c
--- /dev/null
+++ bsrc/interfaces (온체인)/IInfraredBERAFeeReceivor.sol
@@ -0,0 +1,59 @@
+// SPDX-License-Identifier: MIT
+pragma solidity ^0.8.0;
+
+import {IInfrared} from "./IInfrared.sol";
+
+interface IInfraredBERAFeeReceivor {
+    /// @notice Emitted when accumulated rewards are swept to InfraredBERA
+    /// @param receiver The address receiving the swept BERA
+    /// @param amount The amount of BERA swept
+    /// @param fees The amount of fees taken
+    event Sweep(address indexed receiver, uint256 amount, uint256 fees);
+
+    /// @notice Emitted when shareholder fees are collected
+    /// @param receiver The address receiving the collected fees
+    /// @param amount The amount of fees collected
+    /// @param sharesMinted The amount of iBERA shares minted
+    event Collect(
+        address indexed receiver, uint256 amount, uint256 sharesMinted
+    );
+
+    /// @notice The address of the `InfraredBERA.sol` contract
+    function InfraredBERA() external view returns (address);
+
+    /// @notice The `Infrared.sol` contract address
+    function infrared() external view returns (IInfrared);
+
+    /// @notice Accumulated protocol fees in contract to be claimed
+    function shareholderFees() external view returns (uint256);
+
+    /// @notice Amount of BERA swept to InfraredBERA and fees taken for protool on next call to sweep
+    /// @return amount The amount of BERA forwarded to InfraredBERA on next sweep
+    /// @return fees The protocol fees taken on next sweep
+    function distribution()
+        external
+        view
+        returns (uint256 amount, uint256 fees);
+
+    /// @notice Sweeps accumulated coinbase priority fees + MEV to InfraredBERA to autocompound principal
+    /// @return amount The amount of BERA forwarded to InfraredBERA
+    /// @return fees The total fees taken
+    function sweep() external returns (uint256 amount, uint256 fees);
+
+    /// @notice Collects accumulated shareholder fees
+    /// @dev Reverts if msg.sender is not `InfraredBera.sol` contract
+    /// @return sharesMinted The amount of iBERA shares minted and sent to the `Infrared.sol`
+    function collect() external returns (uint256 sharesMinted);
+
+    /// @notice Initializer function (replaces constructor)
+    /// @param _gov Address for admin / gov to upgrade
+    /// @param _keeper Address for keeper
+    /// @param ibera Address for InfraredBERA
+    /// @param _infrared Address for Infrared
+    function initialize(
+        address _gov,
+        address _keeper,
+        address ibera,
+        address _infrared
+    ) external;
+}
diff --git asrc/interfaces (온체인)/IInfraredBERAWithdrawor.sol bsrc/interfaces (온체인)/IInfraredBERAWithdrawor.sol
new file mode 100644
index 0000000..303d4d2
--- /dev/null
+++ bsrc/interfaces (온체인)/IInfraredBERAWithdrawor.sol
@@ -0,0 +1,94 @@
+// SPDX-License-Identifier: MIT
+pragma solidity ^0.8.0;
+
+interface IInfraredBERAWithdrawor {
+    /// @notice Emitted when a withdrawal is queued
+    /// @param receiver The address that will receive the withdrawn BERA
+    /// @param nonce The unique identifier for this withdrawal request
+    /// @param amount The amount of BERA to be withdrawn
+    event Queue(address indexed receiver, uint256 nonce, uint256 amount);
+
+    /// @notice Emitted when a withdrawal is executed
+    /// @param pubkey The validator's public key
+    /// @param start The starting nonce
+    /// @param end The ending nonce
+    /// @param amount The amount of BERA withdrawn
+    event Execute(bytes pubkey, uint256 start, uint256 end, uint256 amount);
+
+    /// @notice Emitted when a withdrawal is processed
+    /// @param receiver The address receiving the withdrawn BERA
+    /// @param nonce The nonce of the processed withdrawal
+    /// @param amount The amount of BERA processed
+    event Process(address indexed receiver, uint256 nonce, uint256 amount);
+
+    /// @notice Emitted when funds are swept from a force-exited validator
+    /// @param receiver The address receiving the swept BERA
+    /// @param amount The amount of BERA swept
+    event Sweep(address indexed receiver, uint256 amount);
+
+    /// @notice The address of the InfraredBERA contract
+    function InfraredBERA() external view returns (address);
+
+    /// @notice Sweeps forced withdrawals to InfraredBERA to re-stake principal
+    /// @param pubkey The validator's public key to sweep funds from
+    /// @dev Only callable when withdrawals are disabled and by keeper
+    function sweep(bytes calldata pubkey) external;
+
+    /// @notice Outstanding requests for claims on previously burnt ibera
+    /// @param nonce The nonce associated with the claim
+    /// @return receiver The address of the receiver of bera funds to be claimed
+    /// @return timestamp The block.timestamp at which withdraw request was issued
+    /// @return fee The fee escrow amount set aside for withdraw precompile request
+    /// @return amountSubmit The amount of bera left to be submitted for withdraw request
+    /// @return amountProcess The amount of bera left to be processed for withdraw request
+    function requests(uint256 nonce)
+        external
+        view
+        returns (
+            address receiver,
+            uint96 timestamp,
+            uint256 fee,
+            uint256 amountSubmit,
+            uint256 amountProcess
+        );
+
+    /// @notice Amount of BERA internally set aside for withdraw precompile request fees
+    function fees() external view returns (uint256);
+
+    /// @notice Amount of BERA internally set aside to process withdraw compile requests from funds received on successful requests
+    function reserves() external view returns (uint256);
+
+    /// @notice Amount of BERA internally rebalancing amongst Infrared validators
+    function rebalancing() external view returns (uint256);
+
+    /// @notice The next nonce to issue withdraw request for
+    function nonceRequest() external view returns (uint256);
+
+    /// @notice The next nonce to submit withdraw request for
+    function nonceSubmit() external view returns (uint256);
+
+    /// @notice The next nonce in queue to process claims for
+    function nonceProcess() external view returns (uint256);
+
+    /// @notice Queues a withdraw request from InfraredBERA
+    /// @param receiver The address to receive withdrawn funds
+    /// @param amount The amount of funds to withdraw
+    /// @return nonce The unique identifier for this withdrawal request
+    /// @dev Requires msg.value to cover minimum withdrawal fee
+    function queue(address receiver, uint256 amount)
+        external
+        payable
+        returns (uint256 nonce);
+
+    /// @notice Executes a withdraw request to withdraw precompile
+    /// @param pubkey The validator's public key to withdraw from
+    /// @param amount The amount of BERA to withdraw
+    /// @dev Payable to cover any additional fees required by precompile
+    /// @dev Only callable by keeper
+    function execute(bytes calldata pubkey, uint256 amount) external payable;
+
+    /// @notice Processes the funds received from withdraw precompile
+    /// @dev Reverts if balance has not increased by full amount of request
+    /// @dev Processes requests in FIFO order based on nonce
+    function process() external;
+}

```
