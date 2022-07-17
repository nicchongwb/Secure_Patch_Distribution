pragma solidity ^0.5.0;

contract SubmitPatch {
  uint public PatchCount; // State Variable similar to Static

  struct Patch {
    uint id;
    string hPatch;  // SHA256 Hash of Patch
    string txHashDC; // Transaction Hash of Dgitial Cert
  }

  // mapping is a hash datastruc where uint is the key, Patch is the value
  // mapping datastruc serves as a DB index method
  mapping(uint => Patch) public patches;

  // Utitlity Function
  function addrToStr(address _addr) public pure returns (string memory) {
    bytes32 value = bytes32(uint256(uint160(_addr)));
    bytes memory alphabet = "0123456789abcdef";

    bytes memory str = new bytes(51);
    str[0] = "0";
    str[1] = "x";
    for (uint i = 0; i < 20; i++) {
        str[2+i*2] = alphabet[uint(uint8(value[i + 12] >> 4))];
        str[3+i*2] = alphabet[uint(uint8(value[i + 12] & 0x0f))];
    }
    return string(str);
}

  // Create a function to be called when contract invoked
  function createPatch(string memory _hPatch, string memory _txHashDC) public {
    PatchCount ++; // Increment State variable

    // Init Patch obj and store it into patches hashmap
    patches[PatchCount] = Patch(PatchCount, _hPatch, _txHashDC);
  }
}
