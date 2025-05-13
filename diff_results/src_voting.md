# src/voting 비교 결과

원본 경로: `/Users/jonathan/berachain-project/infrared-contracts/src/voting`

온체인 경로: `/Users/jonathan/berachain-project/infrared_/src/voting`

## 디렉토리 트리 구조

```
└── 📁 voting 
    ├── 📄 README.md (추가됨)
    ├── 📄 Voter.sol (추가됨)
    ├── 📄 VotingEscrow.sol (추가됨)
    ├── 📁 libraries (추가됨)
    │   ├── 📄 BalanceLogicLibrary.sol (추가됨)
    │   ├── 📄 DelegationLogicLibrary.sol (추가됨)
    │   └── 📄 VelodromeTimeLibrary.sol (추가됨)
    ├── 📁 rewards (추가됨)
    │   ├── 📄 BribeVotingReward.sol (추가됨)
    │   ├── 📄 Reward.sol (추가됨)
    │   └── 📄 VotingReward.sol (추가됨)
    └── 📁 interfaces 
        ├── 📄 IVeArtProxy.sol (추가됨)
        ├── 📄 IVotes.sol (추가됨)
        ├── 📄 IVotingEscrow.sol (추가됨)
        ├── 📄 IReward.sol (동일)
        └── 📄 IVoter.sol (동일)
```

## 차이점

### 추가된 파일 목록

다음 파일들은 온체인 버전에만 존재하고 원본에는 없습니다:

- 📄 `README.md` (추가됨)
- 📄 `Voter.sol` (추가됨)
- 📄 `VotingEscrow.sol` (추가됨)
- 📁 `libraries/` (추가됨)
- 📁 `rewards/` (추가됨)

### 공통 파일 목록

다음 파일들은 양쪽 버전에 모두 존재합니다:

- 📁 `interfaces/`

### 파일 비교 통계

- 삭제된 파일: 0개
- 추가된 파일: 5개
- 수정된 파일: 0개
- 동일한 파일: 0개
- 총 파일 수: 5개

- 📄 `interfaces/IVeArtProxy.sol` (추가됨)
- 📄 `interfaces/IVotes.sol` (추가됨)
- 📄 `interfaces/IVotingEscrow.sol` (추가됨)

### 파일 내용 차이

```diff
diff --git asrc/voting (온체인)/README.md bsrc/voting (온체인)/README.md
new file mode 100644
index 0000000..41c8656
--- /dev/null
+++ bsrc/voting (온체인)/README.md
@@ -0,0 +1,97 @@
+
+# Voting Contracts - Infrared
+
+The `voting` contracts in Infrared enable users to participate in the allocation of IBGT rewards to various vaults through a **voting escrow (ve) system**. The contracts form a bribe-based voting mechanism, where users vote to influence the distribution of validator resources (referred to as the "cutting board") among eligible vaults. Users receive rewards based on their voting commitment, with the option for additional incentives through a bribe system.
+
+## Concepts
+
+The Infrared protocol’s voting contracts implement a **voting escrow (ve)** system. This system encourages long-term token locking by rewarding users with voting power and additional incentives when they help allocate validator resources. Key concepts include:
+
+1. **Voting Power**: Voting power is tied to the number of tokens a user locks and the duration of the lock. Longer locks yield higher voting power, which decreases as the lock expiration date nears.
+2. **Voting Escrow NFTs (veNFTs)**: When users lock tokens, they receive a unique veNFT that represents their voting power. This veNFT can also be delegated to other users for voting purposes.
+3. **Cutting Board Allocation**: The primary goal for veNFT holders is to vote on the distribution of validator resources (cutting board) across multiple vaults. By voting, users influence which vaults receive rewards and the relative weights of these rewards.
+4. **Bribe Mechanism**: external actors can offer bribes to incentivize users to vote in their favor, increasing the likelihood of a higher allocation.
+5. **Epochs and Voting Windows**: Voting periods align with weekly epochs. During each epoch, users can vote on vault allocations, and at the end of the period, votes are tallied and allocations updated.
+
+## Actors
+
+1. **User**: A participant who locks tokens in exchange for voting power. Users receive veNFTs, which allow them to vote on the allocation of validator resources to vaults.
+2. **Governor**: Holds the authority to initialize the `VotingEscrow` contract, set the `Voter` contract address, and approve new vaults eligible for voting. Governors may adjust protocol parameters but are not directly involved in vote outcomes.
+3. **Keeper**: Responsible for operational tasks, including creating new bribe vaults with `createBribeVault`, which allows voters to receive bribes for voting in favor of specific vaults.
+4. **Delegatee**: An entity that receives voting power from users who choose not to vote directly.
+5. **Whitelisted Tokens for Bribes**: Only specific, whitelisted tokens are allowed as bribes for voting. This whitelisting ensures that only tokens approved by governance are used as incentives
+
+---
+
+## Core Contracts
+
+### 1. `VotingEscrow`
+
+The `VotingEscrow` contract is central to the veTokenomics model, managing token locks and voting power.
+
+- **Token Locking**: Users lock tokens in exchange for voting power, represented by veNFTs. The longer the lock, the more voting power the user receives.
+- **Voting Power Decay**: Voting power decreases as the lock nears expiration. Users can extend locks or increase their token amounts to maintain or grow their voting power.
+- **veNFT Management**: veNFTs, representing locked positions, can be delegated to other users or used to vote on allocations.
+
+*Technical Details*: `VotingEscrow` includes structs like `LockedBalance`, `UserPoint`, and `GlobalPoint` to track user-specific and global voting power.
+
+### 2. `Voter`
+
+The `Voter` contract drives the allocation process by allowing veNFT holders to vote on cutting board distribution across vaults. Votes directly influence the weight each vault receives in the reward distribution.
+
+- **Voting on Cutting Board Allocation**: Users cast votes to determine the distribution of validator resources (cutting board) among approved vaults. Vaults with higher votes receive a larger share of resources.
+- **Bribe System with Whitelisted Tokens**: External actors can offer bribes to incentivize users to vote in favor of specific vaults. Bribes help vaults gain higher allocations by attracting more votes from veNFT holders. Importantly, only tokens that have been whitelisted by governance are allowed as incentives.
+- **Vote Tallying and Weight Assignment**: At the end of each voting window, votes are tallied, and the weights for each vault are updated to reflect user preferences.
+- **Epoch-Based Voting**: Votes are cast within a defined voting window in each weekly epoch, ensuring a predictable voting cycle.
+
+*Technical Details*: `Voter` utilizes `VelodromeTimeLibrary` to enforce voting within set windows, helping to maintain synchronized cycles across all users.
+
+### 3. `VelodromeTimeLibrary`
+
+The `VelodromeTimeLibrary` library calculates epochs and voting windows based on weekly intervals. This structure provides consistent and predictable time-based operations within the `VotingEscrow` and `Voter` contracts.
+
+- **Epoch Calculations**: Functions like `epochStart` and `epochNext` allow the protocol to determine the beginning and end of each weekly epoch.
+- **Voting Window Calculations**: The `epochVoteStart` and `epochVoteEnd` functions calculate the voting window within each epoch, ensuring that all votes are cast within the designated timeframe.
+
+---
+
+## Contract Interactions
+
+Here’s an overview of how the `voting` contracts interact:
+
+1. **Locking Tokens**:
+   - Users lock tokens in `VotingEscrow`, creating a veNFT that grants voting power.
+   - Voting power decays over time, encouraging users to commit to longer locks for greater influence.
+
+2. **Voting on Vault Allocations**:
+   - Users vote with their veNFTs in the `Voter` contract to determine how validator resources are allocated across vaults.
+   - Voting power, calculated at each vote, factors in token lock duration and decay rate.
+
+3. **Proposal and Bribe Vault Lifecycle**:
+   - Governance approves vaults eligible for voting through the Governor role.
+   - The Keeper can then create bribe vaults with `createBribeVault` to allow vaults to offer incentives (bribes) for users to vote in their favor.
+
+4. **Tallying Votes and Updating Weights**:
+   - At the end of each voting period, the `Voter` contract tallies the votes.
+   - Each vault’s allocation weight is updated based on vote totals, determining its share of resources until the next epoch.
+
+---
+
+## Security and Access Control
+
+The `voting` contracts implement specific roles for security and access control:
+
+- **Only veNFT Holders Can Vote**: Voting is restricted to users who hold veNFTs in `VotingEscrow`.
+- **Delegation Restrictions**: Users can delegate voting power through veNFTs, with delegates receiving temporary voting power based on the owner's locked balance and lock duration.
+- **Governor Role**: The Governor can initialize contracts, approve eligible vaults, and update protocol settings.
+- **Keeper Role**: The Keeper can create bribe vaults, allowing vaults to incentivize votes, making voting more competitive.
+- **Epoch-Based Voting Enforcement**: Votes are restricted to defined windows, ensuring governance actions are synchronized and follow a predictable cadence.
+- **Whitelisted Tokens for Bribes**: Only specific, whitelisted tokens are allowed as bribes for voting. This whitelisting ensures that only tokens approved by governance are used as incentives.
+
+---
+
+## Summary
+
+The `voting` contracts in Infrared implement a unique allocation mechanism that uses veTokenomics principles to distribute validator resources among vaults based on user votes. The system incentivizes long-term participation through token locking and rewards, while the bribe mechanism encourages active voting by offering additional incentives. 
+
+With clear roles for the **Governor** and **Keeper**, predictable epochs, and well-defined voting windows, the Infrared voting contracts provide an efficient and secure way for the community to influence validator resource allocation. This setup fosters user engagement and transparent decision-making, helping align incentives across the protocol.
diff --git asrc/voting (온체인)/Voter.sol bsrc/voting (온체인)/Voter.sol
new file mode 100644
index 0000000..1cbd1ce
--- /dev/null
+++ bsrc/voting (온체인)/Voter.sol
@@ -0,0 +1,519 @@
+// SPDX-License-Identifier: BUSL-1.1
+pragma solidity 0.8.26;
+
+import {ERC20} from "@solmate/tokens/ERC20.sol";
+import {SafeTransferLib} from "@solmate/utils/SafeTransferLib.sol";
+
+import {ReentrancyGuardUpgradeable} from "@openzeppelin-upgradeable/utils/ReentrancyGuardUpgradeable.sol";
+
+import {InfraredUpgradeable} from "src/core/InfraredUpgradeable.sol";
+import {Errors} from "src/utils/Errors.sol";
+
+import {IReward} from "src/voting/interfaces/IReward.sol";
+import {IVoter} from "src/voting/interfaces/IVoter.sol";
+import {IVotingEscrow} from "src/voting/interfaces/IVotingEscrow.sol";
+
+import {BribeVotingReward} from "src/voting/rewards/BribeVotingReward.sol";
+import {VelodromeTimeLibrary} from "src/voting/libraries/VelodromeTimeLibrary.sol";
+
+import {IInfrared} from "src/interfaces/IInfrared.sol";
+
+/// @title Infrared Voting POL CuttingBoard
+/// @dev This contract manages votes for POL CuttingBoard allocation and respective bribeVault creation.
+///      It also provides support for depositing and withdrawing from managed veNFTs. Inspired by Velodrome V2 Voter.
+/// @author Modified from Velodrome (https://github.com/velodrome-finance/contracts/blob/main/contracts/Voter.sol)
+/// @notice Ensure new epoch before voting and manage staking tokens and bribe vaults.
+contract Voter is IVoter, InfraredUpgradeable, ReentrancyGuardUpgradeable {
+    using SafeTransferLib for ERC20;
+
+    /// @inheritdoc IVoter
+    address public ve;
+
+    /// @inheritdoc IVoter
+    uint256 public totalWeight;
+
+    /// @inheritdoc IVoter
+    uint256 public maxVotingNum;
+
+    /**
+     * @notice Minimum allowed value for maximum voting number
+     *  @dev Used as validation threshold in setMaxVotingNum
+     */
+    uint256 internal constant MIN_MAXVOTINGNUM = 1;
+
+    /// @inheritdoc IVoter
+    address public feeVault;
+
+    /**
+     * @dev Internal array of all staking tokens with active bribe vaults
+     *      Used for token enumeration and state tracking
+     */
+    address[] public stakingTokens;
+
+    /// @inheritdoc IVoter
+    mapping(address => address) public bribeVaults;
+    /// @inheritdoc IVoter
+    mapping(address => uint256) public weights;
+    /// @inheritdoc IVoter
+    mapping(uint256 => mapping(address => uint256)) public votes;
+    /// @dev NFT => List of stakingTokens voted for by NFT
+    mapping(uint256 => address[]) public stakingTokenVote;
+    /// @inheritdoc IVoter
+    mapping(uint256 => uint256) public usedWeights;
+    /// @inheritdoc IVoter
+    mapping(uint256 => uint256) public lastVoted;
+    /// @inheritdoc IVoter
+    mapping(uint256 => bool) public isWhitelistedNFT;
+    /// @inheritdoc IVoter
+    mapping(address => bool) public isAlive;
+
+    /**
+     * @notice Ensures operations only occur in new epochs and outside distribution window
+     * @dev Validates both epoch transition and proper timing within epoch
+     * @param _tokenId The token ID to check last vote timestamp for
+     */
+    modifier onlyNewEpoch(uint256 _tokenId) {
+        // ensure new epoch since last vote
+        if (
+            VelodromeTimeLibrary.epochStart(block.timestamp) <=
+            lastVoted[_tokenId]
+        ) revert AlreadyVotedOrDeposited();
+        if (
+            block.timestamp <=
+            VelodromeTimeLibrary.epochVoteStart(block.timestamp)
+        ) revert DistributeWindow();
+        _;
+    }
+
+    /// @inheritdoc IVoter
+    function epochStart(uint256 _timestamp) external pure returns (uint256) {
+        return VelodromeTimeLibrary.epochStart(_timestamp);
+    }
+    /// @inheritdoc IVoter
+
+    function epochNext(uint256 _timestamp) external pure returns (uint256) {
+        return VelodromeTimeLibrary.epochNext(_timestamp);
+    }
+
+    /// @inheritdoc IVoter
+    function epochVoteStart(
+        uint256 _timestamp
+    ) external pure returns (uint256) {
+        return VelodromeTimeLibrary.epochVoteStart(_timestamp);
+    }
+
+    /// @inheritdoc IVoter
+    function epochVoteEnd(uint256 _timestamp) external pure returns (uint256) {
+        return VelodromeTimeLibrary.epochVoteEnd(_timestamp);
+    }
+
+    /**
+     * @notice Constructor for Voter contract
+     * @dev Reverts if infrared address is zero
+     * @param _infrared Address of the Infrared contract
+     */
+
+    /**
+     * @notice Initializes the Voter contract with the voting escrow and fee vault
+     * @dev Sets up initial state including fee vault with configured reward tokens
+     * @param _ve Address of the voting escrow contract
+     * @param _gov Address of the governance multisig
+     * @param _keeper Address of the keeper
+     */
+    function initialize(
+        address _ve,
+        address _gov,
+        address _keeper
+    ) external initializer {
+        if (_ve == address(0)) revert Errors.ZeroAddress();
+        ve = _ve;
+        maxVotingNum = 30;
+
+        // adaptation to create fee vault for global fees amongst all voters
+        address[] memory _rewards = new address[](2);
+        _rewards[0] = address(infrared.ibgt());
+        _rewards[1] = address(infrared.honey());
+
+        feeVault = address(new BribeVotingReward(address(this), _rewards));
+
+        _grantRole(DEFAULT_ADMIN_ROLE, _gov);
+        _grantRole(GOVERNANCE_ROLE, _gov);
+        _grantRole(KEEPER_ROLE, _keeper);
+
+        // init upgradeable components
+        __ReentrancyGuard_init();
+        __InfraredUpgradeable_init(_keeper);
+    }
+
+    /// @inheritdoc IVoter
+    function setMaxVotingNum(uint256 _maxVotingNum) external onlyGovernor {
+        if (_maxVotingNum < MIN_MAXVOTINGNUM) {
+            revert MaximumVotingNumberTooLow();
+        }
+        if (_maxVotingNum == maxVotingNum) revert SameValue();
+        maxVotingNum = _maxVotingNum;
+        emit MaxVotingNumSet(_maxVotingNum);
+    }
+
+    /// @inheritdoc IVoter
+    function reset(
+        uint256 _tokenId
+    ) external onlyNewEpoch(_tokenId) nonReentrant {
+        if (!IVotingEscrow(ve).isApprovedOrOwner(msg.sender, _tokenId)) {
+            revert NotApprovedOrOwner();
+        }
+        _reset(_tokenId);
+    }
+
+    /**
+     * @notice Resets vote state for a token ID
+     * @dev Cleans up all vote accounting and emits appropriate events
+     * @param _tokenId Token ID to reset voting state for
+     */
+    function _reset(uint256 _tokenId) internal {
+        address[] storage _stakingTokenVote = stakingTokenVote[_tokenId];
+        uint256 _stakingTokenVoteCnt = _stakingTokenVote.length;
+        uint256 _totalWeight = 0;
+
+        for (uint256 i = 0; i < _stakingTokenVoteCnt; i++) {
+            address _stakingToken = _stakingTokenVote[i];
+            uint256 _votes = votes[_tokenId][_stakingToken];
+
+            if (_votes != 0) {
+                weights[_stakingToken] -= _votes;
+                delete votes[_tokenId][_stakingToken];
+                IReward(bribeVaults[_stakingToken])._withdraw(_votes, _tokenId);
+                _totalWeight += _votes;
+                emit Abstained(
+                    msg.sender,
+                    _stakingToken,
+                    _tokenId,
+                    _votes,
+                    weights[_stakingToken],
+                    block.timestamp
+                );
+            }
+        }
+        IVotingEscrow(ve).voting(_tokenId, false);
+        // @dev withdraw from fees reward vault in addition to marking tokenId as not voted
+        IReward(feeVault)._withdraw(usedWeights[_tokenId], _tokenId);
+        totalWeight -= _totalWeight;
+        usedWeights[_tokenId] = 0;
+        delete stakingTokenVote[_tokenId];
+    }
+
+    /// @inheritdoc IVoter
+    function poke(uint256 _tokenId) external nonReentrant {
+        if (
+            block.timestamp <=
+            VelodromeTimeLibrary.epochVoteStart(block.timestamp)
+        ) revert DistributeWindow();
+        uint256 _weight = IVotingEscrow(ve).balanceOfNFT(_tokenId);
+        _poke(_tokenId, _weight);
+    }
+
+    /**
+     * @notice Updates voting power for a token ID
+     * @dev Recalculates and updates all vote weightings
+     * @param _tokenId Token ID to update voting power for
+     * @param _weight New voting power weight to apply
+     */
+    function _poke(uint256 _tokenId, uint256 _weight) internal {
+        address[] memory _stakingTokenVote = stakingTokenVote[_tokenId];
+        uint256 _stakingTokenCnt = _stakingTokenVote.length;
+        uint256[] memory _weights = new uint256[](_stakingTokenCnt);
+
+        for (uint256 i = 0; i < _stakingTokenCnt; i++) {
+            _weights[i] = votes[_tokenId][_stakingTokenVote[i]];
+        }
+        _vote(_tokenId, _weight, _stakingTokenVote, _weights, true);
+    }
+
+    /**
+     * @notice Core voting logic to allocate weights to staking tokens
+     * @param _tokenId Token ID that is voting
+     * @param _weight Total voting power weight available
+     * @param _stakingTokenVote Array of staking tokens to vote for
+     * @param _weights Array of weights to allocate to each token
+     * @param _isPoke if fees should be deposited in addition to marking tokenId as voted
+     * @dev Handles vote accounting, reward deposits and event emissions
+     * @dev Implementation sequence:
+     * 1. Reset all existing votes and accounting via _reset
+     * 2. Calculate total vote weight for normalizing allocations
+     * 3. For each staking token:
+     *    - Validate bribe vault exists and is active
+     *    - Calculate and apply normalized vote weight
+     *    - Update token-specific accounting
+     *    - Deposit into bribe vault
+     * 4. Update global vote accounting if votes were cast
+     * 5. If _isPoke is true, skip processing for tokens with killed bribe vaults
+     */
+    function _vote(
+        uint256 _tokenId,
+        uint256 _weight,
+        address[] memory _stakingTokenVote,
+        uint256[] memory _weights,
+        bool _isPoke
+    ) internal {
+        _reset(_tokenId);
+        uint256 _stakingTokenCnt = _stakingTokenVote.length;
+        uint256 _totalVoteWeight = 0;
+        uint256 _totalWeight = 0;
+        uint256 _usedWeight = 0;
+
+        for (uint256 i = 0; i < _stakingTokenCnt; i++) {
+            _totalVoteWeight += _weights[i];
+        }
+
+        for (uint256 i = 0; i < _stakingTokenCnt; i++) {
+            address _stakingToken = _stakingTokenVote[i];
+            address _bribeVault = bribeVaults[_stakingToken];
+            if (_bribeVault == address(0)) {
+                revert BribeVaultDoesNotExist(_stakingToken);
+            }
+            if (!isAlive[_stakingToken]) {
+                if (_isPoke) {
+                    emit SkipKilledBribeVault(_stakingToken, _tokenId);
+                    continue; // Skip this token without affecting totalWeight and usedWeights
+                    // this effectively means user is using less than 100% of their voting power
+                }
+                revert BribeVaultNotAlive(_bribeVault);
+            }
+
+            uint256 _stakingTokenWeight = (_weights[i] * _weight) /
+                _totalVoteWeight;
+            if (votes[_tokenId][_stakingToken] != 0) revert NonZeroVotes();
+            if (_stakingTokenWeight == 0) revert ZeroBalance();
+
+            stakingTokenVote[_tokenId].push(_stakingToken);
+
+            weights[_stakingToken] += _stakingTokenWeight;
+            votes[_tokenId][_stakingToken] += _stakingTokenWeight;
+
+            IReward(_bribeVault)._deposit(_stakingTokenWeight, _tokenId);
+
+            _usedWeight += _stakingTokenWeight;
+            _totalWeight += _stakingTokenWeight;
+            emit Voted(
+                msg.sender,
+                _stakingToken,
+                _tokenId,
+                _stakingTokenWeight,
+                weights[_stakingToken],
+                block.timestamp
+            );
+        }
+        if (_usedWeight > 0) {
+            IVotingEscrow(ve).voting(_tokenId, true);
+            // @dev deposit in fees reward vault in addition to marking tokenId as voted
+            IReward(feeVault)._deposit(_usedWeight, _tokenId);
+        }
+        totalWeight += _totalWeight;
+        usedWeights[_tokenId] = _usedWeight;
+    }
+
+    /// @inheritdoc IVoter
+    function vote(
+        uint256 _tokenId,
+        address[] calldata _stakingTokenVote,
+        uint256[] calldata _weights
+    ) external onlyNewEpoch(_tokenId) nonReentrant {
+        if (!IVotingEscrow(ve).isApprovedOrOwner(msg.sender, _tokenId)) {
+            revert NotApprovedOrOwner();
+        }
+        if (_stakingTokenVote.length != _weights.length) {
+            revert UnequalLengths();
+        }
+        if (_stakingTokenVote.length > maxVotingNum) {
+            revert TooManyStakingTokens();
+        }
+        if (IVotingEscrow(ve).deactivated(_tokenId)) {
+            revert InactiveManagedNFT();
+        }
+        uint256 _timestamp = block.timestamp;
+        if (
+            (_timestamp > VelodromeTimeLibrary.epochVoteEnd(_timestamp)) &&
+            !isWhitelistedNFT[_tokenId]
+        ) {
+            revert NotWhitelistedNFT();
+        }
+        lastVoted[_tokenId] = _timestamp;
+        uint256 _weight = IVotingEscrow(ve).balanceOfNFT(_tokenId);
+        _vote(_tokenId, _weight, _stakingTokenVote, _weights, false);
+    }
+
+    /// @inheritdoc IVoter
+    function depositManaged(
+        uint256 _tokenId,
+        uint256 _mTokenId
+    ) external nonReentrant onlyNewEpoch(_tokenId) {
+        if (!IVotingEscrow(ve).isApprovedOrOwner(msg.sender, _tokenId)) {
+            revert NotApprovedOrOwner();
+        }
+        if (IVotingEscrow(ve).deactivated(_mTokenId)) {
+            revert InactiveManagedNFT();
+        }
+        _reset(_tokenId);
+        uint256 _timestamp = block.timestamp;
+        if (_timestamp > VelodromeTimeLibrary.epochVoteEnd(_timestamp)) {
+            revert SpecialVotingWindow();
+        }
+        lastVoted[_tokenId] = _timestamp;
+        IVotingEscrow(ve).depositManaged(_tokenId, _mTokenId);
+        uint256 _weight = IVotingEscrow(ve).balanceOfNFTAt(
+            _mTokenId,
+            block.timestamp
+        );
+        _poke(_mTokenId, _weight);
+    }
+
+    /// @inheritdoc IVoter
+    function withdrawManaged(
+        uint256 _tokenId
+    ) external nonReentrant onlyNewEpoch(_tokenId) {
+        if (!IVotingEscrow(ve).isApprovedOrOwner(msg.sender, _tokenId)) {
+            revert NotApprovedOrOwner();
+        }
+        uint256 _mTokenId = IVotingEscrow(ve).idToManaged(_tokenId);
+        IVotingEscrow(ve).withdrawManaged(_tokenId);
+        // If the NORMAL veNFT was the last tokenId locked into _mTokenId, reset vote as there is
+        // no longer voting power available to the _mTokenId.  Otherwise, updating voting power to accurately
+        // reflect the withdrawn voting power.
+        uint256 _weight = IVotingEscrow(ve).balanceOfNFTAt(
+            _mTokenId,
+            block.timestamp
+        );
+        if (_weight == 0) {
+            _reset(_mTokenId);
+            // clear out lastVoted to allow re-voting in the current epoch
+            delete lastVoted[_mTokenId];
+        } else {
+            _poke(_mTokenId, _weight);
+        }
+    }
+
+    /// @inheritdoc IVoter
+    function isWhitelistedToken(address _token) external view returns (bool) {
+        return infrared.whitelistedRewardTokens(_token);
+    }
+
+    /// @inheritdoc IVoter
+    function whitelistNFT(uint256 _tokenId, bool _bool) external onlyGovernor {
+        isWhitelistedNFT[_tokenId] = _bool;
+        emit WhitelistNFT(msg.sender, _tokenId, _bool);
+    }
+
+    /// @inheritdoc IVoter
+    function createBribeVault(
+        address _stakingToken,
+        address[] calldata _rewards
+    ) external onlyKeeper nonReentrant whenInitialized returns (address) {
+        if (address(infrared.vaultRegistry(_stakingToken)) == address(0)) {
+            revert VaultNotRegistered();
+        }
+        if (bribeVaults[_stakingToken] != address(0)) revert BribeVaultExists();
+
+        // iterate through rewards to ensure they are whitelisted
+        uint256 _rewardsLength = _rewards.length;
+        for (uint256 i = 0; i < _rewardsLength; i++) {
+            if (!infrared.whitelistedRewardTokens(_rewards[i])) {
+                revert NotWhitelistedToken();
+            }
+        }
+
+        // adaptation to only create bribe voting rewards
+        address _bribeVault = address(
+            new BribeVotingReward(address(this), _rewards)
+        );
+
+        bribeVaults[_stakingToken] = _bribeVault;
+
+        stakingTokens.push(_stakingToken);
+        isAlive[_stakingToken] = true;
+
+        emit BribeVaultCreated(_stakingToken, _bribeVault, msg.sender);
+        return _bribeVault;
+    }
+
+    /// @inheritdoc IVoter
+    function killBribeVault(address _stakingToken) external onlyGovernor {
+        if (!isAlive[_stakingToken]) revert BribeVaultAlreadyKilled();
+        isAlive[_stakingToken] = false;
+        emit BribeVaultKilled(_stakingToken);
+    }
+
+    /// @inheritdoc IVoter
+    function reviveBribeVault(address _stakingToken) external onlyGovernor {
+        if (isAlive[_stakingToken]) revert BribeVaultAlreadyRevived();
+        isAlive[_stakingToken] = true;
+        emit BribeVaultRevived(_stakingToken);
+    }
+
+    /// @inheritdoc IVoter
+    function length() external view returns (uint256) {
+        return stakingTokens.length;
+    }
+
+    /// @inheritdoc IVoter
+    function claimBribes(
+        address[] memory _bribes,
+        address[][] memory _tokens,
+        uint256 _tokenId
+    ) external {
+        if (!IVotingEscrow(ve).isApprovedOrOwner(msg.sender, _tokenId)) {
+            revert NotApprovedOrOwner();
+        }
+        uint256 _length = _bribes.length;
+        if (_length != _tokens.length) {
+            revert UnequalLengths();
+        }
+        for (uint256 i = 0; i < _length; i++) {
+            IReward(_bribes[i]).getReward(_tokenId, _tokens[i]);
+        }
+    }
+
+    /// @inheritdoc IVoter
+    function claimFees(address[] memory _tokens, uint256 _tokenId) external {
+        if (!IVotingEscrow(ve).isApprovedOrOwner(msg.sender, _tokenId)) {
+            revert NotApprovedOrOwner();
+        }
+        IReward(feeVault).getReward(_tokenId, _tokens);
+    }
+
+    /**
+     * @notice Returns all staking tokens and their current voting weights
+     * @dev Helper function that aggregates staking token data
+     * @return _stakingTokens Array of staking token addresses
+     * @return _weights Array of voting weights corresponding to each token
+     * @return _totalWeight Sum of all voting weights
+     */
+    function getStakingTokenWeights()
+        public
+        view
+        returns (
+            address[] memory _stakingTokens,
+            uint256[] memory _weights,
+            uint256 _totalWeight
+        )
+    {
+        uint256 _length = stakingTokens.length;
+        _weights = new uint256[](_length);
+        _stakingTokens = new address[](_length);
+        uint256 count = 0;
+
+        for (uint256 i = 0; i < _length; i++) {
+            address token = stakingTokens[i];
+
+            _weights[count] = weights[token];
+            _stakingTokens[count] = token;
+            _totalWeight += _weights[count];
+            count++;
+        }
+
+        // Resize the arrays to remove unfilled entries
+        assembly {
+            mstore(_weights, count)
+            mstore(_stakingTokens, count)
+        }
+    }
+}
diff --git asrc/voting (온체인)/VotingEscrow.sol bsrc/voting (온체인)/VotingEscrow.sol
new file mode 100644
index 0000000..5345354
--- /dev/null
+++ bsrc/voting (온체인)/VotingEscrow.sol
@@ -0,0 +1,1446 @@
+// SPDX-License-Identifier: BUSL-1.1
+pragma solidity 0.8.26;
+
+import {IERC721Receiver} from
+    "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
+import {IVeArtProxy} from "./interfaces/IVeArtProxy.sol";
+import {IVotingEscrow} from "./interfaces/IVotingEscrow.sol";
+import {ERC20} from "@solmate/tokens/ERC20.sol";
+import {SafeTransferLib} from "@solmate/utils/SafeTransferLib.sol";
+import {ReentrancyGuard} from
+    "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
+import {DelegationLogicLibrary} from "./libraries/DelegationLogicLibrary.sol";
+import {BalanceLogicLibrary} from "./libraries/BalanceLogicLibrary.sol";
+
+import {SafeCastLib} from "lib/solady/src/utils/SafeCastLib.sol";
+import {IInfraredUpgradeable} from "src/interfaces/IInfraredUpgradeable.sol";
+
+/// @title Voting Escrow Infrared
+/// @notice veNFT implementation that escrows ERC-20 tokens in the form of an ERC-721 NFT
+/// @notice Votes have a weight depending on time, so that users are committed to the future of (whatever they are voting for)
+/// @author Modified from Solidly (https://github.com/solidlyexchange/solidly/blob/master/contracts/ve.sol)
+/// @author Modified from Curve (https://github.com/curvefi/curve-dao-contracts/blob/master/contracts/VotingEscrow.vy)
+/// @author Modified from velodrome.finance (https://github.com/velodrome-finance/contracts/blob/main/contracts/VotingEscrow.sol)
+/// @dev Vote weight decays linearly over time. Lock time cannot be more than `MAXTIME` (4 years).
+contract VotingEscrow is IVotingEscrow, ReentrancyGuard {
+    using SafeTransferLib for ERC20;
+    using SafeCastLib for uint256;
+    using SafeCastLib for int128;
+    /*//////////////////////////////////////////////////////////////
+                               CONSTRUCTOR
+    //////////////////////////////////////////////////////////////*/
+
+    address public immutable keeper;
+    /// @inheritdoc IVotingEscrow
+    address public immutable token;
+    /// @inheritdoc IVotingEscrow
+    address public distributor;
+    /// @inheritdoc IVotingEscrow
+    address public voter;
+    /// @inheritdoc IVotingEscrow
+    address public artProxy;
+    /// @inheritdoc IVotingEscrow
+    address public allowedManager;
+
+    mapping(uint256 => GlobalPoint) internal _pointHistory; // epoch -> unsigned global point
+
+    /// @dev Mapping of interface id to bool about whether or not it's supported
+    mapping(bytes4 => bool) internal supportedInterfaces;
+
+    /// @dev ERC165 interface ID of ERC165
+    bytes4 internal constant ERC165_INTERFACE_ID = 0x01ffc9a7;
+
+    /// @dev ERC165 interface ID of ERC721
+    bytes4 internal constant ERC721_INTERFACE_ID = 0x80ac58cd;
+
+    /// @dev ERC165 interface ID of ERC721Metadata
+    bytes4 internal constant ERC721_METADATA_INTERFACE_ID = 0x5b5e139f;
+
+    /// @dev ERC165 interface ID of ERC4906
+    bytes4 internal constant ERC4906_INTERFACE_ID = 0x49064906;
+
+    /// @dev ERC165 interface ID of ERC6372
+    bytes4 internal constant ERC6372_INTERFACE_ID = 0xda287a1d;
+
+    /// @inheritdoc IVotingEscrow
+    uint256 public tokenId;
+
+    /// @inheritdoc IVotingEscrow
+    IInfraredUpgradeable public immutable infrared;
+
+    /**
+     * @notice Initializes VotingEscrow contract
+     * @param _keeper Address of keeper contract
+     * @param _token Address of token (RED) used to create a veNFT
+     * @param _voter Address of Voter contract
+     * @param _infrared Address of Infrared contract
+     */
+    constructor(
+        address _keeper,
+        address _token,
+        address _voter,
+        address _infrared
+    ) {
+        if (
+            _keeper == address(0) || _token == address(0)
+                || _voter == address(0) || _infrared == address(0)
+        ) revert ZeroAddress();
+        keeper = _keeper;
+        token = _token;
+        voter = _voter;
+        infrared = IInfraredUpgradeable(_infrared);
+
+        _pointHistory[0].blk = block.number;
+        _pointHistory[0].ts = block.timestamp;
+
+        supportedInterfaces[ERC165_INTERFACE_ID] = true;
+        supportedInterfaces[ERC721_INTERFACE_ID] = true;
+        supportedInterfaces[ERC721_METADATA_INTERFACE_ID] = true;
+        supportedInterfaces[ERC4906_INTERFACE_ID] = true;
+        supportedInterfaces[ERC6372_INTERFACE_ID] = true;
+
+        // mint-ish
+        emit Transfer(address(0), address(this), tokenId);
+        // burn-ish
+        emit Transfer(address(this), address(0), tokenId);
+    }
+
+    /*///////////////////////////////////////////////////////////////
+                            MANAGED NFT STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    /// @inheritdoc IVotingEscrow
+    mapping(uint256 => EscrowType) public escrowType;
+
+    /// @inheritdoc IVotingEscrow
+    mapping(uint256 => uint256) public idToManaged;
+    /// @inheritdoc IVotingEscrow
+    mapping(uint256 => mapping(uint256 => uint256)) public weights;
+    /// @inheritdoc IVotingEscrow
+    mapping(uint256 => bool) public deactivated;
+
+    /*///////////////////////////////////////////////////////////////
+                            MANAGED NFT LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @inheritdoc IVotingEscrow
+    function createManagedLockFor(address _to)
+        external
+        nonReentrant
+        returns (uint256 _mTokenId)
+    {
+        if (
+            msg.sender != allowedManager
+                && !infrared.hasRole(infrared.GOVERNANCE_ROLE(), msg.sender)
+        ) {
+            revert NotGovernorOrManager();
+        }
+
+        _mTokenId = ++tokenId;
+        _mint(_to, _mTokenId);
+        _depositFor(
+            _mTokenId,
+            0,
+            0,
+            LockedBalance(0, 0, true),
+            DepositType.CREATE_LOCK_TYPE
+        );
+
+        escrowType[_mTokenId] = EscrowType.MANAGED;
+
+        emit CreateManaged(_to, _mTokenId, msg.sender);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function depositManaged(uint256 _tokenId, uint256 _mTokenId)
+        external
+        nonReentrant
+    {
+        if (msg.sender != voter) revert NotVoter();
+        if (escrowType[_mTokenId] != EscrowType.MANAGED) revert NotManagedNFT();
+        if (escrowType[_tokenId] != EscrowType.NORMAL) revert NotNormalNFT();
+        if (_balanceOfNFTAt(_tokenId, block.timestamp) == 0) {
+            revert ZeroBalance();
+        }
+
+        // adjust user nft
+        int128 _amount = _locked[_tokenId].amount;
+        if (_locked[_tokenId].isPermanent) {
+            permanentLockBalance -= _amount.toUint256();
+            _delegate(_tokenId, 0);
+        }
+        _checkpoint(_tokenId, _locked[_tokenId], LockedBalance(0, 0, false));
+        _locked[_tokenId] = LockedBalance(0, 0, false);
+
+        // adjust managed nft
+        uint256 _weight = _amount.toUint256();
+        permanentLockBalance += _weight;
+        LockedBalance memory newLocked = _locked[_mTokenId];
+        newLocked.amount += _amount;
+        _checkpointDelegatee(_delegates[_mTokenId], _weight, true);
+        _checkpoint(_mTokenId, _locked[_mTokenId], newLocked);
+        _locked[_mTokenId] = newLocked;
+
+        weights[_tokenId][_mTokenId] = _weight;
+        idToManaged[_tokenId] = _mTokenId;
+        escrowType[_tokenId] = EscrowType.LOCKED;
+
+        emit DepositManaged(
+            _ownerOf(_tokenId), _tokenId, _mTokenId, _weight, block.timestamp
+        );
+        emit MetadataUpdate(_tokenId);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function withdrawManaged(uint256 _tokenId) external nonReentrant {
+        uint256 _mTokenId = idToManaged[_tokenId];
+        if (msg.sender != voter) revert NotVoter();
+        if (_mTokenId == 0) revert InvalidManagedNFTId();
+        if (escrowType[_tokenId] != EscrowType.LOCKED) revert NotLockedNFT();
+
+        // update accrued rewards
+        uint256 _weight = weights[_tokenId][_mTokenId];
+        uint256 _total = _weight;
+        uint256 _unlockTime = ((block.timestamp + MAXTIME) / WEEK) * WEEK;
+
+        // adjust user nft
+        LockedBalance memory newLockedNormal =
+            LockedBalance(_total.toInt128(), _unlockTime, false);
+        _checkpoint(_tokenId, _locked[_tokenId], newLockedNormal);
+        _locked[_tokenId] = newLockedNormal;
+
+        // adjust managed nft
+        LockedBalance memory newLockedManaged = _locked[_mTokenId];
+        // do not expect _total > locked.amount / permanentLockBalance but just in case
+        newLockedManaged.amount -= (
+            _total.toInt128() < newLockedManaged.amount
+                ? _total.toInt128()
+                : newLockedManaged.amount
+        );
+        permanentLockBalance -=
+            (_total < permanentLockBalance ? _total : permanentLockBalance);
+        _checkpointDelegatee(_delegates[_mTokenId], _total, false);
+        _checkpoint(_mTokenId, _locked[_mTokenId], newLockedManaged);
+        _locked[_mTokenId] = newLockedManaged;
+
+        delete idToManaged[_tokenId];
+        delete weights[_tokenId][_mTokenId];
+        delete escrowType[_tokenId];
+
+        emit WithdrawManaged(
+            _ownerOf(_tokenId), _tokenId, _mTokenId, _total, block.timestamp
+        );
+        emit MetadataUpdate(_tokenId);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function setAllowedManager(address _allowedManager) external {
+        if (!infrared.hasRole(infrared.GOVERNANCE_ROLE(), msg.sender)) {
+            revert NotGovernor();
+        }
+        if (_allowedManager == allowedManager) revert SameAddress();
+        if (_allowedManager == address(0)) revert ZeroAddress();
+        allowedManager = _allowedManager;
+        emit SetAllowedManager(_allowedManager);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function setManagedState(uint256 _mTokenId, bool _state) external {
+        if (!infrared.hasRole(infrared.GOVERNANCE_ROLE(), msg.sender)) {
+            revert NotGovernor();
+        }
+        if (escrowType[_mTokenId] != EscrowType.MANAGED) revert NotManagedNFT();
+        if (deactivated[_mTokenId] == _state) revert SameState();
+        deactivated[_mTokenId] = _state;
+    }
+
+    /*///////////////////////////////////////////////////////////////
+                             METADATA STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    string public constant name = "veNFT";
+    string public constant symbol = "veNFT";
+    string public constant version = "2.0.0";
+    uint8 public constant decimals = 18;
+
+    function setArtProxy(address _proxy) external {
+        if (_proxy == address(0)) revert ZeroAddress();
+        if (!infrared.hasRole(infrared.GOVERNANCE_ROLE(), msg.sender)) {
+            revert NotGovernor();
+        }
+        artProxy = _proxy;
+        emit BatchMetadataUpdate(0, type(uint256).max);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function tokenURI(uint256 _tokenId) external view returns (string memory) {
+        if (_ownerOf(_tokenId) == address(0)) revert NonExistentToken();
+        return IVeArtProxy(artProxy).tokenURI(_tokenId);
+    }
+
+    /*//////////////////////////////////////////////////////////////
+                      ERC721 BALANCE/OWNER STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    /// @dev Mapping from NFT ID to the address that owns it.
+    mapping(uint256 => address) internal idToOwner;
+
+    /// @dev Mapping from owner address to count of his tokens.
+    mapping(address => uint256) internal ownerToNFTokenCount;
+
+    function _ownerOf(uint256 _tokenId) internal view returns (address) {
+        return idToOwner[_tokenId];
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function ownerOf(uint256 _tokenId) external view returns (address) {
+        return _ownerOf(_tokenId);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function balanceOf(address _owner) external view returns (uint256) {
+        return ownerToNFTokenCount[_owner];
+    }
+
+    /*//////////////////////////////////////////////////////////////
+                         ERC721 APPROVAL STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    /// @dev Mapping from NFT ID to approved address.
+    mapping(uint256 => address) internal idToApprovals;
+
+    /// @dev Mapping from owner address to mapping of operator addresses.
+    mapping(address => mapping(address => bool)) internal ownerToOperators;
+
+    mapping(uint256 => uint256) internal ownershipChange;
+
+    /// @inheritdoc IVotingEscrow
+    function getApproved(uint256 _tokenId) external view returns (address) {
+        return idToApprovals[_tokenId];
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function isApprovedForAll(address _owner, address _operator)
+        external
+        view
+        returns (bool)
+    {
+        return (ownerToOperators[_owner])[_operator];
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function isApprovedOrOwner(address _spender, uint256 _tokenId)
+        external
+        view
+        returns (bool)
+    {
+        return _isApprovedOrOwner(_spender, _tokenId);
+    }
+
+    function _isApprovedOrOwner(address _spender, uint256 _tokenId)
+        internal
+        view
+        returns (bool)
+    {
+        address owner = _ownerOf(_tokenId);
+        bool spenderIsOwner = owner == _spender;
+        bool spenderIsApproved = _spender == idToApprovals[_tokenId];
+        bool spenderIsApprovedForAll = (ownerToOperators[owner])[_spender];
+        return spenderIsOwner || spenderIsApproved || spenderIsApprovedForAll;
+    }
+
+    /*//////////////////////////////////////////////////////////////
+                              ERC721 LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @inheritdoc IVotingEscrow
+    function approve(address _approved, uint256 _tokenId) external {
+        address owner = _ownerOf(_tokenId);
+        // Throws if `_tokenId` is not a valid NFT
+        if (owner == address(0)) revert ZeroAddress();
+        // Throws if `_approved` is the current owner
+        if (owner == _approved) revert SameAddress();
+        // Check requirements
+        bool senderIsOwner = (_ownerOf(_tokenId) == msg.sender);
+        bool senderIsApprovedForAll = (ownerToOperators[owner])[msg.sender];
+        if (!senderIsOwner && !senderIsApprovedForAll) {
+            revert NotApprovedOrOwner();
+        }
+        // Set the approval
+        idToApprovals[_tokenId] = _approved;
+        emit Approval(owner, _approved, _tokenId);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function setApprovalForAll(address _operator, bool _approved) external {
+        // Throws if `_operator` is the `msg.sender`
+        if (_operator == msg.sender) revert SameAddress();
+        ownerToOperators[msg.sender][_operator] = _approved;
+        emit ApprovalForAll(msg.sender, _operator, _approved);
+    }
+
+    /* TRANSFER FUNCTIONS */
+
+    function _transferFrom(
+        address _from,
+        address _to,
+        uint256 _tokenId,
+        address _sender
+    ) internal {
+        if (escrowType[_tokenId] == EscrowType.LOCKED) {
+            revert NotManagedOrNormalNFT();
+        }
+        // Check requirements
+        if (!_isApprovedOrOwner(_sender, _tokenId)) revert NotApprovedOrOwner();
+        // Clear approval. Throws if `_from` is not the current owner
+        if (_ownerOf(_tokenId) != _from) revert NotOwner();
+        delete idToApprovals[_tokenId];
+        // Remove NFT. Throws if `_tokenId` is not a valid NFT
+        _removeTokenFrom(_from, _tokenId);
+        // Update voting checkpoints
+        _checkpointDelegator(_tokenId, 0, _to);
+        // Add NFT
+        _addTokenTo(_to, _tokenId);
+        // Set the block of ownership transfer (for Flash NFT protection)
+        ownershipChange[_tokenId] = block.number;
+        // Log the transfer
+        emit Transfer(_from, _to, _tokenId);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function transferFrom(address _from, address _to, uint256 _tokenId)
+        external
+    {
+        _transferFrom(_from, _to, _tokenId, msg.sender);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function safeTransferFrom(address _from, address _to, uint256 _tokenId)
+        external
+    {
+        safeTransferFrom(_from, _to, _tokenId, "");
+    }
+
+    function _isContract(address account) internal view returns (bool) {
+        // This method relies on extcodesize, which returns 0 for contracts in
+        // construction, since the code is only stored at the end of the
+        // constructor execution.
+        uint256 size;
+        assembly {
+            size := extcodesize(account)
+        }
+        return size > 0;
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function safeTransferFrom(
+        address _from,
+        address _to,
+        uint256 _tokenId,
+        bytes memory _data
+    ) public {
+        _transferFrom(_from, _to, _tokenId, msg.sender);
+
+        if (_isContract(_to)) {
+            // Throws if transfer destination is a contract which does not implement 'onERC721Received'
+            try IERC721Receiver(_to).onERC721Received(
+                msg.sender, _from, _tokenId, _data
+            ) returns (bytes4 response) {
+                if (response != IERC721Receiver(_to).onERC721Received.selector)
+                {
+                    revert ERC721ReceiverRejectedTokens();
+                }
+            } catch (bytes memory reason) {
+                if (reason.length == 0) {
+                    revert ERC721TransferToNonERC721ReceiverImplementer();
+                } else {
+                    assembly {
+                        revert(add(32, reason), mload(reason))
+                    }
+                }
+            }
+        }
+    }
+
+    /*//////////////////////////////////////////////////////////////
+                              ERC165 LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @inheritdoc IVotingEscrow
+    function supportsInterface(bytes4 _interfaceID)
+        external
+        view
+        returns (bool)
+    {
+        return supportedInterfaces[_interfaceID];
+    }
+
+    /*//////////////////////////////////////////////////////////////
+                        INTERNAL MINT/BURN LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @inheritdoc IVotingEscrow
+    mapping(address => mapping(uint256 => uint256)) public ownerToNFTokenIdList;
+
+    /// @dev Mapping from NFT ID to index of owner
+    mapping(uint256 => uint256) internal tokenToOwnerIndex;
+
+    /// @dev Add a NFT to an index mapping to a given address
+    /// @param _to address of the receiver
+    /// @param _tokenId uint ID Of the token to be added
+    function _addTokenToOwnerList(address _to, uint256 _tokenId) internal {
+        uint256 currentCount = ownerToNFTokenCount[_to];
+
+        ownerToNFTokenIdList[_to][currentCount] = _tokenId;
+        tokenToOwnerIndex[_tokenId] = currentCount;
+    }
+
+    /// @dev Add a NFT to a given address
+    ///      Throws if `_tokenId` is owned by someone.
+    function _addTokenTo(address _to, uint256 _tokenId) internal {
+        // Throws if `_tokenId` is owned by someone
+        assert(_ownerOf(_tokenId) == address(0));
+        // Change the owner
+        idToOwner[_tokenId] = _to;
+        // Update owner token index tracking
+        _addTokenToOwnerList(_to, _tokenId);
+        // Change count tracking
+        ownerToNFTokenCount[_to] += 1;
+    }
+
+    /// @dev Function to mint tokens
+    ///      Throws if `_to` is zero address.
+    ///      Throws if `_tokenId` is owned by someone.
+    /// @param _to The address that will receive the minted tokens.
+    /// @param _tokenId The token id to mint.
+    /// @return A boolean that indicates if the operation was successful.
+    function _mint(address _to, uint256 _tokenId) internal returns (bool) {
+        // Throws if `_to` is zero address
+        assert(_to != address(0));
+        // Add NFT. Throws if `_tokenId` is owned by someone
+        _addTokenTo(_to, _tokenId);
+        // Update voting checkpoints
+        _checkpointDelegator(_tokenId, 0, _to);
+        emit Transfer(address(0), _to, _tokenId);
+        return true;
+    }
+
+    /// @dev Remove a NFT from an index mapping to a given address
+    /// @param _from address of the sender
+    /// @param _tokenId uint ID Of the token to be removed
+    function _removeTokenFromOwnerList(address _from, uint256 _tokenId)
+        internal
+    {
+        // Delete
+        uint256 currentCount = ownerToNFTokenCount[_from] - 1;
+        uint256 currentIndex = tokenToOwnerIndex[_tokenId];
+
+        if (currentCount == currentIndex) {
+            // update ownerToNFTokenIdList
+            ownerToNFTokenIdList[_from][currentCount] = 0;
+            // update tokenToOwnerIndex
+            tokenToOwnerIndex[_tokenId] = 0;
+        } else {
+            uint256 lastTokenId = ownerToNFTokenIdList[_from][currentCount];
+
+            // Add
+            // update ownerToNFTokenIdList
+            ownerToNFTokenIdList[_from][currentIndex] = lastTokenId;
+            // update tokenToOwnerIndex
+            tokenToOwnerIndex[lastTokenId] = currentIndex;
+
+            // Delete
+            // update ownerToNFTokenIdList
+            ownerToNFTokenIdList[_from][currentCount] = 0;
+            // update tokenToOwnerIndex
+            tokenToOwnerIndex[_tokenId] = 0;
+        }
+    }
+
+    /// @dev Remove a NFT from a given address
+    ///      Throws if `_from` is not the current owner.
+    function _removeTokenFrom(address _from, uint256 _tokenId) internal {
+        // Throws if `_from` is not the current owner
+        assert(_ownerOf(_tokenId) == _from);
+        // Change the owner
+        idToOwner[_tokenId] = address(0);
+        // Update owner token index tracking
+        _removeTokenFromOwnerList(_from, _tokenId);
+        // Change count tracking
+        ownerToNFTokenCount[_from] -= 1;
+    }
+
+    /// @dev Must be called prior to updating `LockedBalance`
+    function _burn(uint256 _tokenId) internal {
+        if (!_isApprovedOrOwner(msg.sender, _tokenId)) {
+            revert NotApprovedOrOwner();
+        }
+        address owner = _ownerOf(_tokenId);
+
+        // Clear approval
+        delete idToApprovals[_tokenId];
+        // Update voting checkpoints
+        _checkpointDelegator(_tokenId, 0, address(0));
+        // Remove token
+        _removeTokenFrom(owner, _tokenId);
+        emit Transfer(owner, address(0), _tokenId);
+    }
+
+    /*//////////////////////////////////////////////////////////////
+                             ESCROW STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    uint256 internal constant WEEK = 1 weeks;
+    uint256 internal constant MAXTIME = 4 * 365 * 86400;
+    int128 internal constant iMAXTIME = 4 * 365 * 86400;
+    uint256 internal constant MULTIPLIER = 1 ether;
+
+    /// @inheritdoc IVotingEscrow
+    uint256 public epoch;
+    /// @inheritdoc IVotingEscrow
+    uint256 public supply;
+
+    mapping(uint256 => LockedBalance) internal _locked;
+    mapping(uint256 => UserPoint[1000000000]) internal _userPointHistory;
+    mapping(uint256 => uint256) public userPointEpoch;
+    /// @inheritdoc IVotingEscrow
+    mapping(uint256 => int128) public slopeChanges;
+    /// @inheritdoc IVotingEscrow
+    mapping(address => bool) public canSplit;
+    /// @inheritdoc IVotingEscrow
+    uint256 public permanentLockBalance;
+
+    /// @inheritdoc IVotingEscrow
+    function locked(uint256 _tokenId)
+        external
+        view
+        returns (LockedBalance memory)
+    {
+        return _locked[_tokenId];
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function userPointHistory(uint256 _tokenId, uint256 _loc)
+        external
+        view
+        returns (UserPoint memory)
+    {
+        return _userPointHistory[_tokenId][_loc];
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function pointHistory(uint256 _loc)
+        external
+        view
+        returns (GlobalPoint memory)
+    {
+        return _pointHistory[_loc];
+    }
+
+    /*//////////////////////////////////////////////////////////////
+                              ESCROW LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @notice Record global and per-user data to checkpoints. Used by VotingEscrow system.
+    /// @param _tokenId NFT token ID. No user checkpoint if 0
+    /// @param _oldLocked Pevious locked amount / end lock time for the user
+    /// @param _newLocked New locked amount / end lock time for the user
+    function _checkpoint(
+        uint256 _tokenId,
+        LockedBalance memory _oldLocked,
+        LockedBalance memory _newLocked
+    ) internal {
+        UserPoint memory uOld;
+        UserPoint memory uNew;
+        int128 oldDslope = 0;
+        int128 newDslope = 0;
+        uint256 _epoch = epoch;
+
+        if (_tokenId != 0) {
+            uNew.permanent =
+                _newLocked.isPermanent ? _newLocked.amount.toUint256() : 0;
+            // Calculate slopes and biases
+            // Kept at zero when they have to
+            if (_oldLocked.end > block.timestamp && _oldLocked.amount > 0) {
+                uOld.slope = _oldLocked.amount / iMAXTIME;
+                uOld.bias =
+                    uOld.slope * (_oldLocked.end - block.timestamp).toInt128();
+            }
+            if (_newLocked.end > block.timestamp && _newLocked.amount > 0) {
+                uNew.slope = _newLocked.amount / iMAXTIME;
+                uNew.bias =
+                    uNew.slope * (_newLocked.end - block.timestamp).toInt128();
+            }
+
+            // Read values of scheduled changes in the slope
+            // _oldLocked.end can be in the past and in the future
+            // _newLocked.end can ONLY by in the FUTURE unless everything expired: than zeros
+            oldDslope = slopeChanges[_oldLocked.end];
+            if (_newLocked.end != 0) {
+                if (_newLocked.end == _oldLocked.end) {
+                    newDslope = oldDslope;
+                } else {
+                    newDslope = slopeChanges[_newLocked.end];
+                }
+            }
+        }
+
+        GlobalPoint memory lastPoint = GlobalPoint({
+            bias: 0,
+            slope: 0,
+            ts: block.timestamp,
+            blk: block.number,
+            permanentLockBalance: 0
+        });
+        if (_epoch > 0) {
+            lastPoint = _pointHistory[_epoch];
+        }
+        uint256 lastCheckpoint = lastPoint.ts;
+        // initialLastPoint is used for extrapolation to calculate block number
+        // (approximately, for *At methods) and save them
+        // as we cannot figure that out exactly from inside the contract
+        GlobalPoint memory initialLastPoint = GlobalPoint({
+            bias: lastPoint.bias,
+            slope: lastPoint.slope,
+            ts: lastPoint.ts,
+            blk: lastPoint.blk,
+            permanentLockBalance: lastPoint.permanentLockBalance
+        });
+        uint256 blockSlope = 0; // dblock/dt
+        if (block.timestamp > lastPoint.ts) {
+            blockSlope = (MULTIPLIER * (block.number - lastPoint.blk))
+                / (block.timestamp - lastPoint.ts);
+        }
+        // If last point is already recorded in this block, slope=0
+        // But that's ok b/c we know the block in such case
+
+        // Go over weeks to fill history and calculate what the current point is
+        {
+            uint256 t_i = (lastCheckpoint / WEEK) * WEEK;
+            for (uint256 i = 0; i < 255; ++i) {
+                // Hopefully it won't happen that this won't get used in 5 years!
+                // If it does, users will be able to withdraw but vote weight will be broken
+                t_i += WEEK; // Initial value of t_i is always larger than the ts of the last point
+                int128 d_slope = 0;
+                if (t_i > block.timestamp) {
+                    t_i = block.timestamp;
+                } else {
+                    d_slope = slopeChanges[t_i];
+                }
+                lastPoint.bias -=
+                    lastPoint.slope * (t_i - lastCheckpoint).toInt128();
+                lastPoint.slope += d_slope;
+                if (lastPoint.bias < 0) {
+                    // This can happen
+                    lastPoint.bias = 0;
+                }
+                if (lastPoint.slope < 0) {
+                    // This cannot happen - just in case
+                    lastPoint.slope = 0;
+                }
+                lastCheckpoint = t_i;
+                lastPoint.ts = t_i;
+                lastPoint.blk = initialLastPoint.blk
+                    + (blockSlope * (t_i - initialLastPoint.ts)) / MULTIPLIER;
+                _epoch += 1;
+                if (t_i == block.timestamp) {
+                    lastPoint.blk = block.number;
+                    break;
+                } else {
+                    _pointHistory[_epoch] = lastPoint;
+                }
+            }
+        }
+
+        if (_tokenId != 0) {
+            // If last point was in this block, the slope change has been applied already
+            // But in such case we have 0 slope(s)
+            lastPoint.slope += (uNew.slope - uOld.slope);
+            lastPoint.bias += (uNew.bias - uOld.bias);
+            if (lastPoint.slope < 0) {
+                lastPoint.slope = 0;
+            }
+            if (lastPoint.bias < 0) {
+                lastPoint.bias = 0;
+            }
+            lastPoint.permanentLockBalance = permanentLockBalance;
+        }
+
+        // If timestamp of last global point is the same, overwrite the last global point
+        // Else record the new global point into history
+        // Exclude epoch 0 (note: _epoch is always >= 1, see above)
+        // Two possible outcomes:
+        // Missing global checkpoints in prior weeks. In this case, _epoch = epoch + x, where x > 1
+        // No missing global checkpoints, but timestamp != block.timestamp. Create new checkpoint.
+        // No missing global checkpoints, but timestamp == block.timestamp. Overwrite last checkpoint.
+        if (_epoch != 1 && _pointHistory[_epoch - 1].ts == block.timestamp) {
+            // _epoch = epoch + 1, so we do not increment epoch
+            _pointHistory[_epoch - 1] = lastPoint;
+        } else {
+            // more than one global point may have been written, so we update epoch
+            epoch = _epoch;
+            _pointHistory[_epoch] = lastPoint;
+        }
+
+        if (_tokenId != 0) {
+            // Schedule the slope changes (slope is going down)
+            // We subtract new_user_slope from [_newLocked.end]
+            // and add old_user_slope to [_oldLocked.end]
+            if (_oldLocked.end > block.timestamp) {
+                // oldDslope was <something> - uOld.slope, so we cancel that
+                oldDslope += uOld.slope;
+                if (_newLocked.end == _oldLocked.end) {
+                    oldDslope -= uNew.slope; // It was a new deposit, not extension
+                }
+                slopeChanges[_oldLocked.end] = oldDslope;
+            }
+
+            if (_newLocked.end > block.timestamp) {
+                // update slope if new lock is greater than old lock and is not permanent or if old lock is permanent
+                if ((_newLocked.end > _oldLocked.end)) {
+                    newDslope -= uNew.slope; // old slope disappeared at this point
+                    slopeChanges[_newLocked.end] = newDslope;
+                }
+                // else: we recorded it already in oldDslope
+            }
+            // If timestamp of last user point is the same, overwrite the last user point
+            // Else record the new user point into history
+            // Exclude epoch 0
+            uNew.ts = block.timestamp;
+            uNew.blk = block.number;
+            uint256 userEpoch = userPointEpoch[_tokenId];
+            if (
+                userEpoch != 0
+                    && _userPointHistory[_tokenId][userEpoch].ts == block.timestamp
+            ) {
+                _userPointHistory[_tokenId][userEpoch] = uNew;
+            } else {
+                userPointEpoch[_tokenId] = ++userEpoch;
+                _userPointHistory[_tokenId][userEpoch] = uNew;
+            }
+        }
+    }
+
+    /// @notice Deposit and lock tokens for a user
+    /// @param _tokenId NFT that holds lock
+    /// @param _value Amount to deposit
+    /// @param _unlockTime New time when to unlock the tokens, or 0 if unchanged
+    /// @param _oldLocked Previous locked amount / timestamp
+    /// @param _depositType The type of deposit
+    function _depositFor(
+        uint256 _tokenId,
+        uint256 _value,
+        uint256 _unlockTime,
+        LockedBalance memory _oldLocked,
+        DepositType _depositType
+    ) internal {
+        uint256 supplyBefore = supply;
+        supply = supplyBefore + _value;
+
+        // Set newLocked to _oldLocked without mangling memory
+        LockedBalance memory newLocked;
+        (newLocked.amount, newLocked.end, newLocked.isPermanent) =
+            (_oldLocked.amount, _oldLocked.end, _oldLocked.isPermanent);
+
+        // Adding to existing lock, or if a lock is expired - creating a new one
+        newLocked.amount += _value.toInt128();
+        if (_unlockTime != 0) {
+            newLocked.end = _unlockTime;
+        }
+        _locked[_tokenId] = newLocked;
+
+        // Possibilities:
+        // Both _oldLocked.end could be current or expired (>/< block.timestamp)
+        // or if the lock is a permanent lock, then _oldLocked.end == 0
+        // value == 0 (extend lock) or value > 0 (add to lock or extend lock)
+        // newLocked.end > block.timestamp (always)
+        _checkpoint(_tokenId, _oldLocked, newLocked);
+
+        if (_value != 0) {
+            ERC20(token).safeTransferFrom(msg.sender, address(this), _value);
+        }
+
+        emit Deposit(
+            msg.sender,
+            _tokenId,
+            _depositType,
+            _value,
+            newLocked.end,
+            block.timestamp
+        );
+        emit Supply(supplyBefore, supplyBefore + _value);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function checkpoint() external nonReentrant {
+        _checkpoint(0, LockedBalance(0, 0, false), LockedBalance(0, 0, false));
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function depositFor(uint256 _tokenId, uint256 _value)
+        external
+        nonReentrant
+    {
+        if (
+            escrowType[_tokenId] == EscrowType.MANAGED
+                && msg.sender != distributor
+        ) revert NotDistributor();
+        _increaseAmountFor(_tokenId, _value, DepositType.DEPOSIT_FOR_TYPE);
+    }
+
+    /// @dev Deposit `_value` tokens for `_to` and lock for `_lockDuration`
+    /// @param _value Amount to deposit
+    /// @param _lockDuration Number of seconds to lock tokens for (rounded down to nearest week)
+    /// @param _to Address to deposit
+    function _createLock(uint256 _value, uint256 _lockDuration, address _to)
+        internal
+        returns (uint256)
+    {
+        uint256 unlockTime = ((block.timestamp + _lockDuration) / WEEK) * WEEK; // Locktime is rounded down to weeks
+
+        if (_value == 0) revert ZeroAmount();
+        if (unlockTime <= block.timestamp) revert LockDurationNotInFuture();
+        if (unlockTime > block.timestamp + MAXTIME) {
+            revert LockDurationTooLong();
+        }
+
+        uint256 _tokenId = ++tokenId;
+        _mint(_to, _tokenId);
+
+        _depositFor(
+            _tokenId,
+            _value,
+            unlockTime,
+            _locked[_tokenId],
+            DepositType.CREATE_LOCK_TYPE
+        );
+        return _tokenId;
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function createLock(uint256 _value, uint256 _lockDuration)
+        external
+        nonReentrant
+        returns (uint256)
+    {
+        return _createLock(_value, _lockDuration, msg.sender);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function createLockFor(uint256 _value, uint256 _lockDuration, address _to)
+        external
+        nonReentrant
+        returns (uint256)
+    {
+        return _createLock(_value, _lockDuration, _to);
+    }
+
+    function _increaseAmountFor(
+        uint256 _tokenId,
+        uint256 _value,
+        DepositType _depositType
+    ) internal {
+        EscrowType _escrowType = escrowType[_tokenId];
+        if (_escrowType == EscrowType.LOCKED) revert NotManagedOrNormalNFT();
+
+        LockedBalance memory oldLocked = _locked[_tokenId];
+
+        if (_value == 0) revert ZeroAmount();
+        if (oldLocked.amount <= 0) revert NoLockFound();
+        if (oldLocked.end <= block.timestamp && !oldLocked.isPermanent) {
+            revert LockExpired();
+        }
+
+        if (oldLocked.isPermanent) permanentLockBalance += _value;
+        _checkpointDelegatee(_delegates[_tokenId], _value, true);
+        _depositFor(_tokenId, _value, 0, oldLocked, _depositType);
+
+        emit MetadataUpdate(_tokenId);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function increaseAmount(uint256 _tokenId, uint256 _value)
+        external
+        nonReentrant
+    {
+        if (!_isApprovedOrOwner(msg.sender, _tokenId)) {
+            revert NotApprovedOrOwner();
+        }
+        _increaseAmountFor(_tokenId, _value, DepositType.INCREASE_LOCK_AMOUNT);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function increaseUnlockTime(uint256 _tokenId, uint256 _lockDuration)
+        external
+        nonReentrant
+    {
+        if (!_isApprovedOrOwner(msg.sender, _tokenId)) {
+            revert NotApprovedOrOwner();
+        }
+        if (escrowType[_tokenId] != EscrowType.NORMAL) revert NotNormalNFT();
+
+        LockedBalance memory oldLocked = _locked[_tokenId];
+        if (oldLocked.isPermanent) revert PermanentLock();
+        uint256 unlockTime = ((block.timestamp + _lockDuration) / WEEK) * WEEK; // Locktime is rounded down to weeks
+
+        if (oldLocked.end <= block.timestamp) revert LockExpired();
+        if (oldLocked.amount <= 0) revert NoLockFound();
+        if (unlockTime <= oldLocked.end) revert LockDurationNotInFuture();
+        if (unlockTime > block.timestamp + MAXTIME) {
+            revert LockDurationTooLong();
+        }
+
+        _depositFor(
+            _tokenId, 0, unlockTime, oldLocked, DepositType.INCREASE_UNLOCK_TIME
+        );
+
+        emit MetadataUpdate(_tokenId);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function withdraw(uint256 _tokenId) external nonReentrant {
+        if (!_isApprovedOrOwner(msg.sender, _tokenId)) {
+            revert NotApprovedOrOwner();
+        }
+        if (voted[_tokenId]) revert AlreadyVoted();
+        if (escrowType[_tokenId] != EscrowType.NORMAL) revert NotNormalNFT();
+
+        LockedBalance memory oldLocked = _locked[_tokenId];
+        if (oldLocked.isPermanent) revert PermanentLock();
+        if (block.timestamp < oldLocked.end) revert LockNotExpired();
+        uint256 value = oldLocked.amount.toUint256();
+
+        // Burn the NFT
+        _burn(_tokenId);
+        _locked[_tokenId] = LockedBalance(0, 0, false);
+        uint256 supplyBefore = supply;
+        supply = supplyBefore - value;
+
+        // oldLocked can have either expired <= timestamp or zero end
+        // oldLocked has only 0 end
+        // Both can have >= 0 amount
+        _checkpoint(_tokenId, oldLocked, LockedBalance(0, 0, false));
+
+        ERC20(token).safeTransfer(msg.sender, value);
+
+        emit Withdraw(msg.sender, _tokenId, value, block.timestamp);
+        emit Supply(supplyBefore, supplyBefore - value);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function merge(uint256 _from, uint256 _to) external nonReentrant {
+        if (voted[_from]) revert AlreadyVoted();
+        if (escrowType[_from] != EscrowType.NORMAL) revert NotNormalNFT();
+        if (escrowType[_to] != EscrowType.NORMAL) revert NotNormalNFT();
+        if (_from == _to) revert SameNFT();
+        if (!_isApprovedOrOwner(msg.sender, _from)) revert NotApprovedOrOwner();
+        if (!_isApprovedOrOwner(msg.sender, _to)) revert NotApprovedOrOwner();
+        LockedBalance memory oldLockedTo = _locked[_to];
+        if (oldLockedTo.end <= block.timestamp && !oldLockedTo.isPermanent) {
+            revert LockExpired();
+        }
+
+        LockedBalance memory oldLockedFrom = _locked[_from];
+        if (oldLockedFrom.isPermanent) revert PermanentLock();
+        uint256 end = oldLockedFrom.end >= oldLockedTo.end
+            ? oldLockedFrom.end
+            : oldLockedTo.end;
+
+        _burn(_from);
+        _locked[_from] = LockedBalance(0, 0, false);
+        _checkpoint(_from, oldLockedFrom, LockedBalance(0, 0, false));
+
+        LockedBalance memory newLockedTo;
+        newLockedTo.amount = oldLockedTo.amount + oldLockedFrom.amount;
+        newLockedTo.isPermanent = oldLockedTo.isPermanent;
+        if (newLockedTo.isPermanent) {
+            permanentLockBalance += oldLockedFrom.amount.toUint256();
+        } else {
+            newLockedTo.end = end;
+        }
+        _checkpointDelegatee(
+            _delegates[_to], oldLockedFrom.amount.toUint256(), true
+        );
+        _checkpoint(_to, oldLockedTo, newLockedTo);
+        _locked[_to] = newLockedTo;
+
+        emit Merge(
+            msg.sender,
+            _from,
+            _to,
+            oldLockedFrom.amount.toUint256(),
+            oldLockedTo.amount.toUint256(),
+            newLockedTo.amount.toUint256(),
+            newLockedTo.end,
+            block.timestamp
+        );
+        emit MetadataUpdate(_to);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function split(uint256 _from, uint256 _amount)
+        external
+        nonReentrant
+        returns (uint256 _tokenId1, uint256 _tokenId2)
+    {
+        address owner = _ownerOf(_from);
+        if (owner == address(0)) revert SplitNoOwner();
+        if (!canSplit[owner] && !canSplit[address(0)]) revert SplitNotAllowed();
+        if (escrowType[_from] != EscrowType.NORMAL) revert NotNormalNFT();
+        if (voted[_from]) revert AlreadyVoted();
+        if (!_isApprovedOrOwner(msg.sender, _from)) revert NotApprovedOrOwner();
+        LockedBalance memory newLocked = _locked[_from];
+        if (newLocked.end <= block.timestamp && !newLocked.isPermanent) {
+            revert LockExpired();
+        }
+        int128 _splitAmount = _amount.toInt128();
+        if (_splitAmount == 0) revert ZeroAmount();
+        if (newLocked.amount <= _splitAmount) revert AmountTooBig();
+
+        // Zero out and burn old veNFT
+        _burn(_from);
+        _locked[_from] = LockedBalance(0, 0, false);
+        _checkpoint(_from, newLocked, LockedBalance(0, 0, false));
+
+        // Create new veNFT using old balance - amount
+        newLocked.amount -= _splitAmount;
+        _tokenId1 = _createSplitNFT(owner, newLocked);
+
+        // Create new veNFT using amount
+        newLocked.amount = _splitAmount;
+        _tokenId2 = _createSplitNFT(owner, newLocked);
+
+        emit Split(
+            _from,
+            _tokenId1,
+            _tokenId2,
+            msg.sender,
+            _locked[_tokenId1].amount.toUint256(),
+            _splitAmount.toUint256(),
+            newLocked.end,
+            block.timestamp
+        );
+    }
+
+    function _createSplitNFT(address _to, LockedBalance memory _newLocked)
+        private
+        returns (uint256 _tokenId)
+    {
+        _tokenId = ++tokenId;
+        _locked[_tokenId] = _newLocked;
+        _checkpoint(_tokenId, LockedBalance(0, 0, false), _newLocked);
+        _mint(_to, _tokenId);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function toggleSplit(address _account, bool _bool) external {
+        if (!infrared.hasRole(infrared.GOVERNANCE_ROLE(), msg.sender)) {
+            revert NotGovernor();
+        }
+        canSplit[_account] = _bool;
+        emit ToggleSplit(_account, _bool);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function lockPermanent(uint256 _tokenId) external {
+        if (!_isApprovedOrOwner(msg.sender, _tokenId)) {
+            revert NotApprovedOrOwner();
+        }
+        if (escrowType[_tokenId] != EscrowType.NORMAL) revert NotNormalNFT();
+        LockedBalance memory _newLocked = _locked[_tokenId];
+        if (_newLocked.isPermanent) revert PermanentLock();
+        if (_newLocked.end <= block.timestamp) revert LockExpired();
+        if (_newLocked.amount <= 0) revert NoLockFound();
+
+        uint256 _amount = _newLocked.amount.toUint256();
+        permanentLockBalance += _amount;
+        _newLocked.end = 0;
+        _newLocked.isPermanent = true;
+        _checkpoint(_tokenId, _locked[_tokenId], _newLocked);
+        _locked[_tokenId] = _newLocked;
+
+        emit LockPermanent(msg.sender, _tokenId, _amount, block.timestamp);
+        emit MetadataUpdate(_tokenId);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function unlockPermanent(uint256 _tokenId) external {
+        if (!_isApprovedOrOwner(msg.sender, _tokenId)) {
+            revert NotApprovedOrOwner();
+        }
+        if (escrowType[_tokenId] != EscrowType.NORMAL) revert NotNormalNFT();
+        if (voted[_tokenId]) revert AlreadyVoted();
+        LockedBalance memory _newLocked = _locked[_tokenId];
+        if (!_newLocked.isPermanent) revert NotPermanentLock();
+
+        uint256 _amount = _newLocked.amount.toUint256();
+        permanentLockBalance -= _amount;
+        _newLocked.end = ((block.timestamp + MAXTIME) / WEEK) * WEEK;
+        _newLocked.isPermanent = false;
+        _delegate(_tokenId, 0);
+        _checkpoint(_tokenId, _locked[_tokenId], _newLocked);
+        _locked[_tokenId] = _newLocked;
+
+        emit UnlockPermanent(msg.sender, _tokenId, _amount, block.timestamp);
+        emit MetadataUpdate(_tokenId);
+    }
+
+    /*///////////////////////////////////////////////////////////////
+                           GAUGE VOTING STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    function _balanceOfNFTAt(uint256 _tokenId, uint256 _t)
+        internal
+        view
+        returns (uint256)
+    {
+        // flash loan protection
+        if (ownershipChange[_tokenId] == block.number) return 0;
+        return BalanceLogicLibrary.balanceOfNFTAt(
+            userPointEpoch, _userPointHistory, _tokenId, _t
+        );
+    }
+
+    function _supplyAt(uint256 _timestamp) internal view returns (uint256) {
+        return BalanceLogicLibrary.supplyAt(
+            slopeChanges, _pointHistory, epoch, _timestamp
+        );
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function balanceOfNFT(uint256 _tokenId) public view returns (uint256) {
+        return _balanceOfNFTAt(_tokenId, block.timestamp);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function balanceOfNFTAt(uint256 _tokenId, uint256 _t)
+        external
+        view
+        returns (uint256)
+    {
+        return _balanceOfNFTAt(_tokenId, _t);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function totalSupply() external view returns (uint256) {
+        return _supplyAt(block.timestamp);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function totalSupplyAt(uint256 _timestamp)
+        external
+        view
+        returns (uint256)
+    {
+        return _supplyAt(_timestamp);
+    }
+
+    /*///////////////////////////////////////////////////////////////
+                            GAUGE VOTING LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @inheritdoc IVotingEscrow
+    mapping(uint256 => bool) public voted;
+
+    /// @inheritdoc IVotingEscrow
+    function setVoterAndDistributor(address _voter, address _distributor)
+        external
+    {
+        if (_voter == address(0) || _distributor == address(0)) {
+            revert ZeroAddress();
+        }
+        if (!infrared.hasRole(infrared.GOVERNANCE_ROLE(), msg.sender)) {
+            revert NotGovernor();
+        }
+        voter = _voter;
+        distributor = _distributor;
+        emit VoterAndDistributorSet(_voter, _distributor);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function voting(uint256 _tokenId, bool _voted) external {
+        if (msg.sender != voter) revert NotVoter();
+        voted[_tokenId] = _voted;
+    }
+
+    /*///////////////////////////////////////////////////////////////
+                            DAO VOTING STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    /// @notice The EIP-712 typehash for the contract's domain
+    bytes32 public constant DOMAIN_TYPEHASH = keccak256(
+        "EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"
+    );
+
+    /// @notice The EIP-712 typehash for the delegation struct used by the contract
+    bytes32 public constant DELEGATION_TYPEHASH = keccak256(
+        "Delegation(uint256 delegator,uint256 delegatee,uint256 nonce,uint256 expiry)"
+    );
+
+    /// @notice A record of each accounts delegate
+    mapping(uint256 => uint256) private _delegates;
+
+    /// @notice A record of delegated token checkpoints for each tokenId, by index
+    mapping(uint256 => mapping(uint48 => Checkpoint)) private _checkpoints;
+
+    /// @inheritdoc IVotingEscrow
+    mapping(uint256 => uint48) public numCheckpoints;
+
+    /// @inheritdoc IVotingEscrow
+    mapping(address => uint256) public nonces;
+
+    /// @inheritdoc IVotingEscrow
+    function delegates(uint256 delegator) external view returns (uint256) {
+        return _delegates[delegator];
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function checkpoints(uint256 _tokenId, uint48 _index)
+        external
+        view
+        returns (Checkpoint memory)
+    {
+        return _checkpoints[_tokenId][_index];
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function getPastVotes(
+        address _account,
+        uint256 _tokenId,
+        uint256 _timestamp
+    ) external view returns (uint256) {
+        return DelegationLogicLibrary.getPastVotes(
+            numCheckpoints, _checkpoints, _account, _tokenId, _timestamp
+        );
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function getPastTotalSupply(uint256 _timestamp)
+        external
+        view
+        returns (uint256)
+    {
+        return _supplyAt(_timestamp);
+    }
+
+    /*///////////////////////////////////////////////////////////////
+                             DAO VOTING LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    function _checkpointDelegator(
+        uint256 _delegator,
+        uint256 _delegatee,
+        address _owner
+    ) internal {
+        DelegationLogicLibrary.checkpointDelegator(
+            _locked,
+            numCheckpoints,
+            _checkpoints,
+            _delegates,
+            _delegator,
+            _delegatee,
+            _owner
+        );
+    }
+
+    function _checkpointDelegatee(
+        uint256 _delegatee,
+        uint256 balance_,
+        bool _increase
+    ) internal {
+        DelegationLogicLibrary.checkpointDelegatee(
+            numCheckpoints, _checkpoints, _delegatee, balance_, _increase
+        );
+    }
+
+    /// @notice Record user delegation checkpoints. Used by voting system.
+    /// @dev Skips delegation if already delegated to `delegatee`.
+    function _delegate(uint256 _delegator, uint256 _delegatee) internal {
+        LockedBalance memory delegateLocked = _locked[_delegator];
+        if (!delegateLocked.isPermanent) revert NotPermanentLock();
+        if (_delegatee != 0 && _ownerOf(_delegatee) == address(0)) {
+            revert NonExistentToken();
+        }
+        if (ownershipChange[_delegator] == block.number) {
+            revert OwnershipChange();
+        }
+        if (_delegatee == _delegator) _delegatee = 0;
+        uint256 currentDelegate = _delegates[_delegator];
+        if (currentDelegate == _delegatee) return;
+
+        uint256 delegatedBalance = delegateLocked.amount.toUint256();
+        _checkpointDelegator(_delegator, _delegatee, _ownerOf(_delegator));
+        _checkpointDelegatee(_delegatee, delegatedBalance, true);
+
+        emit DelegateChanged(msg.sender, currentDelegate, _delegatee);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function delegate(uint256 delegator, uint256 delegatee) external {
+        if (!_isApprovedOrOwner(msg.sender, delegator)) {
+            revert NotApprovedOrOwner();
+        }
+        return _delegate(delegator, delegatee);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function delegateBySig(
+        uint256 delegator,
+        uint256 delegatee,
+        uint256 nonce,
+        uint256 expiry,
+        uint8 v,
+        bytes32 r,
+        bytes32 s
+    ) external {
+        // EIP-2 still allows signature malleability for ecrecover(). Remove this possibility and make the signature
+        // unique. Appendix F in the Ethereum Yellow paper (https://ethereum.github.io/yellowpaper/paper.pdf), defines
+        // the valid range for s in (301): 0 < s < secp256k1n ÷ 2 + 1, and for v in (302): v ∈ {27, 28}. Most
+        // signatures from current libraries generate a unique signature with an s-value in the lower half order.
+        //
+        // If your library generates malleable signatures, such as s-values in the upper range, calculate a new s-value
+        // with 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 - s1 and flip v from 27 to 28 or
+        // vice versa. If your library also generates signatures with 0/1 for v instead 27/28, add 27 to v to accept
+        // these malleable signatures as well.
+        if (
+            uint256(s)
+                > 0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF5D576E7357A4501DDFE92F46681B20A0
+        ) revert InvalidSignatureS();
+        bytes32 domainSeparator = keccak256(
+            abi.encode(
+                DOMAIN_TYPEHASH,
+                keccak256(bytes(name)),
+                keccak256(bytes(version)),
+                block.chainid,
+                address(this)
+            )
+        );
+        bytes32 structHash = keccak256(
+            abi.encode(DELEGATION_TYPEHASH, delegator, delegatee, nonce, expiry)
+        );
+        bytes32 digest =
+            keccak256(abi.encodePacked("\x19\x01", domainSeparator, structHash));
+        address signatory = ecrecover(digest, v, r, s);
+        if (!_isApprovedOrOwner(signatory, delegator)) {
+            revert NotApprovedOrOwner();
+        }
+        if (signatory == address(0)) revert InvalidSignature();
+        if (nonce != nonces[signatory]++) revert InvalidNonce();
+        if (block.timestamp > expiry) revert SignatureExpired();
+        return _delegate(delegator, delegatee);
+    }
+
+    /*//////////////////////////////////////////////////////////////
+                              ERC6372 LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @inheritdoc IVotingEscrow
+    function clock() external view returns (uint48) {
+        return uint48(block.timestamp);
+    }
+
+    /// @inheritdoc IVotingEscrow
+    function CLOCK_MODE() external pure returns (string memory) {
+        return "mode=timestamp";
+    }
+}
diff --git asrc/voting (온체인)/interfaces/IVeArtProxy.sol bsrc/voting (온체인)/interfaces/IVeArtProxy.sol
new file mode 100644
index 0000000..53d11e5
--- /dev/null
+++ bsrc/voting (온체인)/interfaces/IVeArtProxy.sol
@@ -0,0 +1,134 @@
+// SPDX-License-Identifier: BUSL-1.1
+pragma solidity ^0.8.0;
+
+interface IVeArtProxy {
+    /// @dev Art configuration
+    struct Config {
+        // NFT metadata variables
+        int256 _tokenId;
+        int256 _balanceOf;
+        int256 _lockedEnd;
+        int256 _lockedAmount;
+        // Line art variables
+        int256 shape;
+        uint256 palette;
+        int256 maxLines;
+        int256 dash;
+        // Randomness variables
+        int256 seed1;
+        int256 seed2;
+        int256 seed3;
+    }
+
+    /// @dev Individual line art path variables.
+    struct lineConfig {
+        bytes8 color;
+        uint256 stroke;
+        uint256 offset;
+        uint256 offsetHalf;
+        uint256 offsetDashSum;
+        uint256 pathLength;
+    }
+
+    /// @dev Represents an (x,y) coordinate in a line.
+    struct Point {
+        int256 x;
+        int256 y;
+    }
+
+    /// @notice Generate a SVG based on veNFT metadata
+    /// @param _tokenId Unique veNFT identifier
+    /// @return output SVG metadata as HTML tag
+    function tokenURI(uint256 _tokenId)
+        external
+        view
+        returns (string memory output);
+
+    /// @notice Generate only the foreground <path> elements of the line art for an NFT (excluding SVG header), for flexibility purposes.
+    /// @param _tokenId Unique veNFT identifier
+    /// @return output Encoded output of generateShape()
+    function lineArtPathsOnly(uint256 _tokenId)
+        external
+        view
+        returns (bytes memory output);
+
+    /// @notice Generate the master art config metadata for a veNFT
+    /// @param _tokenId Unique veNFT identifier
+    /// @return cfg Config struct
+    function generateConfig(uint256 _tokenId)
+        external
+        view
+        returns (Config memory cfg);
+
+    /// @notice Generate the points for two stripe lines based on the config generated for a veNFT
+    /// @param cfg Master art config metadata of a veNFT
+    /// @param l Number of line drawn
+    /// @return Line (x, y) coordinates of the drawn stripes
+    function twoStripes(Config memory cfg, int256 l)
+        external
+        pure
+        returns (Point[100] memory Line);
+
+    /// @notice Generate the points for circles based on the config generated for a veNFT
+    /// @param cfg Master art config metadata of a veNFT
+    /// @param l Number of circles drawn
+    /// @return Line (x, y) coordinates of the drawn circles
+    function circles(Config memory cfg, int256 l)
+        external
+        pure
+        returns (Point[100] memory Line);
+
+    /// @notice Generate the points for interlocking circles based on the config generated for a veNFT
+    /// @param cfg Master art config metadata of a veNFT
+    /// @param l Number of interlocking circles drawn
+    /// @return Line (x, y) coordinates of the drawn interlocking circles
+    function interlockingCircles(Config memory cfg, int256 l)
+        external
+        pure
+        returns (Point[100] memory Line);
+
+    /// @notice Generate the points for corners based on the config generated for a veNFT
+    /// @param cfg Master art config metadata of a veNFT
+    /// @param l Number of corners drawn
+    /// @return Line (x, y) coordinates of the drawn corners
+    function corners(Config memory cfg, int256 l)
+        external
+        pure
+        returns (Point[100] memory Line);
+
+    /// @notice Generate the points for a curve based on the config generated for a veNFT
+    /// @param cfg Master art config metadata of a veNFT
+    /// @param l Number of curve drawn
+    /// @return Line (x, y) coordinates of the drawn curve
+    function curves(Config memory cfg, int256 l)
+        external
+        pure
+        returns (Point[100] memory Line);
+
+    /// @notice Generate the points for a spiral based on the config generated for a veNFT
+    /// @param cfg Master art config metadata of a veNFT
+    /// @param l Number of spiral drawn
+    /// @return Line (x, y) coordinates of the drawn spiral
+    function spiral(Config memory cfg, int256 l)
+        external
+        pure
+        returns (Point[100] memory Line);
+
+    /// @notice Generate the points for an explosion based on the config generated for a veNFT
+    /// @param cfg Master art config metadata of a veNFT
+    /// @param l Number of explosion drawn
+    /// @return Line (x, y) coordinates of the drawn explosion
+    function explosion(Config memory cfg, int256 l)
+        external
+        pure
+        returns (Point[100] memory Line);
+
+    /// @notice Generate the points for a wormhole based on the config generated for a veNFT
+    /// @param cfg Master art config metadata of a veNFT
+    /// @param l Number of wormhole drawn
+    /// @return Line (x, y) coordinates of the drawn wormhole
+    function wormhole(Config memory cfg, int256 l)
+        external
+        pure
+        returns (Point[100] memory Line);
+}
diff --git asrc/voting (온체인)/interfaces/IVotes.sol bsrc/voting (온체인)/interfaces/IVotes.sol
new file mode 100644
index 0000000..b957ad9
--- /dev/null
+++ bsrc/voting (온체인)/interfaces/IVotes.sol
@@ -0,0 +1,67 @@
+// SPDX-License-Identifier: BUSL-1.1
+pragma solidity ^0.8.0;
+
+/// Modified IVotes interface for tokenId based voting
+interface IVotes {
+    /**
+     * @dev Emitted when an account changes their delegate.
+     */
+    event DelegateChanged(
+        address indexed delegator,
+        uint256 indexed fromDelegate,
+        uint256 indexed toDelegate
+    );
+
+    /**
+     * @dev Emitted when a token transfer or delegate change results in changes to a delegate's number of votes.
+     */
+    event DelegateVotesChanged(
+        address indexed delegate, uint256 previousBalance, uint256 newBalance
+    );
+
+    /**
+     * @dev Returns the amount of votes that `tokenId` had at a specific moment in the past.
+     *      If the account passed in is not the owner, returns 0.
+     */
+    function getPastVotes(address account, uint256 tokenId, uint256 timepoint)
+        external
+        view
+        returns (uint256);
+
+    /**
+     * @dev Returns the total supply of votes available at a specific moment in the past. If the `clock()` is
+     * configured to use block numbers, this will return the value the end of the corresponding block.
+     *
+     * NOTE: This value is the sum of all available votes, which is not necessarily the sum of all delegated votes.
+     * Votes that have not been delegated are still part of total supply, even though they would not participate in a
+     * vote.
+     */
+    function getPastTotalSupply(uint256 timepoint)
+        external
+        view
+        returns (uint256);
+
+    /**
+     * @dev Returns the delegate that `tokenId` has chosen. Can never be equal to the delegator's `tokenId`.
+     *      Returns 0 if not delegated.
+     */
+    function delegates(uint256 tokenId) external view returns (uint256);
+
+    /**
+     * @dev Delegates votes from the sender to `delegatee`.
+     */
+    function delegate(uint256 delegator, uint256 delegatee) external;
+
+    /**
+     * @dev Delegates votes from `delegator` to `delegatee`. Signer must own `delegator`.
+     */
+    function delegateBySig(
+        uint256 delegator,
+        uint256 delegatee,
+        uint256 nonce,
+        uint256 expiry,
+        uint8 v,
+        bytes32 r,
+        bytes32 s
+    ) external;
+}
diff --git asrc/voting (온체인)/interfaces/IVotingEscrow.sol bsrc/voting (온체인)/interfaces/IVotingEscrow.sol
new file mode 100644
index 0000000..96d233e
--- /dev/null
+++ bsrc/voting (온체인)/interfaces/IVotingEscrow.sol
@@ -0,0 +1,640 @@
+// SPDX-License-Identifier: MIT
+pragma solidity ^0.8.0;
+
+import {
+    IERC721,
+    IERC721Metadata
+} from "@openzeppelin/contracts/token/ERC721/extensions/IERC721Metadata.sol";
+import {IERC6372} from "@openzeppelin/contracts/interfaces/IERC6372.sol";
+import {IERC4906} from "@openzeppelin/contracts/interfaces/IERC4906.sol";
+import {IERC165} from "@openzeppelin/contracts/interfaces/IERC165.sol";
+import {IVotes} from "./IVotes.sol";
+import {IInfraredUpgradeable} from "src/interfaces/IInfraredUpgradeable.sol";
+
+interface IVotingEscrow is IVotes, IERC4906, IERC6372, IERC721Metadata {
+    /*//////////////////////////////////////////////////////////////
+                            STRUCTS/ENUMS
+    //////////////////////////////////////////////////////////////*/
+
+    /**
+     * @notice Represents a locked token balance in the voting escrow system
+     * @param amount The amount of tokens locked by the user
+     * @param end The expiration timestamp for the lock
+     * @param isPermanent Flag indicating if the lock is permanent
+     */
+    struct LockedBalance {
+        int128 amount;
+        uint256 end;
+        bool isPermanent;
+    }
+
+    /**
+     * @notice Represents a snapshot of a user's voting power at a given point
+     * @param bias Voting power, decaying over time
+     * @param slope Rate of decay of voting power
+     * @param ts Timestamp of this snapshot
+     * @param blk Block number of this snapshot
+     * @param permanent Amount locked permanently without decay
+     */
+    struct UserPoint {
+        int128 bias;
+        int128 slope; // # -dweight / dt
+        uint256 ts;
+        uint256 blk; // block
+        uint256 permanent;
+    }
+
+    /**
+     * @notice Tracks cumulative voting power and its decay across all users
+     * @param bias Total voting power, decaying over time
+     * @param slope Global decay rate of voting power
+     * @param ts Timestamp of this global checkpoint
+     * @param blk Block number of this global checkpoint
+     * @param permanentLockBalance Cumulative balance of permanently locked tokens
+     */
+    struct GlobalPoint {
+        int128 bias;
+        int128 slope; // # -dweight / dt
+        uint256 ts;
+        uint256 blk; // block
+        uint256 permanentLockBalance;
+    }
+
+    /**
+     * @notice Snapshot of delegated voting weights at a particular timestamp
+     * @param fromTimestamp Timestamp when the delegation was made
+     * @param owner Address of the NFT owner
+     * @param delegatedBalance Balance that has been delegated
+     * @param delegatee Address receiving the delegated voting power
+     */
+    struct Checkpoint {
+        uint256 fromTimestamp;
+        address owner;
+        uint256 delegatedBalance;
+        uint256 delegatee;
+    }
+
+    /**
+     * @notice Types of deposits supported in the voting escrow contract
+     * @param DEPOSIT_FOR_TYPE Deposit for another address
+     * @param CREATE_LOCK_TYPE Create a new lock
+     * @param INCREASE_LOCK_AMOUNT Increase tokens in an existing lock
+     * @param INCREASE_UNLOCK_TIME Extend the duration of an existing lock
+     */
+    enum DepositType {
+        DEPOSIT_FOR_TYPE,
+        CREATE_LOCK_TYPE,
+        INCREASE_LOCK_AMOUNT,
+        INCREASE_UNLOCK_TIME
+    }
+
+    /**
+     * @notice Specifies the type of voting escrow NFT (veNFT)
+     * @param NORMAL Standard veNFT
+     * @param LOCKED veNFT locked within a managed veNFT
+     * @param MANAGED veNFT capable of accepting deposits from NORMAL veNFTs
+     */
+    enum EscrowType {
+        NORMAL,
+        LOCKED,
+        MANAGED
+    }
+
+    error AlreadyVoted();
+    error AmountTooBig();
+    error ERC721ReceiverRejectedTokens();
+    error ERC721TransferToNonERC721ReceiverImplementer();
+    error InvalidNonce();
+    error InvalidSignature();
+    error InvalidSignatureS();
+    error InvalidManagedNFTId();
+    error LockDurationNotInFuture();
+    error LockDurationTooLong();
+    error LockExpired();
+    error LockNotExpired();
+    error NoLockFound();
+    error NonExistentToken();
+    error NotApprovedOrOwner();
+    error NotDistributor();
+    error NotEmergencyCouncilOrGovernor();
+    error NotGovernor();
+    error NotGovernorOrManager();
+    error NotManagedNFT();
+    error NotManagedOrNormalNFT();
+    error NotLockedNFT();
+    error NotNormalNFT();
+    error NotPermanentLock();
+    error NotOwner();
+    error NotTeam();
+    error NotVoter();
+    error OwnershipChange();
+    error PermanentLock();
+    error SameAddress();
+    error SameNFT();
+    error SameState();
+    error SplitNoOwner();
+    error SplitNotAllowed();
+    error SignatureExpired();
+    error TooManyTokenIDs();
+    error ZeroAddress();
+    error ZeroAmount();
+    error ZeroBalance();
+
+    event Deposit(
+        address indexed provider,
+        uint256 indexed tokenId,
+        DepositType indexed depositType,
+        uint256 value,
+        uint256 locktime,
+        uint256 ts
+    );
+    event Withdraw(
+        address indexed provider,
+        uint256 indexed tokenId,
+        uint256 value,
+        uint256 ts
+    );
+    event LockPermanent(
+        address indexed _owner,
+        uint256 indexed _tokenId,
+        uint256 amount,
+        uint256 _ts
+    );
+    event UnlockPermanent(
+        address indexed _owner,
+        uint256 indexed _tokenId,
+        uint256 amount,
+        uint256 _ts
+    );
+    event Supply(uint256 prevSupply, uint256 supply);
+    event Merge(
+        address indexed _sender,
+        uint256 indexed _from,
+        uint256 indexed _to,
+        uint256 _amountFrom,
+        uint256 _amountTo,
+        uint256 _amountFinal,
+        uint256 _locktime,
+        uint256 _ts
+    );
+    event Split(
+        uint256 indexed _from,
+        uint256 indexed _tokenId1,
+        uint256 indexed _tokenId2,
+        address _sender,
+        uint256 _splitAmount1,
+        uint256 _splitAmount2,
+        uint256 _locktime,
+        uint256 _ts
+    );
+    event CreateManaged(
+        address indexed _to, uint256 indexed _mTokenId, address indexed _from
+    );
+    event DepositManaged(
+        address indexed _owner,
+        uint256 indexed _tokenId,
+        uint256 indexed _mTokenId,
+        uint256 _weight,
+        uint256 _ts
+    );
+    event WithdrawManaged(
+        address indexed _owner,
+        uint256 indexed _tokenId,
+        uint256 indexed _mTokenId,
+        uint256 _weight,
+        uint256 _ts
+    );
+    event SetAllowedManager(address indexed _allowedManager);
+    event ToggleSplit(address indexed account, bool indexed canSplit);
+    event VoterAndDistributorSet(
+        address indexed voter, address indexed distributor
+    );
+
+    // State variables
+
+    /// @notice Address of token (RED) used to create a veNFT
+    function token() external view returns (address);
+
+    /// @notice Address of RewardsDistributor.sol
+    function distributor() external view returns (address);
+
+    /// @notice Address of Voter.sol
+    function voter() external view returns (address);
+
+    /// @notice Address of art proxy used for on-chain art generation
+    function artProxy() external view returns (address);
+
+    /// @dev address which can create managed NFTs
+    function allowedManager() external view returns (address);
+
+    /// @dev Current count of token
+    function tokenId() external view returns (uint256);
+
+    /**
+     * @notice Address of Infrared contract
+     * @return IInfrared instance of contract address
+     */
+    function infrared() external view returns (IInfraredUpgradeable);
+
+    /*///////////////////////////////////////////////////////////////
+                            MANAGED NFT STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    /// @dev Mapping of token id to escrow type
+    ///      Takes advantage of the fact default value is EscrowType.NORMAL
+    function escrowType(uint256 tokenId) external view returns (EscrowType);
+
+    /// @dev Mapping of token id to managed id
+    function idToManaged(uint256 tokenId)
+        external
+        view
+        returns (uint256 managedTokenId);
+
+    /// @dev Mapping of user token id to managed token id to weight of token id
+    function weights(uint256 tokenId, uint256 managedTokenId)
+        external
+        view
+        returns (uint256 weight);
+
+    /// @dev Mapping of managed id to deactivated state
+    function deactivated(uint256 tokenId)
+        external
+        view
+        returns (bool inactive);
+
+    /*///////////////////////////////////////////////////////////////
+                            MANAGED NFT LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @notice Create managed NFT (a permanent lock) for use within ecosystem.
+    /// @dev Throws if address already owns a managed NFT.
+    /// @return _mTokenId managed token id.
+    function createManagedLockFor(address _to)
+        external
+        returns (uint256 _mTokenId);
+
+    /// @notice Delegates balance to managed nft
+    ///         Note that NFTs deposited into a managed NFT will be re-locked
+    ///         to the maximum lock time on withdrawal.
+    ///         Permanent locks that are deposited will automatically unlock.
+    /// @dev Managed nft will remain max-locked as long as there is at least one
+    ///      deposit or withdrawal per week.
+    ///      Throws if deposit nft is managed.
+    ///      Throws if recipient nft is not managed.
+    ///      Throws if deposit nft is already locked.
+    ///      Throws if not called by voter.
+    /// @param _tokenId tokenId of NFT being deposited
+    /// @param _mTokenId tokenId of managed NFT that will receive the deposit
+    function depositManaged(uint256 _tokenId, uint256 _mTokenId) external;
+
+    /// @notice Retrieves locked rewards and withdraws balance from managed nft.
+    ///         Note that the NFT withdrawn is re-locked to the maximum lock time.
+    /// @dev Throws if NFT not locked.
+    ///      Throws if not called by voter.
+    /// @param _tokenId tokenId of NFT being deposited.
+    function withdrawManaged(uint256 _tokenId) external;
+
+    /// @notice Permit one address to call createManagedLockFor() that is not Voter.governor()
+    function setAllowedManager(address _allowedManager) external;
+
+    /// @notice Set Managed NFT state. Inactive NFTs cannot be deposited into.
+    /// @param _mTokenId managed nft state to set
+    /// @param _state true => inactive, false => active
+    function setManagedState(uint256 _mTokenId, bool _state) external;
+
+    /*///////////////////////////////////////////////////////////////
+                             METADATA STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    function name() external view returns (string memory);
+
+    function symbol() external view returns (string memory);
+
+    function version() external view returns (string memory);
+
+    function decimals() external view returns (uint8);
+
+    function setArtProxy(address _proxy) external;
+
+    /// @inheritdoc IERC721Metadata
+    function tokenURI(uint256 tokenId) external view returns (string memory);
+
+    /*//////////////////////////////////////////////////////////////
+                      ERC721 BALANCE/OWNER STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    /// @dev Mapping from owner address to mapping of index to tokenId
+    function ownerToNFTokenIdList(address _owner, uint256 _index)
+        external
+        view
+        returns (uint256 _tokenId);
+
+    /// @inheritdoc IERC721
+    function ownerOf(uint256 tokenId) external view returns (address owner);
+
+    /// @inheritdoc IERC721
+    function balanceOf(address owner) external view returns (uint256 balance);
+
+    /*//////////////////////////////////////////////////////////////
+                         ERC721 APPROVAL STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    /// @inheritdoc IERC721
+    function getApproved(uint256 _tokenId)
+        external
+        view
+        returns (address operator);
+
+    /// @inheritdoc IERC721
+    function isApprovedForAll(address owner, address operator)
+        external
+        view
+        returns (bool);
+
+    /// @notice Check whether spender is owner or an approved user for a given veNFT
+    /// @param _spender .
+    /// @param _tokenId .
+    function isApprovedOrOwner(address _spender, uint256 _tokenId)
+        external
+        returns (bool);
+
+    /*//////////////////////////////////////////////////////////////
+                              ERC721 LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @inheritdoc IERC721
+    function approve(address to, uint256 tokenId) external;
+
+    /// @inheritdoc IERC721
+    function setApprovalForAll(address operator, bool approved) external;
+
+    /// @inheritdoc IERC721
+    function transferFrom(address from, address to, uint256 tokenId) external;
+
+    /// @inheritdoc IERC721
+    function safeTransferFrom(address from, address to, uint256 tokenId)
+        external;
+
+    /// @inheritdoc IERC721
+    function safeTransferFrom(
+        address from,
+        address to,
+        uint256 tokenId,
+        bytes calldata data
+    ) external;
+
+    /*//////////////////////////////////////////////////////////////
+                              ERC165 LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @inheritdoc IERC165
+    function supportsInterface(bytes4 _interfaceID)
+        external
+        view
+        returns (bool);
+
+    /*//////////////////////////////////////////////////////////////
+                             ESCROW STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    /// @notice Total count of epochs witnessed since contract creation
+    function epoch() external view returns (uint256);
+
+    /// @notice Total amount of token() deposited
+    function supply() external view returns (uint256);
+
+    /// @notice Aggregate permanent locked balances
+    function permanentLockBalance() external view returns (uint256);
+
+    function userPointEpoch(uint256 _tokenId)
+        external
+        view
+        returns (uint256 _epoch);
+
+    /// @notice time -> signed slope change
+    function slopeChanges(uint256 _timestamp) external view returns (int128);
+
+    /// @notice account -> can split
+    function canSplit(address _account) external view returns (bool);
+
+    /// @notice Global point history at a given index
+    function pointHistory(uint256 _loc)
+        external
+        view
+        returns (GlobalPoint memory);
+
+    /// @notice Get the LockedBalance (amount, end) of a _tokenId
+    /// @param _tokenId .
+    /// @return LockedBalance of _tokenId
+    function locked(uint256 _tokenId)
+        external
+        view
+        returns (LockedBalance memory);
+
+    /// @notice User -> UserPoint[userEpoch]
+    function userPointHistory(uint256 _tokenId, uint256 _loc)
+        external
+        view
+        returns (UserPoint memory);
+
+    /*//////////////////////////////////////////////////////////////
+                              ESCROW LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @notice Record global data to checkpoint
+    function checkpoint() external;
+
+    /// @notice Deposit `_value` tokens for `_tokenId` and add to the lock
+    /// @dev Anyone (even a smart contract) can deposit for someone else, but
+    ///      cannot extend their locktime and deposit for a brand new user
+    /// @param _tokenId lock NFT
+    /// @param _value Amount to add to user's lock
+    function depositFor(uint256 _tokenId, uint256 _value) external;
+
+    /// @notice Deposit `_value` tokens for `msg.sender` and lock for `_lockDuration`
+    /// @param _value Amount to deposit
+    /// @param _lockDuration Number of seconds to lock tokens for (rounded down to nearest week)
+    /// @return TokenId of created veNFT
+    function createLock(uint256 _value, uint256 _lockDuration)
+        external
+        returns (uint256);
+
+    /// @notice Deposit `_value` tokens for `_to` and lock for `_lockDuration`
+    /// @param _value Amount to deposit
+    /// @param _lockDuration Number of seconds to lock tokens for (rounded down to nearest week)
+    /// @param _to Address to deposit
+    /// @return TokenId of created veNFT
+    function createLockFor(uint256 _value, uint256 _lockDuration, address _to)
+        external
+        returns (uint256);
+
+    /// @notice Deposit `_value` additional tokens for `_tokenId` without modifying the unlock time
+    /// @param _value Amount of tokens to deposit and add to the lock
+    function increaseAmount(uint256 _tokenId, uint256 _value) external;
+
+    /// @notice Extend the unlock time for `_tokenId`
+    ///         Cannot extend lock time of permanent locks
+    /// @param _lockDuration New number of seconds until tokens unlock
+    function increaseUnlockTime(uint256 _tokenId, uint256 _lockDuration)
+        external;
+
+    /// @notice Withdraw all tokens for `_tokenId`
+    /// @dev Only possible if the lock is both expired and not permanent
+    ///      This will burn the veNFT. Any rebases or rewards that are unclaimed
+    ///      will no longer be claimable. Claim all rebases and rewards prior to calling this.
+    function withdraw(uint256 _tokenId) external;
+
+    /// @notice Merges `_from` into `_to`.
+    /// @dev Cannot merge `_from` locks that are permanent or have already voted this epoch.
+    ///      Cannot merge `_to` locks that have already expired.
+    ///      This will burn the veNFT. Any rebases or rewards that are unclaimed
+    ///      will no longer be claimable. Claim all rebases and rewards prior to calling this.
+    /// @param _from VeNFT to merge from.
+    /// @param _to VeNFT to merge into.
+    function merge(uint256 _from, uint256 _to) external;
+
+    /// @notice Splits veNFT into two new veNFTS - one with oldLocked.amount - `_amount`, and the second with `_amount`
+    /// @dev    This burns the tokenId of the target veNFT
+    ///         Callable by approved or owner
+    ///         If this is called by approved, approved will not have permissions to manipulate the newly created veNFTs
+    ///         Returns the two new split veNFTs to owner
+    ///         If `from` is permanent, will automatically dedelegate.
+    ///         This will burn the veNFT. Any rebases or rewards that are unclaimed
+    ///         will no longer be claimable. Claim all rebases and rewards prior to calling this.
+    /// @param _from VeNFT to split.
+    /// @param _amount Amount to split from veNFT.
+    /// @return _tokenId1 Return tokenId of veNFT with oldLocked.amount - `_amount`.
+    /// @return _tokenId2 Return tokenId of veNFT with `_amount`.
+    function split(uint256 _from, uint256 _amount)
+        external
+        returns (uint256 _tokenId1, uint256 _tokenId2);
+
+    /// @notice Toggle split for a specific address.
+    /// @dev Toggle split for address(0) to enable or disable for all.
+    /// @param _account Address to toggle split permissions
+    /// @param _bool True to allow, false to disallow
+    function toggleSplit(address _account, bool _bool) external;
+
+    /// @notice Permanently lock a veNFT. Voting power will be equal to
+    ///         `LockedBalance.amount` with no decay. Required to delegate.
+    /// @dev Only callable by unlocked normal veNFTs.
+    /// @param _tokenId tokenId to lock.
+    function lockPermanent(uint256 _tokenId) external;
+
+    /// @notice Unlock a permanently locked veNFT. Voting power will decay.
+    ///         Will automatically dedelegate if delegated.
+    /// @dev Only callable by permanently locked veNFTs.
+    ///      Cannot unlock if already voted this epoch.
+    /// @param _tokenId tokenId to unlock.
+    function unlockPermanent(uint256 _tokenId) external;
+
+    /*///////////////////////////////////////////////////////////////
+                           GAUGE VOTING STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    /// @notice Get the voting power for _tokenId at the current timestamp
+    /// @dev Returns 0 if called in the same block as a transfer.
+    /// @param _tokenId .
+    /// @return Voting power
+    function balanceOfNFT(uint256 _tokenId) external view returns (uint256);
+
+    /// @notice Get the voting power for _tokenId at a given timestamp
+    /// @param _tokenId .
+    /// @param _t Timestamp to query voting power
+    /// @return Voting power
+    function balanceOfNFTAt(uint256 _tokenId, uint256 _t)
+        external
+        view
+        returns (uint256);
+
+    /// @notice Calculate total voting power at current timestamp
+    /// @return Total voting power at current timestamp
+    function totalSupply() external view returns (uint256);
+
+    /// @notice Calculate total voting power at a given timestamp
+    /// @param _t Timestamp to query total voting power
+    /// @return Total voting power at given timestamp
+    function totalSupplyAt(uint256 _t) external view returns (uint256);
+
+    /*///////////////////////////////////////////////////////////////
+                            GAUGE VOTING LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @notice See if a queried _tokenId has actively voted
+    /// @param _tokenId .
+    /// @return True if voted, else false
+    function voted(uint256 _tokenId) external view returns (bool);
+
+    /// @notice Set the global state voter and distributor
+    /// @dev This is only called once, at setup
+    function setVoterAndDistributor(address _voter, address _distributor)
+        external;
+
+    /// @notice Set `voted` for _tokenId to true or false
+    /// @dev Only callable by voter
+    /// @param _tokenId .
+    /// @param _voted .
+    function voting(uint256 _tokenId, bool _voted) external;
+
+    /*///////////////////////////////////////////////////////////////
+                            DAO VOTING STORAGE
+    //////////////////////////////////////////////////////////////*/
+
+    /// @notice The number of checkpoints for each tokenId
+    function numCheckpoints(uint256 tokenId) external view returns (uint48);
+
+    /// @notice A record of states for signing / validating signatures
+    function nonces(address account) external view returns (uint256);
+
+    /// @inheritdoc IVotes
+    function delegates(uint256 delegator) external view returns (uint256);
+
+    /// @notice A record of delegated token checkpoints for each account, by index
+    /// @param tokenId .
+    /// @param index .
+    /// @return Checkpoint
+    function checkpoints(uint256 tokenId, uint48 index)
+        external
+        view
+        returns (Checkpoint memory);
+
+    /// @inheritdoc IVotes
+    function getPastVotes(address account, uint256 tokenId, uint256 timestamp)
+        external
+        view
+        returns (uint256);
+
+    /// @inheritdoc IVotes
+    function getPastTotalSupply(uint256 timestamp)
+        external
+        view
+        returns (uint256);
+
+    /*///////////////////////////////////////////////////////////////
+                             DAO VOTING LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @inheritdoc IVotes
+    function delegate(uint256 delegator, uint256 delegatee) external;
+
+    /// @inheritdoc IVotes
+    function delegateBySig(
+        uint256 delegator,
+        uint256 delegatee,
+        uint256 nonce,
+        uint256 expiry,
+        uint8 v,
+        bytes32 r,
+        bytes32 s
+    ) external;
+
+    /*//////////////////////////////////////////////////////////////
+                              ERC6372 LOGIC
+    //////////////////////////////////////////////////////////////*/
+
+    /// @inheritdoc IERC6372
+    function clock() external view returns (uint48);
+
+    /// @inheritdoc IERC6372
+    function CLOCK_MODE() external view returns (string memory);
+}
diff --git asrc/voting (온체인)/libraries/BalanceLogicLibrary.sol bsrc/voting (온체인)/libraries/BalanceLogicLibrary.sol
new file mode 100644
index 0000000..9508dc0
--- /dev/null
+++ bsrc/voting (온체인)/libraries/BalanceLogicLibrary.sol
@@ -0,0 +1,162 @@
+// SPDX-License-Identifier: BUSL-1.1
+pragma solidity 0.8.26;
+
+import {IVotingEscrow} from "../interfaces/IVotingEscrow.sol";
+import {SafeCastLib} from "lib/solady/src/utils/SafeCastLib.sol";
+
+library BalanceLogicLibrary {
+    using SafeCastLib for uint256;
+    using SafeCastLib for int128;
+
+    uint256 internal constant WEEK = 1 weeks;
+
+    /// @notice Binary search to get the user point index for a token id at or prior to a given timestamp
+    /// @dev If a user point does not exist prior to the timestamp, this will return 0.
+    /// @param _userPointEpoch State of all user point epochs
+    /// @param _userPointHistory State of all user point history
+    /// @param _tokenId .
+    /// @param _timestamp .
+    /// @return User point index
+    function getPastUserPointIndex(
+        mapping(uint256 => uint256) storage _userPointEpoch,
+        mapping(uint256 => IVotingEscrow.UserPoint[1000000000]) storage
+            _userPointHistory,
+        uint256 _tokenId,
+        uint256 _timestamp
+    ) internal view returns (uint256) {
+        uint256 _userEpoch = _userPointEpoch[_tokenId];
+        if (_userEpoch == 0) return 0;
+        // First check most recent balance
+        if (_userPointHistory[_tokenId][_userEpoch].ts <= _timestamp) {
+            return (_userEpoch);
+        }
+        // Next check implicit zero balance
+        if (_userPointHistory[_tokenId][1].ts > _timestamp) return 0;
+
+        uint256 lower = 0;
+        uint256 upper = _userEpoch;
+        while (upper > lower) {
+            uint256 center = upper - (upper - lower) / 2; // ceil, avoiding overflow
+            IVotingEscrow.UserPoint storage userPoint =
+                _userPointHistory[_tokenId][center];
+            if (userPoint.ts == _timestamp) {
+                return center;
+            } else if (userPoint.ts < _timestamp) {
+                lower = center;
+            } else {
+                upper = center - 1;
+            }
+        }
+        return lower;
+    }
+
+    /// @notice Binary search to get the global point index at or prior to a given timestamp
+    /// @dev If a checkpoint does not exist prior to the timestamp, this will return 0.
+    /// @param _epoch Current global point epoch
+    /// @param _pointHistory State of all global point history
+    /// @param _timestamp .
+    /// @return Global point index
+    function getPastGlobalPointIndex(
+        uint256 _epoch,
+        mapping(uint256 => IVotingEscrow.GlobalPoint) storage _pointHistory,
+        uint256 _timestamp
+    ) internal view returns (uint256) {
+        if (_epoch == 0) return 0;
+        // First check most recent balance
+        if (_pointHistory[_epoch].ts <= _timestamp) return (_epoch);
+        // Next check implicit zero balance
+        if (_pointHistory[1].ts > _timestamp) return 0;
+
+        uint256 lower = 0;
+        uint256 upper = _epoch;
+        while (upper > lower) {
+            uint256 center = upper - (upper - lower) / 2; // ceil, avoiding overflow
+            IVotingEscrow.GlobalPoint storage globalPoint =
+                _pointHistory[center];
+            if (globalPoint.ts == _timestamp) {
+                return center;
+            } else if (globalPoint.ts < _timestamp) {
+                lower = center;
+            } else {
+                upper = center - 1;
+            }
+        }
+        return lower;
+    }
+
+    /// @notice Get the current voting power for `_tokenId`
+    /// @dev Adheres to the ERC20 `balanceOf` interface for Aragon compatibility
+    ///      Although only true of curve, but not solidly and its forks.
+    ///      Fetches last user point prior to a certain timestamp, then walks forward to timestamp.
+    /// @param _userPointEpoch State of all user point epochs
+    /// @param _userPointHistory State of all user point history
+    /// @param _tokenId NFT for lock
+    /// @param _t Epoch time to return voting power at
+    /// @return User voting power
+    function balanceOfNFTAt(
+        mapping(uint256 => uint256) storage _userPointEpoch,
+        mapping(uint256 => IVotingEscrow.UserPoint[1000000000]) storage
+            _userPointHistory,
+        uint256 _tokenId,
+        uint256 _t
+    ) external view returns (uint256) {
+        uint256 _epoch = getPastUserPointIndex(
+            _userPointEpoch, _userPointHistory, _tokenId, _t
+        );
+        // epoch 0 is an empty point
+        if (_epoch == 0) return 0;
+        IVotingEscrow.UserPoint memory lastPoint =
+            _userPointHistory[_tokenId][_epoch];
+        if (lastPoint.permanent != 0) {
+            return lastPoint.permanent;
+        } else {
+            lastPoint.bias -= lastPoint.slope * (_t - lastPoint.ts).toInt128();
+            if (lastPoint.bias < 0) {
+                lastPoint.bias = 0;
+            }
+            return lastPoint.bias.toUint256();
+        }
+    }
+
+    /// @notice Calculate total voting power at some point in the past
+    /// @param _slopeChanges State of all slopeChanges
+    /// @param _pointHistory State of all global point history
+    /// @param _epoch The epoch to start search from
+    /// @param _t Time to calculate the total voting power at
+    /// @return Total voting power at that time
+    function supplyAt(
+        mapping(uint256 => int128) storage _slopeChanges,
+        mapping(uint256 => IVotingEscrow.GlobalPoint) storage _pointHistory,
+        uint256 _epoch,
+        uint256 _t
+    ) external view returns (uint256) {
+        uint256 epoch_ = getPastGlobalPointIndex(_epoch, _pointHistory, _t);
+        // epoch 0 is an empty point
+        if (epoch_ == 0) return 0;
+        IVotingEscrow.GlobalPoint memory _point = _pointHistory[epoch_];
+        int128 bias = _point.bias;
+        int128 slope = _point.slope;
+        uint256 ts = _point.ts;
+        uint256 t_i = (ts / WEEK) * WEEK;
+        for (uint256 i = 0; i < 255; ++i) {
+            t_i += WEEK;
+            int128 dSlope = 0;
+            if (t_i > _t) {
+                t_i = _t;
+            } else {
+                dSlope = _slopeChanges[t_i];
+            }
+            bias -= slope * (t_i - ts).toInt128();
+            if (t_i == _t) {
+                break;
+            }
+            slope += dSlope;
+            ts = t_i;
+        }
+
+        if (bias < 0) {
+            bias = 0;
+        }
+        return bias.toUint256() + _point.permanentLockBalance;
+    }
+}
diff --git asrc/voting (온체인)/libraries/DelegationLogicLibrary.sol bsrc/voting (온체인)/libraries/DelegationLogicLibrary.sol
new file mode 100644
index 0000000..656ba3e
--- /dev/null
+++ bsrc/voting (온체인)/libraries/DelegationLogicLibrary.sol
@@ -0,0 +1,201 @@
+// SPDX-License-Identifier: BUSL-1.1
+pragma solidity 0.8.26;
+
+import {IVotingEscrow} from "../interfaces/IVotingEscrow.sol";
+import {SafeCastLib} from "lib/solady/src/utils/SafeCastLib.sol";
+
+library DelegationLogicLibrary {
+    using SafeCastLib for int128;
+
+    /// @notice Used by `_mint`, `_transferFrom`, `_burn` and `delegate`
+    ///         to update delegator voting checkpoints.
+    ///         Automatically dedelegates, then updates checkpoint.
+    /// @dev This function depends on `_locked` and must be called prior to token state changes.
+    ///      If you wish to dedelegate only, use `_delegate(tokenId, 0)` instead.
+    /// @param _locked State of all locked balances
+    /// @param _numCheckpoints State of all user checkpoint counts
+    /// @param _checkpoints State of all user checkpoints
+    /// @param _delegates State of all user delegatees
+    /// @param _delegator The delegator to update checkpoints for
+    /// @param _delegatee The new delegatee for the delegator. Cannot be equal to `_delegator` (use 0 instead).
+    /// @param _owner The new (or current) owner for the delegator
+    function checkpointDelegator(
+        mapping(uint256 => IVotingEscrow.LockedBalance) storage _locked,
+        mapping(uint256 => uint48) storage _numCheckpoints,
+        mapping(uint256 => mapping(uint48 => IVotingEscrow.Checkpoint)) storage
+            _checkpoints,
+        mapping(uint256 => uint256) storage _delegates,
+        uint256 _delegator,
+        uint256 _delegatee,
+        address _owner
+    ) external {
+        uint256 delegatedBalance = _locked[_delegator].amount.toUint256();
+        uint48 numCheckpoint = _numCheckpoints[_delegator];
+        IVotingEscrow.Checkpoint storage cpOld = numCheckpoint > 0
+            ? _checkpoints[_delegator][numCheckpoint - 1]
+            : _checkpoints[_delegator][0];
+        // Dedelegate from delegatee if delegated
+        checkpointDelegatee(
+            _numCheckpoints,
+            _checkpoints,
+            cpOld.delegatee,
+            delegatedBalance,
+            false
+        );
+        IVotingEscrow.Checkpoint storage cp =
+            _checkpoints[_delegator][numCheckpoint];
+        cp.fromTimestamp = block.timestamp;
+        cp.delegatedBalance = cpOld.delegatedBalance;
+        cp.delegatee = _delegatee;
+        cp.owner = _owner;
+
+        if (_isCheckpointInNewBlock(_numCheckpoints, _checkpoints, _delegator))
+        {
+            _numCheckpoints[_delegator]++;
+        } else {
+            _checkpoints[_delegator][numCheckpoint - 1] = cp;
+            delete _checkpoints[_delegator][numCheckpoint];
+        }
+
+        _delegates[_delegator] = _delegatee;
+    }
+
+    /// @notice Update delegatee's `delegatedBalance` by `balance`.
+    ///         Only updates if delegating to a new delegatee.
+    /// @dev If used with `balance` == `_locked[_tokenId].amount`, then this is the same as
+    ///      delegating or dedelegating from `_tokenId`
+    ///      If used with `balance` < `_locked[_tokenId].amount`, then this is used to adjust
+    ///      `delegatedBalance` when a user's balance is modified (e.g. `increaseAmount`, `merge` etc).
+    ///      If `delegatee` is 0 (i.e. user is not delegating), then do nothing.
+    /// @param _numCheckpoints State of all user checkpoint counts
+    /// @param _checkpoints State of all user checkpoints
+    /// @param _delegatee The delegatee's tokenId
+    /// @param balance_ The delta in balance change
+    /// @param _increase True if balance is increasing, false if decreasing
+    function checkpointDelegatee(
+        mapping(uint256 => uint48) storage _numCheckpoints,
+        mapping(uint256 => mapping(uint48 => IVotingEscrow.Checkpoint)) storage
+            _checkpoints,
+        uint256 _delegatee,
+        uint256 balance_,
+        bool _increase
+    ) public {
+        if (_delegatee == 0) return;
+        uint48 numCheckpoint = _numCheckpoints[_delegatee];
+        IVotingEscrow.Checkpoint storage cpOld = numCheckpoint > 0
+            ? _checkpoints[_delegatee][numCheckpoint - 1]
+            : _checkpoints[_delegatee][0];
+        IVotingEscrow.Checkpoint storage cp =
+            _checkpoints[_delegatee][numCheckpoint];
+        cp.fromTimestamp = block.timestamp;
+        cp.owner = cpOld.owner;
+        // do not expect balance_ > cpOld.delegatedBalance when decrementing but just in case
+        cp.delegatedBalance = _increase
+            ? cpOld.delegatedBalance + balance_
+            : (
+                balance_ < cpOld.delegatedBalance
+                    ? cpOld.delegatedBalance - balance_
+                    : 0
+            );
+        cp.delegatee = cpOld.delegatee;
+
+        if (_isCheckpointInNewBlock(_numCheckpoints, _checkpoints, _delegatee))
+        {
+            _numCheckpoints[_delegatee]++;
+        } else {
+            _checkpoints[_delegatee][numCheckpoint - 1] = cp;
+            delete _checkpoints[_delegatee][numCheckpoint];
+        }
+    }
+
+    function _isCheckpointInNewBlock(
+        mapping(uint256 => uint48) storage _numCheckpoints,
+        mapping(uint256 => mapping(uint48 => IVotingEscrow.Checkpoint)) storage
+            _checkpoints,
+        uint256 _tokenId
+    ) internal view returns (bool) {
+        uint48 _nCheckPoints = _numCheckpoints[_tokenId];
+
+        if (
+            _nCheckPoints > 0
+                && _checkpoints[_tokenId][_nCheckPoints - 1].fromTimestamp
+                    == block.timestamp
+        ) {
+            return false;
+        } else {
+            return true;
+        }
+    }
+
+    /// @notice Binary search to get the voting checkpoint for a token id at or prior to a given timestamp.
+    /// @dev If a checkpoint does not exist prior to the timestamp, this will return 0.
+    /// @param _numCheckpoints State of all user checkpoint counts
+    /// @param _checkpoints State of all user checkpoints
+    /// @param _tokenId .
+    /// @param _timestamp .
+    /// @return The index of the checkpoint.
+    function getPastVotesIndex(
+        mapping(uint256 => uint48) storage _numCheckpoints,
+        mapping(uint256 => mapping(uint48 => IVotingEscrow.Checkpoint)) storage
+            _checkpoints,
+        uint256 _tokenId,
+        uint256 _timestamp
+    ) internal view returns (uint48) {
+        uint48 nCheckpoints = _numCheckpoints[_tokenId];
+        if (nCheckpoints == 0) return 0;
+        // First check most recent balance
+        if (
+            _checkpoints[_tokenId][nCheckpoints - 1].fromTimestamp <= _timestamp
+        ) return (nCheckpoints - 1);
+        // Next check implicit zero balance
+        if (_checkpoints[_tokenId][0].fromTimestamp > _timestamp) return 0;
+
+        uint48 lower = 0;
+        uint48 upper = nCheckpoints - 1;
+        while (upper > lower) {
+            uint48 center = upper - (upper - lower) / 2; // ceil, avoiding overflow
+            IVotingEscrow.Checkpoint storage cp = _checkpoints[_tokenId][center];
+            if (cp.fromTimestamp == _timestamp) {
+                return center;
+            } else if (cp.fromTimestamp < _timestamp) {
+                lower = center;
+            } else {
+                upper = center - 1;
+            }
+        }
+        return lower;
+    }
+
+    /// @notice Retrieves historical voting balance for a token id at a given timestamp.
+    /// @dev If a checkpoint does not exist prior to the timestamp, this will return 0.
+    ///      The user must also own the token at the time in order to receive a voting balance.
+    /// @param _numCheckpoints State of all user checkpoint counts
+    /// @param _checkpoints State of all user checkpoints
+    /// @param _account .
+    /// @param _tokenId .
+    /// @param _timestamp .
+    /// @return Total voting balance including delegations at a given timestamp.
+    function getPastVotes(
+        mapping(uint256 => uint48) storage _numCheckpoints,
+        mapping(uint256 => mapping(uint48 => IVotingEscrow.Checkpoint)) storage
+            _checkpoints,
+        address _account,
+        uint256 _tokenId,
+        uint256 _timestamp
+    ) external view returns (uint256) {
+        uint48 _checkIndex = getPastVotesIndex(
+            _numCheckpoints, _checkpoints, _tokenId, _timestamp
+        );
+        IVotingEscrow.Checkpoint memory lastCheckpoint =
+            _checkpoints[_tokenId][_checkIndex];
+        // If no point exists prior to the given timestamp, return 0
+        if (lastCheckpoint.fromTimestamp > _timestamp) return 0;
+        // Check ownership
+        if (_account != lastCheckpoint.owner) return 0;
+        uint256 votes = lastCheckpoint.delegatedBalance;
+        return lastCheckpoint.delegatee == 0
+            ? votes
+                + IVotingEscrow(address(this)).balanceOfNFTAt(_tokenId, _timestamp)
+            : votes;
+    }
+}
diff --git asrc/voting (온체인)/libraries/VelodromeTimeLibrary.sol bsrc/voting (온체인)/libraries/VelodromeTimeLibrary.sol
new file mode 100644
index 0000000..2532dcb
--- /dev/null
+++ bsrc/voting (온체인)/libraries/VelodromeTimeLibrary.sol
@@ -0,0 +1,58 @@
+// SPDX-License-Identifier: BUSL-1.1
+pragma solidity 0.8.26;
+
+library VelodromeTimeLibrary {
+    uint256 internal constant WEEK = 7 days;
+
+    /**
+     * @notice Calculate the start of the current epoch based on the timestamp provided
+     * @dev Epochs are aligned to weekly intervals, with each epoch starting at midnight UTC.
+     * @param timestamp The current timestamp to align
+     * @return The start timestamp of the epoch week
+     */
+    function epochStart(uint256 timestamp) internal pure returns (uint256) {
+        unchecked {
+            return timestamp - (timestamp % WEEK);
+        }
+    }
+
+    /**
+     * @notice Calculate the start of the next epoch or end of the current epoch
+     * @dev Returns the timestamp at the start of the next weekly epoch following the given timestamp.
+     * @param timestamp The current timestamp
+     * @return The start timestamp of the next epoch
+     */
+    function epochNext(uint256 timestamp) internal pure returns (uint256) {
+        unchecked {
+            return timestamp - (timestamp % WEEK) + WEEK;
+        }
+    }
+
+    /**
+     * @notice Determine the start of the voting window for the current epoch
+     * @dev Voting windows start one hour into the weekly epoch.
+     * @param timestamp The timestamp to calculate from
+     * @return The start timestamp of the voting window within the epoch
+     */
+    function epochVoteStart(uint256 timestamp)
+        internal
+        pure
+        returns (uint256)
+    {
+        unchecked {
+            return timestamp - (timestamp % WEEK) + 1 hours;
+        }
+    }
+
+    /**
+     * @notice Calculate the end of the voting window within the current epoch
+     * @dev Voting windows close one hour before the next epoch begins.
+     * @param timestamp The timestamp to calculate from
+     * @return The end timestamp of the voting window within the epoch
+     */
+    function epochVoteEnd(uint256 timestamp) internal pure returns (uint256) {
+        unchecked {
+            return timestamp - (timestamp % WEEK) + WEEK - 1 hours;
+        }
+    }
+}
diff --git asrc/voting (온체인)/rewards/BribeVotingReward.sol bsrc/voting (온체인)/rewards/BribeVotingReward.sol
new file mode 100644
index 0000000..1674fa9
--- /dev/null
+++ bsrc/voting (온체인)/rewards/BribeVotingReward.sol
@@ -0,0 +1,68 @@
+// SPDX-License-Identifier: BUSL-1.1
+pragma solidity 0.8.26;
+
+import {IVoter} from "../interfaces/IVoter.sol";
+import {VotingReward} from "./VotingReward.sol";
+
+/**
+ * @title BribeVotingReward
+ * @notice Implementation of voting rewards for bribes based on user votes
+ * @dev Final implementation of voting rewards specifically for bribe distribution
+ */
+contract BribeVotingReward is VotingReward {
+    event NoLongerWhitelistedTokenRemoved(address indexed token);
+
+    /**
+     * @notice Initializes bribe voting rewards
+     * @param _voter Address of voter contract
+     * @param _rewards Initial array of reward token addresses
+     */
+    constructor(address _voter, address[] memory _rewards)
+        VotingReward(_voter, _rewards)
+    {}
+
+    /**
+     * @inheritdoc VotingReward
+     * @dev Validates and whitelists reward tokens before processing
+     */
+    function notifyRewardAmount(address token, uint256 amount)
+        external
+        override
+        nonReentrant
+    {
+        if (!isReward[token]) {
+            if (!IVoter(voter).isWhitelistedToken(token)) {
+                revert NotWhitelisted();
+            }
+            isReward[token] = true;
+            rewards.push(token);
+        }
+
+        _notifyRewardAmount(msg.sender, token, amount);
+    }
+
+    /**
+     * @notice Removes tokens from the rewards list that are no longer whitelisted
+     * @param tokens The list of tokens to remove
+     */
+    function removeNoLongerWhitelistedTokens(address[] calldata tokens)
+        external
+    {
+        for (uint256 i = 0; i < tokens.length; i++) {
+            if (
+                !IVoter(voter).isWhitelistedToken(tokens[i])
+                    && isReward[tokens[i]]
+            ) {
+                isReward[tokens[i]] = false;
+                for (uint256 j = 0; j < rewards.length; j++) {
+                    if (rewards[j] == tokens[i]) {
+                        rewards[j] = rewards[rewards.length - 1];
+                        rewards.pop();
+                        break;
+                    }
+                }
+                emit NoLongerWhitelistedTokenRemoved(tokens[i]);
+            }
+        }
+    }
+}
diff --git asrc/voting (온체인)/rewards/Reward.sol bsrc/voting (온체인)/rewards/Reward.sol
new file mode 100644
index 0000000..e1c46aa
--- /dev/null
+++ bsrc/voting (온체인)/rewards/Reward.sol
@@ -0,0 +1,340 @@
+// SPDX-License-Identifier: BUSL-1.1
+pragma solidity 0.8.26;
+
+import {IReward} from "../interfaces/IReward.sol";
+import {IVoter} from "../interfaces/IVoter.sol";
+import {ERC20} from "@solmate/tokens/ERC20.sol";
+import {SafeTransferLib} from "@solmate/utils/SafeTransferLib.sol";
+import {ERC2771Context} from "@openzeppelin/contracts/metatx/ERC2771Context.sol";
+import {ReentrancyGuard} from
+    "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
+import {VelodromeTimeLibrary} from "../libraries/VelodromeTimeLibrary.sol";
+
+/**
+ * @title Reward
+ * @author velodrome.finance, @figs999, @pegahcarter
+ * @notice Base implementation for reward distribution contracts
+ * @dev Abstract contract providing core reward distribution functionality
+ */
+abstract contract Reward is IReward, ReentrancyGuard {
+    using SafeTransferLib for ERC20;
+
+    /// @inheritdoc IReward
+    uint256 public constant DURATION = 7 days;
+
+    /// @inheritdoc IReward
+    address public immutable voter;
+    /// @inheritdoc IReward
+    address public immutable ve;
+    /// @inheritdoc IReward
+    address public immutable authorized;
+    /// @inheritdoc IReward
+    uint256 public totalSupply;
+    /// @inheritdoc IReward
+    uint256 public supplyNumCheckpoints;
+    /**
+     * @notice List of all reward tokens supported by this contract
+     * @dev Used for token enumeration and management
+     */
+    address[] public rewards;
+    /// @inheritdoc IReward
+    mapping(uint256 => uint256) public balanceOf;
+    /// @inheritdoc IReward
+    mapping(address => mapping(uint256 => uint256)) public tokenRewardsPerEpoch;
+    /// @inheritdoc IReward
+    mapping(address => mapping(uint256 => uint256)) public lastEarn;
+    /// @inheritdoc IReward
+    mapping(address => bool) public isReward;
+    /// @notice A record of balance checkpoints for each account, by index
+    mapping(uint256 => mapping(uint256 => Checkpoint)) public checkpoints;
+    /// @inheritdoc IReward
+    mapping(uint256 => uint256) public numCheckpoints;
+    /// @notice A record of balance checkpoints for each token, by index
+    mapping(uint256 => SupplyCheckpoint) public supplyCheckpoints;
+
+    /**
+     * @notice Initializes reward contract with voter address
+     * @param _voter Address of voter contract managing rewards
+     */
+    constructor(address _voter) {
+        voter = _voter;
+        ve = IVoter(_voter).ve();
+    }
+
+    /// @inheritdoc IReward
+    function getPriorBalanceIndex(uint256 tokenId, uint256 timestamp)
+        public
+        view
+        returns (uint256)
+    {
+        uint256 nCheckpoints = numCheckpoints[tokenId];
+        if (nCheckpoints == 0) {
+            return 0;
+        }
+
+        // First check most recent balance
+        if (checkpoints[tokenId][nCheckpoints - 1].timestamp <= timestamp) {
+            return (nCheckpoints - 1);
+        }
+
+        // Next check implicit zero balance
+        if (checkpoints[tokenId][0].timestamp > timestamp) {
+            return 0;
+        }
+
+        uint256 lower = 0;
+        uint256 upper = nCheckpoints - 1;
+        while (upper > lower) {
+            uint256 center = upper - (upper - lower) / 2; // ceil, avoiding overflow
+            Checkpoint memory cp = checkpoints[tokenId][center];
+            if (cp.timestamp == timestamp) {
+                return center;
+            } else if (cp.timestamp < timestamp) {
+                lower = center;
+            } else {
+                upper = center - 1;
+            }
+        }
+        return lower;
+    }
+
+    /// @inheritdoc IReward
+    function getPriorSupplyIndex(uint256 timestamp)
+        public
+        view
+        returns (uint256)
+    {
+        uint256 nCheckpoints = supplyNumCheckpoints;
+        if (nCheckpoints == 0) {
+            return 0;
+        }
+
+        // First check most recent balance
+        if (supplyCheckpoints[nCheckpoints - 1].timestamp <= timestamp) {
+            return (nCheckpoints - 1);
+        }
+
+        // Next check implicit zero balance
+        if (supplyCheckpoints[0].timestamp > timestamp) {
+            return 0;
+        }
+
+        uint256 lower = 0;
+        uint256 upper = nCheckpoints - 1;
+        while (upper > lower) {
+            uint256 center = upper - (upper - lower) / 2; // ceil, avoiding overflow
+            SupplyCheckpoint memory cp = supplyCheckpoints[center];
+            if (cp.timestamp == timestamp) {
+                return center;
+            } else if (cp.timestamp < timestamp) {
+                lower = center;
+            } else {
+                upper = center - 1;
+            }
+        }
+        return lower;
+    }
+    /**
+     * @notice Writes user checkpoint with updated balance
+     * @dev Updates or creates checkpoint based on epoch timing
+     * @param tokenId ID of veNFT to checkpoint
+     * @param balance New balance to record
+     */
+
+    function _writeCheckpoint(uint256 tokenId, uint256 balance) internal {
+        uint256 _nCheckPoints = numCheckpoints[tokenId];
+        uint256 _timestamp = block.timestamp;
+
+        if (
+            _nCheckPoints > 0
+                && VelodromeTimeLibrary.epochStart(
+                    checkpoints[tokenId][_nCheckPoints - 1].timestamp
+                ) == VelodromeTimeLibrary.epochStart(_timestamp)
+        ) {
+            checkpoints[tokenId][_nCheckPoints - 1] =
+                Checkpoint(_timestamp, balance);
+        } else {
+            checkpoints[tokenId][_nCheckPoints] =
+                Checkpoint(_timestamp, balance);
+            numCheckpoints[tokenId] = _nCheckPoints + 1;
+        }
+    }
+    /**
+     * @notice Writes global supply checkpoint
+     * @dev Updates or creates checkpoint based on epoch timing
+     */
+
+    function _writeSupplyCheckpoint() internal {
+        uint256 _nCheckPoints = supplyNumCheckpoints;
+        uint256 _timestamp = block.timestamp;
+
+        if (
+            _nCheckPoints > 0
+                && VelodromeTimeLibrary.epochStart(
+                    supplyCheckpoints[_nCheckPoints - 1].timestamp
+                ) == VelodromeTimeLibrary.epochStart(_timestamp)
+        ) {
+            supplyCheckpoints[_nCheckPoints - 1] =
+                SupplyCheckpoint(_timestamp, totalSupply);
+        } else {
+            supplyCheckpoints[_nCheckPoints] =
+                SupplyCheckpoint(_timestamp, totalSupply);
+            supplyNumCheckpoints = _nCheckPoints + 1;
+        }
+    }
+
+    /// @inheritdoc IReward
+    function rewardsListLength() external view returns (uint256) {
+        return rewards.length;
+    }
+
+    /// @inheritdoc IReward
+    function earned(address token, uint256 tokenId)
+        public
+        view
+        returns (uint256)
+    {
+        if (numCheckpoints[tokenId] == 0) {
+            return 0;
+        }
+
+        uint256 reward = 0;
+        uint256 _supply = 1;
+        uint256 _currTs =
+            VelodromeTimeLibrary.epochStart(lastEarn[token][tokenId]); // take epoch last claimed in as starting point
+        uint256 _index = getPriorBalanceIndex(tokenId, _currTs);
+        Checkpoint memory cp0 = checkpoints[tokenId][_index];
+
+        // accounts for case where lastEarn is before first checkpoint
+        // max value
+        _currTs = _currTs > VelodromeTimeLibrary.epochStart(cp0.timestamp)
+            ? _currTs
+            : VelodromeTimeLibrary.epochStart(cp0.timestamp);
+
+        // get epochs between current epoch and first checkpoint in same epoch as last claim
+        uint256 numEpochs = (
+            VelodromeTimeLibrary.epochStart(block.timestamp) - _currTs
+        ) / DURATION;
+
+        if (numEpochs > 0) {
+            for (uint256 i = 0; i < numEpochs; i++) {
+                // get index of last checkpoint in this epoch
+                _index = getPriorBalanceIndex(tokenId, _currTs + DURATION - 1);
+                // get checkpoint in this epoch
+                cp0 = checkpoints[tokenId][_index];
+                // get supply of last checkpoint in this epoch
+                // max value
+                uint256 supplyCP = supplyCheckpoints[getPriorSupplyIndex(
+                    _currTs + DURATION - 1
+                )].supply;
+                _supply = supplyCP > 1 ? supplyCP : 1;
+                reward += (cp0.balanceOf * tokenRewardsPerEpoch[token][_currTs])
+                    / _supply;
+                _currTs += DURATION;
+            }
+        }
+
+        return reward;
+    }
+
+    /// @inheritdoc IReward
+    function _deposit(uint256 amount, uint256 tokenId) external {
+        if (msg.sender != authorized) revert NotAuthorized();
+
+        totalSupply += amount;
+        balanceOf[tokenId] += amount;
+
+        _writeCheckpoint(tokenId, balanceOf[tokenId]);
+        _writeSupplyCheckpoint();
+
+        emit Deposit(msg.sender, tokenId, amount);
+    }
+
+    /// @inheritdoc IReward
+    function _withdraw(uint256 amount, uint256 tokenId) external {
+        if (msg.sender != authorized) revert NotAuthorized();
+
+        totalSupply -= amount;
+        balanceOf[tokenId] -= amount;
+
+        _writeCheckpoint(tokenId, balanceOf[tokenId]);
+        _writeSupplyCheckpoint();
+
+        emit Withdraw(msg.sender, tokenId, amount);
+    }
+
+    /// @inheritdoc IReward
+    function getReward(uint256 tokenId, address[] memory tokens)
+        external
+        virtual
+        nonReentrant
+    {}
+
+    /**
+     * @notice Internal helper for processing reward claims
+     * @dev Calculates and transfers earned rewards to recipient
+     * @param recipient Address to receive claimed rewards
+     * @param tokenId ID of veNFT claiming rewards
+     * @param tokens Array of reward tokens to claim
+     */
+    function _getReward(
+        address recipient,
+        uint256 tokenId,
+        address[] memory tokens
+    ) internal {
+        uint256 _length = tokens.length;
+        for (uint256 i = 0; i < _length; i++) {
+            uint256 _reward = earned(tokens[i], tokenId);
+            lastEarn[tokens[i]][tokenId] = block.timestamp;
+            if (_reward > 0) ERC20(tokens[i]).safeTransfer(recipient, _reward);
+
+            emit ClaimRewards(recipient, tokens[i], _reward);
+        }
+    }
+
+    /// @inheritdoc IReward
+    function notifyRewardAmount(address token, uint256 amount)
+        external
+        virtual
+        nonReentrant
+    {}
+
+    /// @inheritdoc IReward
+    function renotifyRewardAmount(uint256 timestamp, address token) external {
+        uint256 epochStart = VelodromeTimeLibrary.epochStart(timestamp);
+        uint256 currentEpochStart =
+            VelodromeTimeLibrary.epochStart(block.timestamp);
+        uint256 rewardAmount = tokenRewardsPerEpoch[token][epochStart];
+        uint256 index = getPriorSupplyIndex(timestamp);
+
+        if (rewardAmount == 0) revert ZeroAmount();
+        if (currentEpochStart <= epochStart) revert ActiveEpoch();
+        if (supplyCheckpoints[index].supply != 0) revert NonZeroSupply();
+
+        tokenRewardsPerEpoch[token][epochStart] = 0;
+
+        // Redistribute rewards to current epoch.
+        tokenRewardsPerEpoch[token][currentEpochStart] += rewardAmount;
+
+        emit NotifyReward(address(this), token, epochStart, rewardAmount);
+    }
+
+    /**
+     * @notice Internal helper for adding rewards
+     * @dev Transfers tokens and updates reward accounting
+     * @param sender Address providing reward tokens
+     * @param token Address of reward token
+     * @param amount Amount of tokens to add as rewards
+     */
+    function _notifyRewardAmount(address sender, address token, uint256 amount)
+        internal
+    {
+        if (amount == 0) revert ZeroAmount();
+        ERC20(token).safeTransferFrom(sender, address(this), amount);
+
+        uint256 epochStart = VelodromeTimeLibrary.epochStart(block.timestamp);
+        tokenRewardsPerEpoch[token][epochStart] += amount;
+
+        emit NotifyReward(sender, token, epochStart, amount);
+    }
+}
diff --git asrc/voting (온체인)/rewards/VotingReward.sol bsrc/voting (온체인)/rewards/VotingReward.sol
new file mode 100644
index 0000000..f8f4b15
--- /dev/null
+++ bsrc/voting (온체인)/rewards/VotingReward.sol
@@ -0,0 +1,56 @@
+// SPDX-License-Identifier: BUSL-1.1
+pragma solidity 0.8.26;
+
+import {Reward} from "./Reward.sol";
+import {IVotingEscrow} from "../interfaces/IVotingEscrow.sol";
+import {IVoter} from "../interfaces/IVoter.sol";
+
+/**
+ * @title VotingReward
+ * @notice Base contract for rewards distributed based on voting power
+ * @dev Extends Reward with voting-specific reward logic
+ */
+abstract contract VotingReward is Reward {
+    /**
+     * @notice Configures voting rewards with initial reward tokens
+     * @param _voter Address of voter contract
+     * @param _rewards Initial array of reward token addresses
+     */
+    constructor(address _voter, address[] memory _rewards) Reward(_voter) {
+        uint256 _length = _rewards.length;
+        for (uint256 i; i < _length; i++) {
+            if (_rewards[i] != address(0)) {
+                isReward[_rewards[i]] = true;
+                rewards.push(_rewards[i]);
+            }
+        }
+
+        authorized = _voter;
+    }
+
+    /**
+     * @inheritdoc Reward
+     * @dev Validates caller is token owner or voter before processing claim
+     */
+    function getReward(uint256 tokenId, address[] memory tokens)
+        external
+        override
+        nonReentrant
+    {
+        if (
+            !IVotingEscrow(ve).isApprovedOrOwner(msg.sender, tokenId)
+                && msg.sender != voter
+        ) revert NotAuthorized();
+
+        address _owner = IVotingEscrow(ve).ownerOf(tokenId);
+        _getReward(_owner, tokenId, tokens);
+    }
+
+    /// @inheritdoc Reward
+    function notifyRewardAmount(address token, uint256 amount)
+        external
+        virtual
+        override
+        nonReentrant
+    {}
+}

```
