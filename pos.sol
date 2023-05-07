pragma solidity ^0.8.0;

contract ProofOfStake {
    struct Validator {
        address validatorAddress;
        uint256 stake;
        uint256 balance;
    }

    struct Block {
        uint256 id;
        uint256 timestamp;
        string data;
        bytes32 previousHash;
        bytes32 hash;
    }

    Validator[] public validators;
    Block[] public blocks;

    constructor() {
        // Add initial validators
        addValidator(msg.sender, 100);
        addValidator(0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2, 50);
        addValidator(0x4B20993Bc481177ec7E8f571ceCaE8A9e22C02db, 75);
        Block memory genesisBlock = Block({
            id: 0,
            timestamp: block.timestamp,
            data: "Genesis Block",
            previousHash: 0,
            hash: 0
        });
        genesisBlock.hash = keccak256(
            abi.encode(
                genesisBlock.id,
                genesisBlock.timestamp,
                genesisBlock.data,
                genesisBlock.previousHash
            )
        );
        blocks.push(genesisBlock);
    }

    function addValidator(address _address, uint256 _stake) public {
        validators.push(
            Validator({validatorAddress: _address, stake: _stake, balance: 0})
        );
    }

    function selectValidator() public view returns (Validator memory) {
        uint256 totalStake = 0;
        for (uint256 i = 0; i < validators.length; i++) {
            totalStake += validators[i].stake;
        }
        bytes memory packedData = abi.encodePacked(
            block.difficulty,
            block.timestamp
        );
        for (uint256 i = 0; i < validators.length; i++) {
            packedData = abi.encodePacked(
                packedData,
                validators[i].validatorAddress,
                validators[i].stake
            );
        }
        uint256 randomValue = uint256(keccak256(packedData)) % totalStake;
        uint256 cumulativeStake = 0;
        for (uint256 i = 0; i < validators.length; i++) {
            cumulativeStake += validators[i].stake;
            if (randomValue < cumulativeStake) {
                return validators[i];
            }
        }
    }

    function addBlock(string memory _data) public {
        Validator memory validator = selectValidator();
        Block memory newBlock = Block(
            blocks.length,
            block.timestamp,
            _data,
            blocks[blocks.length - 1].hash,
            0
        );
        newBlock.hash = keccak256(
            abi.encode(
                newBlock.id,
                newBlock.timestamp,
                newBlock.data,
                newBlock.previousHash
            )
        );
        if (validateBlock(validator, newBlock, blocks[blocks.length - 1])) {
            blocks.push(newBlock);
            validator.balance += 10;
        }
    }

    function validateBlock(
        Validator memory validator,
        Block memory newBlock,
        Block memory previousBlock
    ) internal pure returns (bool) {
        bytes32 hash = keccak256(
            abi.encode(
                newBlock.id,
                newBlock.timestamp,
                newBlock.data,
                previousBlock.hash
            )
        );
        return (hash == newBlock.hash);
    }

    function isBlockValid(Block memory _newBlock, Block memory _previousBlock)
        internal
        pure
        returns (bool)
    {
        if (_newBlock.previousHash != _previousBlock.previousHash) {
            return false;
        }
        bytes32 hash = keccak256(
            abi.encodePacked(
                _newBlock.id,
                _newBlock.timestamp,
                _newBlock.data,
                _previousBlock.previousHash
            )
        );
        if (hash != _newBlock.hash) {
            return false;
        }
        return true;
    }
}
