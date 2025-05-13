# src/staking 비교 결과

원본 경로: `/Users/jonathan/berachain-project/infrared-contracts/src/staking`

온체인 경로: `/Users/jonathan/berachain-project/infrared_/src/staking`

## 디렉토리 트리 구조

```
└── 📁 staking 
    ├── 📄 InfraredBERA.sol (추가됨)
    ├── 📄 InfraredBERAClaimor.sol (추가됨)
    ├── 📄 InfraredBERAConstants.sol (추가됨)
    ├── 📄 InfraredBERADepositor.sol (추가됨)
    ├── 📄 InfraredBERAFeeReceivor.sol (추가됨)
    ├── 📄 InfraredBERAWithdrawor.sol (추가됨)
    └── 📄 InfraredBERAWithdraworLite.sol (추가됨)
```

## 차이점

### 추가된 파일 목록

다음 파일들은 온체인 버전에만 존재하고 원본에는 없습니다:

- 📄 `InfraredBERA.sol` (추가됨)
- 📄 `InfraredBERAClaimor.sol` (추가됨)
- 📄 `InfraredBERAConstants.sol` (추가됨)
- 📄 `InfraredBERADepositor.sol` (추가됨)
- 📄 `InfraredBERAFeeReceivor.sol` (추가됨)
- 📄 `InfraredBERAWithdrawor.sol` (추가됨)
- 📄 `InfraredBERAWithdraworLite.sol` (추가됨)

### 파일 내용 차이

```diff
diff --git asrc/staking (온체인)/InfraredBERA.sol bsrc/staking (온체인)/InfraredBERA.sol
new file mode 100644
index 0000000..d437fc2
--- /dev/null
+++ bsrc/staking (온체인)/InfraredBERA.sol
@@ -0,0 +1,478 @@
+// SPDX-License-Identifier: MIT
+pragma solidity 0.8.26;
+
+import {ERC20Upgradeable} from
+    "@openzeppelin/contracts-upgradeable/token/ERC20/ERC20Upgradeable.sol";
+import {Errors, Upgradeable} from "src/utils/Upgradeable.sol";
+import {IInfrared} from "src/interfaces/IInfrared.sol";
+import {IInfraredBERADepositor} from "src/interfaces/IInfraredBERADepositor.sol";
+import {IInfraredBERAWithdrawor} from
+    "src/interfaces/IInfraredBERAWithdrawor.sol";
+import {IInfraredBERAFeeReceivor} from
+    "src/interfaces/IInfraredBERAFeeReceivor.sol";
+import {IInfraredBERA} from "src/interfaces/IInfraredBERA.sol";
+import {InfraredBERAConstants} from "./InfraredBERAConstants.sol";
+import {InfraredBERADepositor} from "./InfraredBERADepositor.sol";
+import {InfraredBERAWithdrawor} from "./InfraredBERAWithdrawor.sol";
+import {InfraredBERAClaimor} from "./InfraredBERAClaimor.sol";
+import {InfraredBERAFeeReceivor} from "./InfraredBERAFeeReceivor.sol";
+
+/*
+
+    Made with Love by the Bears at Infrared Finance, so that all Bears may
+         get the best yields on their BERA. For the Bears, by the Bears. <3
+
+
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡤⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⣠⠴⠶⢤⡞⢡⡚⣦⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⢰⣃⠀⠀⠈⠁⠀⠉⠁⢺⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠈⢯⣄⡀⠀⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠦⠤⣤⣤⠞⠀⠀⢀⣴⠒⢦⣴⣖⢲⡀⠀⠀⠀⠀⣠⣴⠾⠿⠷⣶⣄⠀⣀⣠⣤⣴⣶⣶⣶⣦⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠈⠳⠼⣰⠃⠀⠀⠀⣼⡟⠁⠀⣀⣀⠀⠙⢿⠟⠋⠉⠀⠀⠀⠀⠀⠀⠉⠉⠛⠿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⣦⣄⣠⣶⣿⣛⠛⠿⣾⣿⠀⢠⣾⠋⣹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣷⣄⡀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣴⡶⠿⠟⠛⠛⠛⠛⠛⠛⠿⢷⣾⣿⣷⡀⠻⠾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⣄⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⢷⣦⡀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⣶⣶⣤⡀⠀⠀⠀⠀⢀⣤⡶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣆⠙⣿⡄
+⠀⠀⠀⠀⠀⠀⠀⣠⣾⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣷⡀⠀⢷⡄⠸⣯⣀⣼⡷⠒⢉⣉⡙⢢⡀⠀⠀⠀⠀⠀⢸⣿⡀⢸⣿
+⠀⠀⠀⠀⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⢄⡾⠐⠒⢆⠀⠀⣿⡇⠀⢸⡇⠀⠈⢉⡟⠀⠀⠀⢹⡟⠃⢧⣴⠶⢶⡄⠀⠀⣿⣇⣼⡟
+⠀⠀⣠⣴⡶⠶⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⢃⡾⠁⠀⠀⢸⠃⠀⣿⡇⠀⣸⡇⠀⠀⣼⠀⠀⠀⢠⡾⠁⠀⢸⣿⣤⣼⠗⠀⠀⣿⣿⠛⠀
+⢀⣾⠟⠁⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⠀⢿⠇⡼⠁⠀⠀⢀⡜⠀⢀⣿⠃⠀⠉⠀⠀⠀⢧⠀⠠⡶⣿⠁⠀⢠⠇⠀⠉⠁⠀⠀⠀⣿⡏⠀⠀
+⢸⣿⠀⢠⡞⠉⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠾⢿⣠⣷⡄⠀⠁⠳⠤⠖⠋⠀⠀⣸⡟⠀⠀⠀⠀⠀⠀⠘⣄⡀⠀⠛⢀⡴⠋⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀
+⢸⣿⡀⠈⠻⣦⣼⠀⠀⠀⠀⠀⠀⠀⢀⣤⣴⡶⠶⠆⠀⢠⣤⡾⠋⠀⣿⠀⠀⠀⠀⠀⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⡅⠀⠀
+⠀⠻⣿⣦⣄⣀⣰⡀⠀⠀⠀⠀⠀⠀⣸⠯⢄⡀⠀⠀⠀⢸⣇⠀⠀⠀⣸⡇⠀⠀⠀⠀⠀⢠⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠃⠀⠀
+⠀⠀⠀⠉⠙⠛⣿⣇⠀⠀⠀⠀⢀⠎⠀⠀⠀⠈⣆⠀⠀⠀⠻⣦⣄⣴⠟⠀⠀⠀⠀⠀⣰⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡄⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⡿⠋⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠸⣿⣆⠀⠀⠀⠘⡄⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠉⠀⠀⢀⣀⣤⣴⣾⣿⣧⣄⠀⢀⣠⣴⣶⣶⣶⣤⡶⠋⠉⠀⠀⢀⣀⣀⣠⣤⣶⣾⠿⠋⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠘⢿⣦⡀⠀⠀⠈⠒⠤⠔⠋⠀⠀⠀⠀⠀⠀⣠⣴⡾⠟⠋⠉⠀⠀⠀⠛⣹⣷⣿⠟⠒⠀⠀⠀⠉⢻⣷⣶⣾⠿⠿⠿⠛⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⢿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣹⣿⣿⣄⣀⠀⠀⠀⠀⢀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠿⣷⣶⣶⣤⣤⣶⡦⠀⠁⠀⠀⠀⠀⠀⣀⣀⣀⣤⣴⡾⠟⠁⠙⠿⣷⣶⣤⣴⣾⠿⠛⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⣽⡿⠁⠀⣤⣤⣶⡶⠾⠿⠟⢻⠛⠉⠁⠀⠀⠀⠀⠀⠀⠈⠉⠙⣿⡆⠀⠈⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠟⠁⠀⢸⣟⡁⠀⠀⠀⠀⣰⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠈⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⣿⡏⠀⠀⠀⠸⣿⣤⣶⣀⣤⣾⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣧⣄⣀⣤⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣇⣿⡇⠀⠀⠀⠀⣾⣿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣍⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⣿⡇⠀⠀⠀⠀⠉⣿⣆⠀⠀⠀⠀⠀⠀⠀⢴⣶⣶⠆⠀⠀⠀⠀⠀⠀⣈⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⠀⠀⠀⠀⠀⠀⣸⣿⡄⠀⠀⠀⠀⠀⠀⢸⣟⢿⣿⣦⠀⠀⢠⣄⣠⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣥⣤⣶⣀⣠⣶⣴⡿⢻⣷⣄⣴⣆⣀⣆⣠⣿⡇⠈⠻⣿⣵⣶⡿⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
+*/
+
+/// @title InfraredBERA
+/// @notice Infrared BERA is a liquid staking token for Berachain
+/// @dev This is the main "Front-End" contract for the whole BERA staking system.
+contract InfraredBERA is ERC20Upgradeable, Upgradeable, IInfraredBERA {
+    /*´:°•.°+.*•´.*:˚.°*.˚•´.°:°•.°•.*•´.*:˚.°*.˚•´.°:°•.°+.*•´.*:*/
+    /*                       STORAGE                              */
+    /*.•°:°.´+˚.*°.˚:*.´•*.+°.•°:´*.´•*.•°.•°:°.´:•˚°.*°.˚:*.´+°.•*/
+
+    /// @notice Withdrawals are not enabled by default, not supported by https://github.com/berachain/beacon-kit yet.
+    bool public withdrawalsEnabled;
+
+    /// @notice Whether the contract has been initialized
+    bool private _initialized;
+
+    /// @notice The fee divisor for protocol + operator + voter fees. 1/N, where N is the divisor. example 100 = 1/100 = 1%
+    uint16 public feeDivisorShareholders;
+
+    /// @notice The `Infrared.sol` smart contract.
+    address public infrared;
+
+    /// @notice The `InfraredBERADepositor.sol` smart contract.
+    address public depositor;
+
+    /// @notice The `InfraredBERAWithdrawor.sol` smart contract.
+    address public withdrawor;
+
+    /// @notice The `InfraredBERAFeeReceivor.sol` smart contract.
+    address public receivor;
+
+    /// @notice The total amount of `BERA` deposited by the system.
+    uint256 public deposits;
+
+    /// @notice Mapping of validator pubkeyHash to their stake in `BERA`.
+    mapping(bytes32 pubkeyHash => uint256 stake) internal _stakes;
+
+    /// @notice Mapping of validator pubkeyHash to whether they have recieved stake from this contract.
+    mapping(bytes32 pubkeyHash => bool isStaked) internal _staked;
+
+    /// @notice Mapping of validator pubkeyHash to whether they have exited from this contract. (voluntarily or force).
+    mapping(bytes32 pubkeyHash => bool hasExited) internal _exited;
+
+    /// @notice Mapping of validator pubkeyHash to their deposit signature. All validators MUST have their signiture amounts set to `INITIAL_DEPOSIT` to be valid.
+    mapping(bytes32 pubkeyHash => bytes) internal _signatures;
+
+    /// @dev Reserve storage slots for future upgrades for safety
+    uint256[40] private __gap;
+
+    /*´:°•.°+.*•´.*:˚.°*.˚•´.°:°•.°•.*•´.*:˚.°*.˚•´.°:°•.°+.*•´.*:*/
+    /*                       INITIALIZATION                       */
+    /*.•°:°.´+˚.*°.˚:*.´•*.+°.•°:´*.´•*.•°.•°:°.´:•˚°.*°.˚:*.´+°.•*/
+
+    /// @notice Initiializer for `InfraredBERA`.
+    /// @param _gov The address of the governance contract.
+    /// @param _keeper The address of the keeper contract.
+    /// @param _infrared The address of the `Infrared.sol` contract.
+    /// @param _depositor The address of the `InfraredBERADepositor.sol` contract.
+    /// @param _withdrawor The address of the `InfraredBERAWithdrawor.sol` contract.
+    /// @param _receivor The address of the `InfraredBERAFeeReceivor.sol` contract.
+    function initialize(
+        address _gov,
+        address _keeper,
+        address _infrared,
+        address _depositor,
+        address _withdrawor,
+        address _receivor
+    ) external payable initializer {
+        if (
+            _gov == address(0) || _infrared == address(0)
+                || _depositor == address(0) || _withdrawor == address(0)
+                || _receivor == address(0)
+        ) revert Errors.ZeroAddress();
+        __ERC20_init("Infrared BERA", "iBERA");
+        __Upgradeable_init();
+
+        infrared = _infrared;
+        depositor = _depositor;
+        withdrawor = _withdrawor;
+        receivor = _receivor;
+
+        _grantRole(DEFAULT_ADMIN_ROLE, _gov);
+        _grantRole(GOVERNANCE_ROLE, _gov);
+        _grantRole(KEEPER_ROLE, _keeper);
+
+        // mint minimum amount to mitigate inflation attack with shares
+        _initialized = true;
+        mint(address(this));
+    }
+
+    /*´:°•.°+.*•´.*:˚.°*.˚•´.°:°•.°•.*•´.*:˚.°*.˚•´.°:°•.°+.*•´.*:*/
+    /*                       AUTH                                 */
+    /*.•°:°.´+˚.*°.˚:*.´•*.+°.•°:´*.´•*.•°.•°:°.´:•˚°.*°.˚:*.´+°.•*/
+
+    /// @notice Checks if account has the governance role.
+    /// @param account The address to check.
+    /// @return True if the account has the governance role.
+    function governor(address account) public view returns (bool) {
+        return hasRole(GOVERNANCE_ROLE, account);
+    }
+
+    /// @notice Checks if account has the keeper role.
+    /// @param account The address to check.
+    /// @return True if the account has the keeper role.
+    function keeper(address account) public view returns (bool) {
+        return hasRole(KEEPER_ROLE, account);
+    }
+
+    /// @notice Checks if a given pubkey is a validator in the `Infrared` contract.
+    /// @param pubkey The pubkey to check.
+    /// @return True if the pubkey is a validator.
+    function validator(bytes calldata pubkey) external view returns (bool) {
+        return IInfrared(infrared).isInfraredValidator(pubkey);
+    }
+
+    /*´:°•.°+.*•´.*:˚.°*.˚•´.°:°•.°•.*•´.*:˚.°*.˚•´.°:°•.°+.*•´.*:*/
+    /*                       ADMIN                                */
+    /*.•°:°.´+˚.*°.˚:*.´•*.+°.•°:´*.´•*.•°.•°:°.´:•˚°.*°.˚:*.´+°.•*/
+
+    /// @notice Allows withdrawals to be enabled or disabled.
+    /// @param flag The flag to set for withdrawals.
+    /// @dev Only callable by the governor.
+    function setWithdrawalsEnabled(bool flag) external onlyGovernor {
+        withdrawalsEnabled = flag;
+        emit WithdrawalFlagSet(flag);
+    }
+
+    /// @notice Sets the fee shareholders taken on yield from EL coinbase priority fees + MEV
+    /// @param to The new fee shareholders represented as an integer denominator (1/x)%
+    function setFeeDivisorShareholders(uint16 to) external onlyGovernor {
+        compound();
+        emit SetFeeShareholders(feeDivisorShareholders, to);
+        feeDivisorShareholders = to;
+    }
+
+    /// @notice Sets the deposit signature for a given pubkey. Ensure that the pubkey has signed the correct deposit amount of `INITIAL_DEPOSIT`.
+    /// @param pubkey The pubkey to set the deposit signature for.
+    /// @param signature The signature to set for the pubkey.
+    /// @dev Only callable by the governor.
+    function setDepositSignature(
+        bytes calldata pubkey,
+        bytes calldata signature
+    ) external onlyGovernor {
+        if (signature.length != 96) revert Errors.InvalidSignature();
+        emit SetDepositSignature(
+            pubkey, _signatures[keccak256(pubkey)], signature
+        );
+        _signatures[keccak256(pubkey)] = signature;
+    }
+
+    /*´:°•.°+.*•´.*:˚.°*.˚•´.°:°•.°•.*•´.*:˚.°*.˚•´.°:°•.°+.*•´.*:*/
+    /*                       MINT/BURN                            */
+    /*.•°:°.´+˚.*°.˚:*.´•*.+°.•°:´*.´•*.•°.•°:°.´:•˚°.*°.˚:*.´+°.•*/
+
+    /// @notice Mints `ibera` to the `receiver` in exchange for `bera`.
+    /// @dev takes in msg.value as amount to mint `ibera` with.
+    /// @param receiver The address to mint `ibera` to.
+    /// @return shares The amount of `ibera` minted.
+    function mint(address receiver) public payable returns (uint256 shares) {
+        // @dev make sure to compound yield earned from EL rewards first to avoid accounting errors.
+        compound();
+
+        // cache prior since updated in _deposit call
+        uint256 d = deposits;
+        uint256 ts = totalSupply();
+
+        // deposit bera request
+        uint256 amount = msg.value;
+        _deposit(amount);
+
+        // mint shares to receiver of ibera, if there are no deposits or total supply, mint full amount
+        // else mint amount based on total supply and deposits: (totalSupply * amount) / deposits
+        shares = (d != 0 && ts != 0) ? (ts * amount) / d : amount;
+        if (shares == 0) revert Errors.InvalidShares();
+        _mint(receiver, shares);
+
+        emit Mint(receiver, amount, shares);
+    }
+
+    /// @notice Burns `ibera` from the `msg.sender` and sets a receiver to get the `BERA` in exchange for `iBERA`.
+    /// @param receiver The address to send the `BERA` to.
+    /// @param shares The amount of `ibera` to burn.
+    /// @return nonce The nonce of the withdrawal. Queue based system for withdrawals.
+    /// @return amount The amount of `BERA` withdrawn for the exchange of `iBERA`.
+    function burn(address receiver, uint256 shares)
+        external
+        payable
+        returns (uint256 nonce, uint256 amount)
+    {
+        if (!withdrawalsEnabled) revert Errors.WithdrawalsNotEnabled();
+        // @dev make sure to compound yield earned from EL rewards first to avoid accounting errors.
+        compound();
+
+        uint256 ts = totalSupply();
+        if (shares == 0 || ts == 0) revert Errors.InvalidShares();
+
+        amount = (deposits * shares) / ts;
+        if (amount == 0) revert Errors.InvalidAmount();
+
+        // burn shares from sender of ibera
+        _burn(msg.sender, shares);
+
+        // withdraw bera request
+        // @dev pay withdraw precompile fee via funds sent in on payable call
+        uint256 fee = msg.value;
+        if (fee < InfraredBERAConstants.MINIMUM_WITHDRAW_FEE) {
+            revert Errors.InvalidFee();
+        }
+        nonce = _withdraw(receiver, amount, fee);
+
+        emit Burn(receiver, nonce, amount, shares, fee);
+    }
+
+    /// @notice Internal function to update top level accounting and minimum deposit.
+    /// @param amount The amount of `BERA` to deposit.
+    function _deposit(uint256 amount) internal {
+        // @dev check at internal deposit level to prevent donations prior
+        if (!_initialized) revert Errors.NotInitialized();
+
+        // update tracked deposits with validators
+        deposits += amount;
+        // escrow funds to depositor contract to eventually forward to precompile
+        IInfraredBERADepositor(depositor).queue{value: amount}();
+    }
+
+    /// @notice Internal function to update top level accounting.
+    /// @param receiver The address to withdraw `BERA` to.
+    /// @param amount The amount of `BERA` to withdraw.
+    /// @param fee The fee to pay for the withdrawal.
+    function _withdraw(address receiver, uint256 amount, uint256 fee)
+        private
+        returns (uint256 nonce)
+    {
+        if (!_initialized) revert Errors.NotInitialized();
+
+        // request to withdrawor contract to eventually forward to precompile
+        nonce = IInfraredBERAWithdrawor(withdrawor).queue{value: fee}(
+            receiver, amount
+        );
+        // update tracked deposits with validators *after* queue given used by withdrawor via confirmed
+        deposits -= amount;
+    }
+
+    /*´:°•.°+.*•´.*:˚.°*.˚•´.°:°•.°•.*•´.*:˚.°*.˚•´.°:°•.°+.*•´.*:*/
+    /*                       ACCOUNTING                           */
+    /*.•°:°.´+˚.*°.˚:*.´•*.+°.•°:´*.´•*.•°.•°:°.´:•˚°.*°.˚:*.´+°.•*/
+
+    /// @notice Previews the amount of InfraredBERA shares that would be minted for a given BERA amount
+    /// @param beraAmount The amount of BERA to simulate depositing
+    /// @return shares The amount of InfraredBERA shares that would be minted, returns 0 if the operation would fail
+    function previewMint(uint256 beraAmount)
+        public
+        view
+        returns (uint256 shares)
+    {
+        if (!_initialized) {
+            return 0;
+        }
+
+        // First simulate compound effects like in actual mint
+        (uint256 compoundAmount,) =
+            IInfraredBERAFeeReceivor(receivor).distribution();
+
+        // Calculate shares considering both:
+        // 1. The compound effect (compoundAmount - fee)
+        // 2. The new deposit (beraAmount - fee)
+        uint256 ts = totalSupply();
+        uint256 depositsAfterCompound = deposits;
+
+        // First simulate compound effect on deposits
+        if (compoundAmount > 0) {
+            depositsAfterCompound += (compoundAmount);
+        }
+
+        // Then calculate shares based on user deposit
+        uint256 amount = beraAmount;
+        if (depositsAfterCompound == 0 || ts == 0) {
+            shares = amount;
+        } else {
+            shares = (ts * amount) / depositsAfterCompound;
+        }
+    }
+
+    /// @notice Previews the amount of BERA that would be received for burning InfraredBERA shares
+    /// @param shareAmount The amount of InfraredBERA shares to simulate burning
+    /// @return beraAmount The amount of BERA that would be received, returns 0 if the operation would fail
+    /// @return fee The fee that would be charged for the burn operation
+    function previewBurn(uint256 shareAmount)
+        public
+        view
+        returns (uint256 beraAmount, uint256 fee)
+    {
+        if (!_initialized || shareAmount == 0) {
+            return (0, 0);
+        }
+
+        // First simulate compound effects like in actual burn
+        (uint256 compoundAmount,) =
+            IInfraredBERAFeeReceivor(receivor).distribution();
+
+        uint256 ts = totalSupply();
+        if (ts == 0) {
+            return (0, InfraredBERAConstants.MINIMUM_WITHDRAW_FEE);
+        }
+
+        // Calculate amount considering compound effect
+        uint256 depositsAfterCompound = deposits;
+
+        if (compoundAmount > 0) {
+            depositsAfterCompound += (compoundAmount);
+        }
+
+        beraAmount = (depositsAfterCompound * shareAmount) / ts;
+        fee = InfraredBERAConstants.MINIMUM_WITHDRAW_FEE;
+
+        if (beraAmount == 0) {
+            return (0, fee);
+        }
+    }
+
+    /// @notice Returns the amount of BERA staked in validator with given pubkey
+    /// @return The amount of BERA staked in validator
+    function stakes(bytes calldata pubkey) external view returns (uint256) {
+        return _stakes[keccak256(pubkey)];
+    }
+
+    /// @notice Returns whether initial deposit has been staked to validator with given pubkey
+    /// @return Whethere initial deposit has been staked to validator
+    function staked(bytes calldata pubkey) external view returns (bool) {
+        return _staked[keccak256(pubkey)];
+    }
+
+    /// @notice Pending deposits yet to be forwarded to CL
+    /// @return The amount of BERA yet to be deposited to CL
+    function pending() public view returns (uint256) {
+        return (
+            IInfraredBERADepositor(depositor).reserves()
+                + IInfraredBERAWithdrawor(withdrawor).rebalancing()
+        );
+    }
+
+    /// @notice Confirmed deposits sent to CL, total - future deposits
+    /// @return The amount of BERA confirmed to be deposited to CL
+    function confirmed() external view returns (uint256) {
+        uint256 _pending = pending();
+        // If pending is greater than deposits, return 0 instead of underflowing
+        return _pending > deposits ? 0 : deposits - _pending;
+    }
+
+    /// @inheritdoc IInfraredBERA
+    function compound() public {
+        IInfraredBERAFeeReceivor(receivor).sweep();
+    }
+
+    /// @notice Compounds accumulated EL yield in fee receivor into deposits
+    /// @dev Called internally at bof whenever InfraredBERA minted or burned
+    /// @dev Only sweeps if amount transferred from fee receivor would exceed min deposit thresholds
+    function sweep() external payable {
+        if (msg.sender != receivor) {
+            revert Errors.Unauthorized(msg.sender);
+        }
+        _deposit(msg.value);
+        emit Sweep(msg.value);
+    }
+
+    /// @notice Collects yield from fee receivor and mints ibera shares to Infrared
+    /// @dev Called in `RewardsLib::harvestOperatorRewards()` in `Infrared.sol`
+    /// @dev Only Infrared can call this function
+    /// @return sharesMinted The amount of ibera shares
+    function collect() external returns (uint256 sharesMinted) {
+        if (msg.sender != address(infrared)) {
+            revert Errors.Unauthorized(msg.sender);
+        }
+        sharesMinted = IInfraredBERAFeeReceivor(receivor).collect();
+    }
+
+    /*´:°•.°+.*•´.*:˚.°*.˚•´.°:°•.°•.*•´.*:˚.°*.˚•´.°:°•.°+.*•´.*:*/
+    /*                       VALIDATORS                           */
+    /*.•°:°.´+˚.*°.˚:*.´•*.+°.•°:´*.´•*.•°.•°:°.´:•˚°.*°.˚:*.´+°.•*/
+
+    /// @notice Updates the accounted for stake of a validator pubkey.
+    /// @notice This does NOT mean its the balance on the CL, edge case is if another user has staked to the pubkey.
+    /// @param pubkey The pubkey of the validator.
+    /// @param delta The change in stake.
+    function register(bytes calldata pubkey, int256 delta) external {
+        if (msg.sender != depositor && msg.sender != withdrawor) {
+            revert Errors.Unauthorized(msg.sender);
+        }
+        if (_exited[keccak256(pubkey)]) {
+            revert Errors.ValidatorForceExited();
+        }
+        // update validator pubkey stake for delta
+        uint256 stake = _stakes[keccak256(pubkey)];
+        if (delta > 0) stake += uint256(delta);
+        else stake -= uint256(-delta);
+        _stakes[keccak256(pubkey)] = stake;
+        // update whether have staked to validator before
+        if (delta > 0 && !_staked[keccak256(pubkey)]) {
+            _staked[keccak256(pubkey)] = true;
+        }
+        // only 0 if validator was force exited
+        if (stake == 0) {
+            _staked[keccak256(pubkey)] = false;
+            _exited[keccak256(pubkey)] = true;
+        }
+
+        emit Register(pubkey, delta, stake);
+    }
+
+    /// @notice Returns whether a validator pubkey has exited.
+    function hasExited(bytes calldata pubkey) external view returns (bool) {
+        return _exited[keccak256(pubkey)];
+    }
+
+    /// @notice Returns the deposit signature to use for given pubkey
+    /// @return The deposit signature for pubkey
+    function signatures(bytes calldata pubkey)
+        external
+        view
+        returns (bytes memory)
+    {
+        return _signatures[keccak256(pubkey)];
+    }
+}
diff --git asrc/staking (온체인)/InfraredBERAClaimor.sol bsrc/staking (온체인)/InfraredBERAClaimor.sol
new file mode 100644
index 0000000..b81de13
--- /dev/null
+++ bsrc/staking (온체인)/InfraredBERAClaimor.sol
@@ -0,0 +1,57 @@
+// SPDX-License-Identifier: MIT
+pragma solidity 0.8.26;
+
+import {SafeTransferLib} from "@solmate/utils/SafeTransferLib.sol";
+import {Upgradeable} from "src/utils/Upgradeable.sol";
+import {IInfraredBERAClaimor} from "src/interfaces/IInfraredBERAClaimor.sol";
+import {IInfraredBERA} from "src/interfaces/IInfraredBERA.sol";
+import {Errors} from "src/utils/Errors.sol";
+
+/// @title InfraredBERAClaimor
+/// @notice Claimor to claim BERA withdrawn from CL for Infrared liquid staking token
+/// @dev Separate contract so withdrawor process has trusted contract to forward funds to so no issue with naked bera transfer and receive function
+contract InfraredBERAClaimor is Upgradeable, IInfraredBERAClaimor {
+    /// @inheritdoc IInfraredBERAClaimor
+    mapping(address => uint256) public claims;
+
+    IInfraredBERA public ibera;
+
+    /// Reserve storage slots for future upgrades for safety
+    uint256[40] private __gap;
+
+    /// @notice Initializer function (replaces constructor)
+    /// @param _gov Address of the initial admin / gov
+    /// @param _keeper Address of the initial keeper
+    /// @param _ibera Address of InfraredBera proxy contract
+    function initialize(address _gov, address _keeper, address _ibera)
+        external
+        initializer
+    {
+        ibera = IInfraredBERA(_ibera);
+        __Upgradeable_init();
+        _grantRole(DEFAULT_ADMIN_ROLE, _gov);
+        _grantRole(GOVERNANCE_ROLE, _gov);
+        _grantRole(KEEPER_ROLE, _keeper);
+    }
+
+    /// @inheritdoc IInfraredBERAClaimor
+    function queue(address receiver) external payable {
+        // Only allow the withdrawor contract to queue claims
+        if (msg.sender != ibera.withdrawor()) {
+            revert Errors.Unauthorized(msg.sender);
+        }
+
+        uint256 claim = claims[receiver];
+        claim += msg.value;
+        claims[receiver] = claim;
+        emit Queue(receiver, msg.value, claim);
+    }
+
+    /// @inheritdoc IInfraredBERAClaimor
+    function sweep(address receiver) external {
+        uint256 amount = claims[receiver];
+        delete claims[receiver];
+        if (amount > 0) SafeTransferLib.safeTransferETH(receiver, amount);
+        emit Sweep(receiver, amount);
+    }
+}
diff --git asrc/staking (온체인)/InfraredBERAConstants.sol bsrc/staking (온체인)/InfraredBERAConstants.sol
new file mode 100644
index 0000000..480e464
--- /dev/null
+++ bsrc/staking (온체인)/InfraredBERAConstants.sol
@@ -0,0 +1,9 @@
+// SPDX-License-Identifier: MIT
+pragma solidity ^0.8.0;
+
+library InfraredBERAConstants {
+    uint256 public constant INITIAL_DEPOSIT = 10000 ether;
+    uint256 public constant MINIMUM_WITHDRAW_FEE = 1 ether;
+    uint256 public constant FORCED_MIN_DELAY = 7 days;
+    uint256 public constant MAX_EFFECTIVE_BALANCE = 10_000_000 ether;
+}
diff --git asrc/staking (온체인)/InfraredBERADepositor.sol bsrc/staking (온체인)/InfraredBERADepositor.sol
new file mode 100644
index 0000000..9073718
--- /dev/null
+++ bsrc/staking (온체인)/InfraredBERADepositor.sol
@@ -0,0 +1,159 @@
+// SPDX-License-Identifier: MIT
+pragma solidity 0.8.26;
+
+import {SafeTransferLib} from "@solmate/utils/SafeTransferLib.sol";
+import {IBeaconDeposit} from "@berachain/pol/interfaces/IBeaconDeposit.sol";
+import {Errors, Upgradeable} from "src/utils/Upgradeable.sol";
+import {IInfraredBERA} from "src/interfaces/IInfraredBERA.sol";
+import {IInfraredBERADepositor} from "src/interfaces/IInfraredBERADepositor.sol";
+import {InfraredBERAConstants} from "./InfraredBERAConstants.sol";
+
+/// @title InfraredBERADepositor
+/// @notice Depositor to deposit BERA to CL for Infrared liquid staking token
+contract InfraredBERADepositor is Upgradeable {
+    /// @notice https://eth2book.info/capella/part2/deposits-withdrawals/withdrawal-processing/
+    uint8 public constant ETH1_ADDRESS_WITHDRAWAL_PREFIX = 0x01;
+    /// @notice The Deposit Contract Address for Berachain
+    address public DEPOSIT_CONTRACT;
+    /// @notice the main InfraredBERA contract address
+    address public InfraredBERA;
+    /// @notice the queued amount of BERA to be deposited
+    uint256 public reserves;
+
+    event Queue(uint256 amount);
+    event Execute(bytes pubkey, uint256 amount);
+
+    /// Reserve storage slots for future upgrades for safety
+    uint256[40] private __gap;
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
+    ) public initializer {
+        if (
+            _gov == address(0) || _keeper == address(0) || ibera == address(0)
+                || _depositContract == address(0)
+        ) revert Errors.ZeroAddress();
+        __Upgradeable_init();
+        _grantRole(DEFAULT_ADMIN_ROLE, _gov);
+        _grantRole(GOVERNANCE_ROLE, _gov);
+        _grantRole(KEEPER_ROLE, _keeper);
+
+        InfraredBERA = ibera;
+        DEPOSIT_CONTRACT = _depositContract;
+    }
+
+    /// @notice Queues a deposit by sending BERA to this contract and storing the amount
+    /// in the pending deposits acculimator
+    function queue() external payable {
+        /// @dev can only be called by InfraredBERA for adding to the reserves and by withdrawor for rebalancing
+        /// when validators get kicked out of the set, TODO: link the set kickout code.
+        if (
+            msg.sender != InfraredBERA
+                && msg.sender != IInfraredBERA(InfraredBERA).withdrawor()
+        ) {
+            revert Errors.Unauthorized(msg.sender);
+        }
+
+        // @dev accumulate the amount of BERA to be deposited with `execute`
+        reserves += msg.value;
+
+        emit Queue(msg.value);
+    }
+
+    /// @notice Executes a deposit to the deposit contract for the specified pubkey and amount.
+    /// @param pubkey The pubkey of the validator to deposit for
+    /// @param amount The amount of BERA to deposit
+    /// @dev Only callable by the keeper
+    /// @dev Only callable if the deposits are enabled
+    function execute(bytes calldata pubkey, uint256 amount)
+        external
+        onlyKeeper
+    {
+        // check if pubkey is a valid validator being tracked by InfraredBERA
+        if (!IInfraredBERA(InfraredBERA).validator(pubkey)) {
+            revert Errors.InvalidValidator();
+        }
+
+        // The amount must be a multiple of 1 gwei as per the deposit contract, cannot be more eth than we have, and must be at least the minimum deposit amount.
+        if (amount == 0 || (amount % 1 gwei) != 0 || amount > reserves) {
+            revert Errors.InvalidAmount();
+        }
+
+        // cache the withdrawor address since we will be using it multiple times.
+        address withdrawor = IInfraredBERA(InfraredBERA).withdrawor();
+
+        // Check if there is any forced exits on the withdrawor contract.
+        // @notice if the balance of the withdrawor is more than INITIAL_DEPOSIT, we can assume that there is an unprocessed forced exit and
+        // we should sweep it before we can deposit the BERA. This stops the protocol from staking into exited validators.
+        if (withdrawor.balance >= InfraredBERAConstants.INITIAL_DEPOSIT) {
+            revert Errors.HandleForceExitsBeforeDeposits();
+        }
+
+        // The validator balance + amount must not surpase MaxEffectiveBalance of 10 million BERA.
+        if (
+            IInfraredBERA(InfraredBERA).stakes(pubkey) + amount
+                > InfraredBERAConstants.MAX_EFFECTIVE_BALANCE
+        ) {
+            revert Errors.ExceedsMaxEffectiveBalance();
+        }
+
+        // @dev determin what to set the operator, if the operator is not set we know this is the first deposit and we should set it to infrared.
+        // if not we know this is the second or subsequent deposit (subject to internal test below) and we should set the operator to address(0).
+        address operatorBeacon =
+            IBeaconDeposit(DEPOSIT_CONTRACT).getOperator(pubkey);
+        address operator = IInfraredBERA(InfraredBERA).infrared();
+        // check if first beacon deposit by checking if the registered operator is set
+        if (operatorBeacon != address(0)) {
+            // Not first deposit. Ensure the correct operator is set for subsequent deposits
+            if (operatorBeacon != operator) {
+                revert Errors.UnauthorizedOperator();
+            }
+            // check whether first deposit via internal logic to protect against bypass beacon deposit attack
+            if (!IInfraredBERA(InfraredBERA).staked(pubkey)) {
+                revert Errors.OperatorAlreadySet();
+            }
+            // A nuance of berachain is that subsequent deposits set operator to address(0)
+            operator = address(0);
+        } else {
+            /// First deposit, overwrite the amount to the initial deposit amount.
+            amount = InfraredBERAConstants.INITIAL_DEPOSIT;
+        }
+
+        // @notice load the signature for the pubkey. This is only used for the first deposit but can be re-used safley since this is checked only on the first deposit.
+        // https://github.com/berachain/beacon-kit/blob/395085d18667e48395503a20cd1b367309fe3d11/state-transition/core/state_processor_staking.go#L101
+        bytes memory signature = IInfraredBERA(InfraredBERA).signatures(pubkey);
+        if (signature.length == 0) {
+            revert Errors.InvalidSignature();
+        }
+
+        // @notice ethereum/consensus-specs/blob/dev/specs/phase0/validator.md#eth1_address_withdrawal_prefix
+        // @dev similar to the signiture above, this is only used for the first deposit but can be re-used safley since this is checked only on the first deposit.
+        bytes memory credentials = abi.encodePacked(
+            ETH1_ADDRESS_WITHDRAWAL_PREFIX,
+            uint88(0), // 11 zero bytes
+            withdrawor
+        );
+
+        /// @dev reduce the reserves by the amount deposited.
+        reserves -= amount;
+
+        /// @dev register the increase in stake to the validator.
+        IInfraredBERA(InfraredBERA).register(pubkey, int256(amount));
+
+        // @dev deposit the BERA to the deposit contract.
+        // @dev the amount being divided by 1 gwei is checked inside.
+        IBeaconDeposit(DEPOSIT_CONTRACT).deposit{value: amount}(
+            pubkey, credentials, signature, operator
+        );
+
+        emit Execute(pubkey, amount);
+    }
+}
diff --git asrc/staking (온체인)/InfraredBERAFeeReceivor.sol bsrc/staking (온체인)/InfraredBERAFeeReceivor.sol
new file mode 100644
index 0000000..012d740
--- /dev/null
+++ bsrc/staking (온체인)/InfraredBERAFeeReceivor.sol
@@ -0,0 +1,102 @@
+// SPDX-License-Identifier: MIT
+pragma solidity 0.8.26;
+
+import {SafeTransferLib} from "@solmate/utils/SafeTransferLib.sol";
+import {Errors, Upgradeable} from "src/utils/Upgradeable.sol";
+import {IInfraredBERA} from "src/interfaces/IInfraredBERA.sol";
+import {IInfraredBERAFeeReceivor} from
+    "src/interfaces/IInfraredBERAFeeReceivor.sol";
+import {IInfrared} from "src/interfaces/IInfrared.sol";
+import {InfraredBERAConstants} from "./InfraredBERAConstants.sol";
+
+/// @title InfraredBERAFeeReceivor
+/// @notice Receivor for fees from InfraredBERA from tips and share of the proof-of-liquidity incentive system.
+/// @dev Validators need to set this address as their coinbase(fee_recepient on most clients).
+contract InfraredBERAFeeReceivor is Upgradeable, IInfraredBERAFeeReceivor {
+    /// @notice The address of the `InfraredBERA.sol` contract.
+    address public InfraredBERA;
+
+    /// @notice The `Infrared.sol` contract address.
+    IInfrared public infrared;
+
+    /// @notice Accumulated protocol fees in contract to be claimed.
+    uint256 public shareholderFees;
+
+    /// @notice Reserve storage slots for future upgrades for safety
+    uint256[40] private __gap;
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
+    ) external initializer {
+        if (
+            _gov == address(0) || _keeper == address(0) || ibera == address(0)
+                || _infrared == address(0)
+        ) revert Errors.ZeroAddress();
+        __Upgradeable_init();
+
+        InfraredBERA = ibera;
+        infrared = IInfrared(_infrared);
+
+        _grantRole(DEFAULT_ADMIN_ROLE, _gov);
+        _grantRole(GOVERNANCE_ROLE, _gov);
+        _grantRole(KEEPER_ROLE, _keeper);
+    }
+
+    /// @notice Amount of BERA swept to InfraredBERA and fees taken for protool on next call to sweep
+    /// @return amount THe amount of BERA forwarded to InfraredBERA on next sweep.
+    /// @return fees The protocol fees taken on next sweep.
+    function distribution()
+        public
+        view
+        returns (uint256 amount, uint256 fees)
+    {
+        amount = (address(this).balance - shareholderFees);
+        uint16 feeShareholders =
+            IInfraredBERA(InfraredBERA).feeDivisorShareholders();
+
+        // take protocol fees
+        if (feeShareholders > 0) {
+            fees = amount / uint256(feeShareholders);
+            amount -= fees;
+        }
+    }
+
+    /// @notice Sweeps accumulated coinbase priority fees + MEV to InfraredBERA to autocompound principal
+    /// @return amount The amount of BERA forwarded to InfraredBERA.
+    /// @return fees The total fees taken.
+    function sweep() external returns (uint256 amount, uint256 fees) {
+        (amount, fees) = distribution();
+
+        // add to protocol fees and sweep amount back to ibera to deposit
+        if (fees > 0) shareholderFees += fees;
+        IInfraredBERA(InfraredBERA).sweep{value: amount}();
+        emit Sweep(InfraredBERA, amount, fees);
+    }
+
+    /// @notice Collects accumulated shareholder fees
+    /// @dev Reverts if msg.sender is not `InfraredBera.sol` contract
+    /// @return sharesMinted The amount of iBERA shares minted and sent to the `Infrared.sol`
+    function collect() external returns (uint256 sharesMinted) {
+        if (msg.sender != InfraredBERA) revert Errors.Unauthorized(msg.sender);
+        uint256 _shareholderFees = shareholderFees;
+        if (_shareholderFees == 0) return 0;
+
+        delete shareholderFees;
+        sharesMinted = IInfraredBERA(InfraredBERA).mint{value: _shareholderFees}(
+            address(infrared)
+        );
+
+        emit Collect(address(infrared), _shareholderFees, sharesMinted);
+    }
+
+    /// @notice Fallback function to receive BERA
+    receive() external payable {}
+}
diff --git asrc/staking (온체인)/InfraredBERAWithdrawor.sol bsrc/staking (온체인)/InfraredBERAWithdrawor.sol
new file mode 100644
index 0000000..4fd3e9c
--- /dev/null
+++ bsrc/staking (온체인)/InfraredBERAWithdrawor.sol
@@ -0,0 +1,272 @@
+// SPDX-License-Identifier: MIT
+pragma solidity 0.8.26;
+
+import {SafeTransferLib} from "@solmate/utils/SafeTransferLib.sol";
+import {Errors, Upgradeable} from "src/utils/Upgradeable.sol";
+import {IInfraredBERA} from "src/interfaces/IInfraredBERA.sol";
+import {IInfraredBERADepositor} from "src/interfaces/IInfraredBERADepositor.sol";
+import {IInfraredBERAClaimor} from "src/interfaces/IInfraredBERAClaimor.sol";
+import {IInfraredBERAWithdrawor} from
+    "src/interfaces/IInfraredBERAWithdrawor.sol";
+import {InfraredBERAConstants} from "./InfraredBERAConstants.sol";
+
+/// @title InfraredBERAWithdrawor
+/// @notice Withdrawor to withdraw BERA from CL for Infrared liquid staking token
+/// @dev Assumes ETH returned via withdraw precompile credited to contract so receive unnecessary
+contract InfraredBERAWithdrawor is Upgradeable, IInfraredBERAWithdrawor {
+    uint8 public constant WITHDRAW_REQUEST_TYPE = 0x01;
+    address public WITHDRAW_PRECOMPILE; // @dev: EIP7002
+
+    /// @inheritdoc IInfraredBERAWithdrawor
+    address public InfraredBERA;
+
+    address public claimor;
+
+    struct Request {
+        /// receiver of withdrawn bera funds
+        address receiver;
+        /// block.timestamp at which withdraw request issued
+        uint96 timestamp;
+        /// fee escrow for withdraw precompile request
+        uint256 fee;
+        /// amount of withdrawn bera funds left to submit request to withdraw precompile
+        uint256 amountSubmit;
+        /// amount of withdrawn bera funds left to process from funds received via withdraw request
+        uint256 amountProcess;
+    }
+
+    /// @inheritdoc IInfraredBERAWithdrawor
+    mapping(uint256 => Request) public requests;
+
+    /// @inheritdoc IInfraredBERAWithdrawor
+    uint256 public fees;
+
+    /// @inheritdoc IInfraredBERAWithdrawor
+    uint256 public rebalancing;
+
+    /// @inheritdoc IInfraredBERAWithdrawor
+    uint256 public nonceRequest;
+    /// @inheritdoc IInfraredBERAWithdrawor
+    uint256 public nonceSubmit;
+    /// @inheritdoc IInfraredBERAWithdrawor
+    uint256 public nonceProcess;
+
+    /// Reserve storage slots for future upgrades for safety
+    uint256[40] private __gap;
+
+    function initializeV2(address _claimor, address _withdraw_precompile)
+        external
+        onlyGovernor
+    {
+        if (_claimor == address(0) || _withdraw_precompile == address(0)) {
+            revert Errors.ZeroAddress();
+        }
+        WITHDRAW_PRECOMPILE = _withdraw_precompile;
+        claimor = _claimor;
+    }
+
+    /// @notice Checks whether enough time has passed beyond min delay
+    /// @param then The block timestamp in past
+    /// @param current The current block timestamp now
+    /// @return has Whether time between then and now exceeds forced min delay
+    function _enoughtime(uint96 then, uint96 current)
+        private
+        pure
+        returns (bool has)
+    {
+        unchecked {
+            has = (current - then) >= InfraredBERAConstants.FORCED_MIN_DELAY;
+        }
+    }
+
+    /// @inheritdoc IInfraredBERAWithdrawor
+    function reserves() public view returns (uint256) {
+        return address(this).balance - fees;
+    }
+
+    /// @inheritdoc IInfraredBERAWithdrawor
+    function queue(address receiver, uint256 amount)
+        external
+        payable
+        returns (uint256 nonce)
+    {
+        bool kpr = IInfraredBERA(InfraredBERA).keeper(msg.sender);
+        address depositor = IInfraredBERA(InfraredBERA).depositor();
+        // @dev rebalances can be queued by keeper but receiver must be depositor and amount must exceed deposit fee
+        if (msg.sender != InfraredBERA && !kpr) {
+            revert Errors.Unauthorized(msg.sender);
+        }
+        if ((kpr && receiver != depositor) || (!kpr && receiver == depositor)) {
+            revert Errors.InvalidReceiver();
+        }
+        if (
+            (receiver != depositor && amount == 0)
+                || amount > IInfraredBERA(InfraredBERA).confirmed()
+        ) {
+            revert Errors.InvalidAmount();
+        }
+
+        if (msg.value < InfraredBERAConstants.MINIMUM_WITHDRAW_FEE) {
+            revert Errors.InvalidFee();
+        }
+        fees += msg.value;
+
+        // account for rebalancing amount
+        // @dev must update *after* InfraredBERA.confirmed checked given used in confirmed view
+        if (kpr) rebalancing += amount;
+
+        nonce = nonceRequest++;
+        requests[nonce] = Request({
+            receiver: receiver,
+            timestamp: uint96(block.timestamp),
+            fee: msg.value,
+            amountSubmit: amount,
+            amountProcess: amount
+        });
+        emit Queue(receiver, nonce, amount);
+    }
+
+    /// @inheritdoc IInfraredBERAWithdrawor
+    function execute(bytes calldata pubkey, uint256 amount) external payable {
+        bool kpr = IInfraredBERA(InfraredBERA).keeper(msg.sender);
+        // no need to check if in *current* validator set as revert before precompile call if have no stake in pubkey
+        // allows for possibly removing stake from validators that were previously removed from validator set on Infrared
+        // TODO: check whether precompile ultimately modified for amount / 1 gwei to be consistent with deposits
+        if (
+            amount == 0 || IInfraredBERA(InfraredBERA).stakes(pubkey) < amount
+                || (amount % 1 gwei) != 0 || (amount / 1 gwei) > type(uint64).max
+        ) {
+            revert Errors.InvalidAmount();
+        }
+
+        // cache for event after the bundling while loop
+        uint256 _nonce = nonceSubmit; // start
+        uint256 nonce; // end (inclusive)
+        uint256 fee;
+
+        // bundle nonces to meet up to amount
+        // @dev care should be taken with choice of amount parameter not to reach gas limit
+        uint256 remaining = amount;
+        while (remaining > 0) {
+            nonce = nonceSubmit;
+            Request memory r = requests[nonce];
+            if (r.amountSubmit == 0) revert Errors.InvalidAmount();
+
+            // @dev allow user to force withdraw from infrared validator if enough time has passed
+            // TODO: check signature not needed (ignored) on second deposit to pubkey (think so)
+            if (!kpr && !_enoughtime(r.timestamp, uint96(block.timestamp))) {
+                revert Errors.Unauthorized(msg.sender);
+            }
+
+            // first time loop ever hits request dedicate fee to this call
+            // @dev for large request requiring multiple separate calls to execute, keeper must front fee in subsequent calls
+            // @dev but should make up for fronting via protocol fees on size
+            if (r.fee > 0) {
+                fee += r.fee;
+                r.fee = 0;
+            }
+
+            // either use all of request amount and increment nonce if remaining > request amount or use remaining
+            // not fully filling request in this call
+            uint256 delta =
+                remaining > r.amountSubmit ? r.amountSubmit : remaining;
+            r.amountSubmit -= delta;
+            if (r.amountSubmit == 0) nonceSubmit++;
+            requests[nonce] = r;
+
+            // always >= 0 due to delta ternary
+            remaining -= delta;
+        }
+
+        // remove accumulated escrowed fee from each request in bundled withdraws and refund excess to keeper
+        fees -= fee;
+        // couple with additional msg.value from keeper in case withdraw precompile fee is large or has been used in prior call that did not fully fill
+        fee += msg.value;
+        // cache balance prior to withdraw compile to calculate refund on fee
+        uint256 _balance = address(this).balance;
+
+        // prepare RLP encoded data (for simplicity, using abi.encodePacked for concatenation)
+        // @dev must ensure no matter what withdraw call guaranteed to happen
+        bytes memory encoded = abi.encodePacked(
+            WITHDRAW_REQUEST_TYPE, // 0x01
+            msg.sender, // source_address
+            pubkey, // validator_pubkey
+            uint64(amount / 1 gwei) // amount in gwei
+        );
+        (bool success,) = WITHDRAW_PRECOMPILE.call{value: fee}(encoded);
+        if (!success) revert Errors.CallFailed();
+
+        // calculate excess from withdraw precompile call to refund
+        // TODO: test excess value passed over fee actually refunded
+        uint256 excess = fee - (_balance - address(this).balance);
+
+        // register update to stake
+        IInfraredBERA(InfraredBERA).register(pubkey, -int256(amount)); // safe as max fits in uint96
+
+        // sweep excess fee back to keeper to cover gas
+        if (excess > 0) SafeTransferLib.safeTransferETH(msg.sender, excess);
+
+        emit Execute(pubkey, _nonce, nonce, amount);
+    }
+
+    /// @inheritdoc IInfraredBERAWithdrawor
+    function process() external {
+        uint256 nonce = nonceProcess;
+        address depositor = IInfraredBERA(InfraredBERA).depositor();
+        Request memory r = requests[nonce];
+        if (r.amountSubmit != 0 || r.amountProcess == 0) {
+            revert Errors.InvalidAmount();
+        }
+
+        uint256 amount = r.amountProcess;
+        if (amount > reserves()) revert Errors.InvalidReserves();
+        r.amountProcess -= amount;
+        nonceProcess++;
+        requests[nonce] = r;
+
+        if (r.receiver == depositor) {
+            // queue up rebalance to depositor
+            rebalancing -= amount;
+            IInfraredBERADepositor(r.receiver).queue{value: amount}();
+        } else {
+            // queue up receiver claim to claimor
+            IInfraredBERAClaimor(claimor).queue{value: amount}(r.receiver);
+        }
+        emit Process(r.receiver, nonce, amount);
+    }
+
+    /// @inheritdoc IInfraredBERAWithdrawor
+    function sweep(bytes calldata pubkey) external {
+        // Check withdrawals disabled
+        if (IInfraredBERA(InfraredBERA).withdrawalsEnabled()) {
+            revert Errors.Unauthorized(msg.sender);
+        }
+        // Check keeper authorization
+        if (!IInfraredBERA(InfraredBERA).keeper(msg.sender)) {
+            revert Errors.Unauthorized(msg.sender);
+        }
+        // Check if validator has already exited - do this before checking stake
+        if (IInfraredBERA(InfraredBERA).hasExited(pubkey)) {
+            revert Errors.ValidatorForceExited();
+        }
+        // forced exit always withdraw entire stake of validator
+        uint256 amount = IInfraredBERA(InfraredBERA).stakes(pubkey);
+
+        // revert if insufficient balance
+        if (amount > reserves()) revert Errors.InvalidAmount();
+
+        // todo: verfiy forced withdrawal against beacon roots
+
+        // register new validator delta
+        IInfraredBERA(InfraredBERA).register(pubkey, -int256(amount));
+
+        // re-stake amount back to ibera depositor
+        IInfraredBERADepositor(IInfraredBERA(InfraredBERA).depositor()).queue{
+            value: amount
+        }();
+
+        emit Sweep(IInfraredBERA(InfraredBERA).depositor(), amount);
+    }
+
+    receive() external payable {}
+}
diff --git asrc/staking (온체인)/InfraredBERAWithdraworLite.sol bsrc/staking (온체인)/InfraredBERAWithdraworLite.sol
new file mode 100644
index 0000000..fc8bb47
--- /dev/null
+++ bsrc/staking (온체인)/InfraredBERAWithdraworLite.sol
@@ -0,0 +1,188 @@
+// SPDX-License-Identifier: MIT
+pragma solidity 0.8.26;
+
+import {SafeTransferLib} from "@solmate/utils/SafeTransferLib.sol";
+import {Errors, Upgradeable} from "src/utils/Upgradeable.sol";
+import {IInfraredBERA} from "src/interfaces/IInfraredBERA.sol";
+import {IInfraredBERADepositor} from "src/interfaces/IInfraredBERADepositor.sol";
+import {IInfraredBERAClaimor} from "src/interfaces/IInfraredBERAClaimor.sol";
+import {IInfraredBERAWithdrawor} from "src/interfaces/IInfraredBERAWithdrawor.sol";
+import {InfraredBERAConstants} from "./InfraredBERAConstants.sol";
+
+/// @title InfraredBERAWithdraworLite
+/// @notice This contract is only responsible for handling involuntary exits from the CL. It is a light version of the InfraredBERAWithdrawor contract.
+/// @dev This contract should be upgraded once withdrawals are enabled by `https://github.com/berachain/beacon-kit`.
+/// @dev expects compliance of https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7002.md
+contract InfraredBERAWithdraworLite is Upgradeable, IInfraredBERAWithdrawor {
+    /// @notice The withdrawal request type, execution layer withdrawal.
+    uint8 public constant WITHDRAW_REQUEST_TYPE = 0x01;
+
+    /// @notice The address of the Withdraw Precompile settable in the next upgrade.
+    address public WITHDRAW_PRECOMPILE; // @dev: EIP7002
+
+    /// @notice The address of the `InfraredBERA.sol` contract.
+    address public InfraredBERA;
+
+    /// @notice The address of the `InfraredBERAClaimor.sol` contract.
+    /// @dev This contract will be set in the next upgrade.
+    address public claimor;
+
+    /// @notice The request struct for withdrawal requests.
+    /// @param receiver The address of the receiver of the withdrawn BERA funds.
+    /// @param timestamp The block.timestamp at which the withdraw request was issued.
+    /// @param fee The fee escrow for the withdraw precompile request.
+    /// @param amountSubmit The amount of withdrawn BERA funds left to submit request to withdraw precompile.
+    /// @param amountProcess The amount of withdrawn BERA funds left to process from funds received via withdraw request.
+    struct Request {
+        address receiver;
+        uint96 timestamp;
+        uint256 fee;
+        uint256 amountSubmit;
+        uint256 amountProcess;
+    }
+
+    /// @notice Outstanding requests for claims on previously burnt ibera
+    /// The key = nonce associated with the claim
+    mapping(uint256 => Request) public requests;
+
+    /// @notice Amount of BERA internally set aside for withdraw precompile request fees
+    uint256 public fees;
+
+    /// @notice Amount of BERA internally rebalancing amongst Infrared validators
+    uint256 public rebalancing;
+
+    /// @notice The next nonce to issue withdraw request for
+    uint256 public nonceRequest;
+
+    /// @notice The next nonce to submit withdraw request for
+    uint256 public nonceSubmit;
+
+    /// @inheritdoc IInfraredBERAWithdrawor
+    uint256 public nonceProcess;
+
+    /// Reserve storage slots for future upgrades for safety
+    uint256[40] private __gap;
+
+    /// @notice Initialize the contract (replaces the constructor)
+    /// @param _gov Address for admin / gov to upgrade
+    /// @param _keeper Address for keeper
+    /// @param ibera The initial InfraredBERA address
+    function initialize(
+        address _gov,
+        address _keeper,
+        address ibera
+    ) public initializer {
+        if (
+            _gov == address(0) || _keeper == address(0) || ibera == address(0)
+        ) {
+            revert Errors.ZeroAddress();
+        }
+        __Upgradeable_init();
+        InfraredBERA = ibera;
+
+        nonceRequest = 1;
+        nonceSubmit = 1;
+        nonceProcess = 1;
+
+        _grantRole(DEFAULT_ADMIN_ROLE, _gov);
+        _grantRole(GOVERNANCE_ROLE, _gov);
+        _grantRole(KEEPER_ROLE, _keeper);
+    }
+
+    /// @notice Checks whether enough time has passed beyond min delay
+    /// @param then The block timestamp in past
+    /// @param current The current block timestamp now
+    /// @return has Whether time between then and now exceeds forced min delay
+    function _enoughtime(
+        uint96 then,
+        uint96 current
+    ) private pure returns (bool has) {
+        unchecked {
+            has = (current - then) >= InfraredBERAConstants.FORCED_MIN_DELAY;
+        }
+    }
+
+    /// @notice Amount of BERA internally set aside to process withdraw compile requests from funds received on successful requests
+    function reserves() public view returns (uint256) {
+        return address(this).balance - fees;
+    }
+
+    /// @notice Queues a withdraw from InfraredBERA for chain withdraw precompile escrowing minimum fees for request to withdraw precompile
+    /// @dev not used until next upgrade.
+    function queue(address, uint256) external payable returns (uint256) {
+        revert Errors.WithdrawalsNotEnabled();
+    }
+
+    /// @notice Executes a withdraw request to withdraw precompile
+    /// @dev not used until next upgrade.
+    function execute(bytes calldata, uint256) external payable {
+        revert Errors.WithdrawalsNotEnabled();
+    }
+
+    /// @notice Processes the funds received from withdraw precompile to next-to-process request receiver
+    /// @dev Reverts if balance has not increased by full amount of request for next-to-process request nonce
+    /// @dev not used until next upgrade.
+    function process() external pure {
+        revert Errors.WithdrawalsNotEnabled();
+    }
+
+    /// @notice Handles Forced withdrawals from the CL.
+    /// @param pubkey The pubkey of the validator that has been forced to exit.
+    /// @dev RESTRICTED USAGE: This function should ONLY be called when:
+    /// - A validator has been forced to exit from the CL.
+    /// @dev The funds will enter the IBERA system as a deposit via the InfraredBERADepositor.
+    function sweep(bytes calldata pubkey) external onlyGovernor {
+        // only callable when withdrawals are not enabled
+        if (IInfraredBERA(InfraredBERA).withdrawalsEnabled()) {
+            revert Errors.Unauthorized(msg.sender);
+        }
+        // Check if validator has already exited - do this before checking stake
+        if (IInfraredBERA(InfraredBERA).hasExited(pubkey)) {
+            revert Errors.ValidatorForceExited();
+        }
+        // forced exit always withdraw entire stake of validator
+        uint256 amount = IInfraredBERA(InfraredBERA).stakes(pubkey);
+
+        // revert if insufficient balance
+        if (amount > address(this).balance) revert Errors.InvalidAmount();
+
+        // register new validator delta
+        IInfraredBERA(InfraredBERA).register(pubkey, -int256(amount));
+
+        // re-stake amount back to ibera depositor
+        IInfraredBERADepositor(IInfraredBERA(InfraredBERA).depositor()).queue{
+            value: amount
+        }();
+
+        emit Sweep(InfraredBERA, amount);
+    }
+
+    /// @notice Handles excess stake that was refunded from a validator due to non-IBERA deposits exceeding MAX_EFFECTIVE_BALANCE
+    /// @dev RESTRICTED USAGE: This function should ONLY be called when:
+    /// - A non-IBERA entity deposits to our validator, pushing total stake above MAX_EFFECTIVE_BALANCE
+    /// - The excess stake is refunded by the CL to this contract
+    /// @dev The funds will enter the IBERA system as yield via the FeeReceivor
+    /// @dev This should NEVER be used for:
+    /// - Validators exited due to falling out of the validator set
+    /// @param amount The amount of excess stake to sweep
+    /// @custom:access Only callable by governance
+    function sweepUnaccountedForFunds(uint256 amount) external onlyGovernor {
+        // only callable when withdrawals are not enabled
+        if (IInfraredBERA(InfraredBERA).withdrawalsEnabled()) {
+            revert Errors.Unauthorized(msg.sender);
+        }
+
+        // revert if amount exceeds balance
+        if (amount > address(this).balance) {
+            revert Errors.InvalidAmount();
+        }
+
+        address receivor = IInfraredBERA(InfraredBERA).receivor();
+        // transfer amount to ibera receivor
+        SafeTransferLib.safeTransferETH(receivor, amount);
+
+        emit Sweep(receivor, amount);
+    }
+
+    receive() external payable {}
+}

```
