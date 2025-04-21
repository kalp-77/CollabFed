## Overview

This project implements the public blockchain components of **CollabFed**, a decentralized architecture for interfacing private blockchain-based consortia with open consumer networks, as described in the IEEE INFOCOM 2021 paper *Leveraging Public-Private Blockchain Interoperability for Closed Consortium Interfacing*. The implementation focuses on the Ethereum-based smart contracts (User Request Contract and Resource Provisioning Contract) using the **Truffle Suite**, with a roadmap for integrating private blockchain (Hyperledger Fabric or Burrow) and BLS multi-signature mechanisms. The project simulates consumer requests and consortium interactions, measuring metrics like gas consumption and latency, aligning with the paper’s evaluation.

## Project Structure

The project is organized as follows:

- `contracts/`: Contains Solidity smart contracts.
  - `UserRequestContract.sol`: Handles consumer request submission and consortium endorsements.
  - `ResourceProvisioningContract.sol`: Manages consortium responses with simplified signature verification.
- `migrations/`: Deployment scripts for smart contracts.
  - `2_deploy_contracts.js`: Deploys both contracts to Ethereum.
- `test/`: Test scripts for smart contracts.
  - `collabfed.test.js`: Tests request submission, endorsement, and response posting.
- `scripts/`: Simulation scripts for experiments.
  - `simulate.js`: Simulates consumer requests and consortium endorsements.
- `truffle-config.js`: Truffle configuration for Ganache and Ropsten networks.
- `package.json`: Node.js dependencies.
- `README.txt`: This file.

## Prerequisites

- **Operating System**: Ubuntu 20.04 (recommended), macOS, or Windows.
- **Hardware**: 4GB RAM, 2 CPU cores minimum.
- **Software**:
  - Node.js (v18.x or higher): `curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt install -y nodejs`
  - Truffle: `npm install -g truffle`
  - Ganache CLI: `npm install -g ganache-cli`
  - Python 3: `sudo apt install python3 python3-pip -y && pip3 install web3`
  - Git: `sudo apt install git -y`
  - MetaMask browser extension (for Ropsten deployment): metamask.io
  - Infura account: infura.io for Ropsten endpoint.
- **Ropsten ETH**: Fund your MetaMask account via a faucet (e.g., faucet.ropsten.be).

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository_url>  # Replace with this repo URL
   cd collabfed_truffle
   ```

2. **Install Node.js dependencies**:

   ```bash
   npm install
   ```

3. **Configure Truffle**:

   - Open `truffle-config.js` and update:
     - `mnemonic`: Your MetaMask seed phrase (store securely, never commit).
     - `ropsten.provider`: Replace `YOUR_INFURA_PROJECT_ID` with your Infura Project ID.
   - Example:

     ```javascript
     const mnemonic = "your twelve word mnemonic phrase";
     provider: () => new HDWalletProvider(mnemonic, "https://ropsten.infura.io/v3/your_infura_project_id")
     ```

## Running the Project

### 1. Local Testing with Ganache

1. **Start Ganache**:

   ```bash
   ganache-cli -p 8545 -a 10 -e 1000
   ```

   - Creates 10 accounts, each with 1000 ETH.
   - Runs on port 8545.

2. **Deploy contracts**:

   ```bash
   truffle migrate --network development
   ```

   - Deploys `UserRequestContract` and `ResourceProvisioningContract` to Ganache.
   - Note the contract addresses in the output.

3. **Run tests**:

   ```bash
   truffle test
   ```

   - Executes tests in `test/collabfed.test.js` to verify request submission, endorsement, and response posting.

4. **Simulate consumer requests**:

   - Update `scripts/simulate.js` with deployed contract addresses:

     ```javascript
     const userRequestAddress = "0x..."; // From migration output
     const resourceProvisioningAddress = "0x...";
     ```
   - Run:

     ```bash
     node scripts/simulate.js
     ```
   - Simulates 4 consumer requests and endorsements, logging latency and gas usage.

### 2. Deployment to Ropsten Testnet

1. **Fund MetaMask account**:

   - Use a Ropsten faucet to send ETH to your MetaMask account.

2. **Deploy contracts**:

   ```bash
   truffle migrate --network ropsten
   ```

   - Deploys contracts to Ropsten.
   - Note contract addresses.

3. **Interact via Truffle Console**:

   ```bash
   truffle console --network ropsten
   ```

   - Example commands:

     ```javascript
     userRequest = await UserRequestContract.at("0x...");
     await userRequest.submitRequest("VM: 2CPU, 4GB");
     request = await userRequest.getRequest(0);
     console.log(request);
     ```

4. **Run simulation**:

   - Update `scripts/simulate.js` with Ropsten contract addresses and Web3 provider (e.g., Infura endpoint).
   - Run:

     ```bash
     node scripts/simulate.js
     ```

## Measuring Metrics

- **Gas Consumption**:
  - Check gas used in `simulate.js` output (e.g., `receipt.gasUsed`).
  - Compare with CryptoKitties (as in the paper).
- **Latency**:
  - Measure transaction time in `simulate.js` (logged as `Total time`).
  - Run multiple times to capture variability (similar to Figure 5 in the paper).
- **Output**:
  - Results are logged to the console. Redirect to a file for analysis:

    ```bash
    node scripts/simulate.js > results.txt
    ```

## How the Project Was Made

### Design

The project implements the Ethereum-based public blockchain components of CollabFed, focusing on:

- **User Request Contract**: Allows consumers to submit requests (e.g., VM provisioning) and consortium members to endorse them, simulating the paper’s Consensus on Consensus mechanism.
- **Resource Provisioning Contract**: Handles consortium responses with a placeholder for BLS multi-signatures (to be verified off-chain).
- **Simulation**: Mimics 4–64 consumer requests (as in the paper’s experiments) and consortium endorsements, measuring latency and gas.

The implementation aligns with the paper’s use of Ethereum (Ropsten testnet) and Solidity (v0.8.0 for compatibility). Truffle was chosen for its robust smart contract development, testing, and deployment capabilities, with Ganache for local testing and Ropsten for realistic deployment.

### Development Process

1. **Environment Setup**:
   - Installed Node.js, Truffle, and Ganache CLI.
   - Configured Truffle for Ganache (local) and Ropsten (testnet) networks.
2. **Smart Contract Development**:
   - Wrote `UserRequestContract.sol` to handle request submission and endorsements.
   - Wrote `ResourceProvisioningContract.sol` for response posting with simplified signature verification.
   - Used Solidity v0.8.0 for modern features and security.
3. **Testing**:
   - Developed tests in `collabfed.test.js` to verify contract functionality (request submission, endorsement, response posting).
   - Used Mocha/Chai (Truffle defaults) for assertions.
4. **Simulation**:
   - Created `simulate.js` to emulate consumer and consortium interactions, replicating the paper’s 4–64 request experiments.
   - Integrated Web3.js for Ethereum interaction.
5. **Metrics**:
   - Added gas and latency measurements in `simulate.js` to match the paper’s evaluation (Figures 5–6).
6. **Documentation**:
   - Wrote this README to guide setup, execution, and project understanding.

### Limitations

- **Scope**: Currently implements only the public blockchain (Ethereum) components. Private blockchain (Fabric/Burrow) and BLS signatures are planned for future integration.
- **Network Emulation**: Truffle doesn’t emulate network latency (50–400ms in the paper). Use Linux `tc` or a cloud setup for full replication.
- **BLS Signatures**: Simplified placeholder in `ResourceProvisioningContract`; requires off-chain computation with a library like noble-bls12-381.

## Roadmap for Full Implementation

To fully replicate CollabFed:

1. **Private Blockchain**:
   - Deploy Hyperledger Fabric or Burrow:
     - Fabric: `curl -sSL https://bit.ly/2ysbOFE | bash -s`
     - Burrow: `go get github.com/hyperledger/burrow`
   - Implement Propagation and Fair Scheduling Contracts as chaincode (Go/JavaScript).
   - Bridge Ethereum events to Fabric/Burrow using Node.js.
2. **BLS Signatures**:
   - Use noble-bls12-381 for off-chain signature aggregation:

     ```javascript
     const { bls } = require('@noble/bls12-381');
     ```
   - Integrate with `ResourceProvisioningContract` for verification.
   - Simulate M-ary tree collection (Table I in the paper).
3. **Scalability**:
   - Test with 64 consumers and 32 consortium nodes (requires private blockchain setup).
   - Measure latency (\~2.5s for Burrow, \~3.5s for BLS) and resource usage (CPU &lt;10%, memory &lt;200MB).
4. **Network Emulation**:
   - Use Linux `tc` to simulate 50–400ms latency:

     ```bash
     sudo tc qdisc add dev eth0 root netem delay 50ms
     ```
   - Alternatively, deploy on a cloud provider (e.g., AWS) with distributed nodes.

## Troubleshooting

- **Ganache fails to start**: Ensure port 8545 is free (`lsof -i :8545`).
- **Ropsten deployment fails**: Check MetaMask balance and Infura endpoint.
- **Test errors**: Verify contract addresses and account funds in Ganache.
- **Slow Ropsten transactions**: Increase gas price in `truffle-config.js` (e.g., 30 Gwei).

## References

- Paper: *Leveraging Public-Private Blockchain Interoperability for Closed Consortium Interfacing*, IEEE INFOCOM 2021.
- Truffle Documentation: trufflesuite.com
- Ethereum Ropsten: ropsten.etherscan.io


Last updated: April 20, 2025
