FROM hyperledger/fabric-peer:2.2

# Install required packages using Alpine's package manager (apk)
RUN apk update && apk add --no-cache \
    nodejs \
    npm \
    python3 \
    py3-pip \
    curl \
    bash \
    git

# Install Truffle for Ethereum smart contract development
RUN npm install -g truffle

# Install Python libraries
RUN pip3 install web3 bls flask

# Copy application code to container
COPY . /app

# Set working directory
WORKDIR /app

