pragma solidity ^0.5.0;

contract Enrollment {
  uint public EnrollmentCount; // State Variable similar to Static

  struct Enrollment {
    uint id;
    string vendorName;
    string puv; // sha256 checksum
    string bpuv; // ETH wallet address
  }

  // mapping is a hash datastruc where uint is the key, Enrollment is the value
  // mapping datastruc serves as a DB index method
  mapping(uint => Enrollment) public enrollments;

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

  // When we deploy contract to ledger, it will init a default enrollment
  // constructor() public {
  //   string memory daName = "DistributorAuthority";
  //   string memory  puDA = "81294bb551beec628ed8bf38927e8489b7322d9c43d1235bb7d481917a91c305";
  //   address bpuDAaddr = 0x3781f7B2cC44BeF32B6D532561A84A5726Ecd44d;
  //   string memory bpuDA = addrToStr(bpuDAaddr); // Arbitrary ganache wallet address
  //   createEnrollment(daName, puDA, bpuDA);
  // }

  // Create a function to be called when contract invoked
  function createEnrollment(string memory _vendorName, string memory _puv, string memory _bpuv) public {
    EnrollmentCount ++; // Increment State variable

    // Init Enrollment obj and store it into enrollments hashmap
    enrollments[EnrollmentCount] = Enrollment(EnrollmentCount, _vendorName, _puv, _bpuv);
  }
}
