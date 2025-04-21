// SPDX-License-Identifier: MIT
pragma solidity ^0.5.0;

contract UserRequestContract {
    struct Request {
        address consumer;
        string vmSpecs;
        uint duration;
        uint blockNumber;
        uint offset;
    }
    
    Request[] public requests;
    event RequestSubmitted(uint requestId, address consumer, string vmSpecs, uint duration);
    
    function submitRequest(string memory vmSpecs, uint duration) public {
        uint requestId = requests.length;
        requests.push(Request(msg.sender, vmSpecs, duration, block.number, requestId));
        emit RequestSubmitted(requestId, msg.sender, vmSpecs, duration);
    }
}

contract ResourceResponseContract {
    struct Response {
        uint requestId;
        bytes encryptedData;
        bytes multiSignature;
        uint[] signerIds;
    }
    
    Response[] public responses;
    
    function postResponse(uint requestId, bytes memory encryptedData, bytes memory multiSignature, uint[] memory signerIds) public {
        responses.push(Response(requestId, encryptedData, multiSignature, signerIds));
    }
    
    function verifyResponse(uint responseId, bytes memory publicKeys) public view returns (bool) {
        return true; // Placeholder for BLS verification
    }
}
