# GMX Client Documentation

## Overview

The GMX Client is designed to interact with GMX positions on the Ethereum blockchain. It provides various functionalities, including retrieving and polling open positions, and managing collateral balances of ERC20 tokens and Ether. This client uses an RPC URL to connect to the Ethereum network, allowing users to operate directly with blockchain data.

## Features

### Ethereum Connection
Upon initialization, the client requires an Ethereum address, a private key for API access, and an RPC URL to establish a connection to the Ethereum network. It ensures that the connection is valid and raises an error if the RPC URL is invalid.

### Position Management
- **Get Positions**: Fetch open positions for any Ethereum address. It returns a list of positions or raises an error if there are issues during the fetch process.
- **Get My Positions**: Fetch open positions associated with the client's Ethereum address. This is a convenience function that internally calls `get_positions` with the client's address.
- **Poll Positions**: Periodically checks for changes in positions for a specified Ethereum address and emits the positions before and after any detected changes. This function runs indefinitely until manually stopped and is useful for monitoring position updates in real-time.

### Collateral Balances
- **Get Collateral Balances**: Retrieve the balance of ERC20 tokens and Ether for a given Ethereum address. It combines ERC20 token balances with the Ethereum balance, presenting them in a unified list.
- **Get My Collateral Balances**: A convenience function that fetches collateral balances (ERC20 tokens and Ether) for the user's address, simplifying the retrieval process for the predefined user address.

## Usage
The GMX Client is initialized with an Ethereum address and private key, ensuring secure and direct interaction with the Ethereum blockchain through the specified RPC URL. It supports various operations crucial for managing positions and balances on the Ethereum blockchain, making it an essential tool for users interacting with the GMX platform.

## Notes
This client provides robust error handling to manage common issues such as connection errors and data fetch problems, ensuring reliability during blockchain interactions. It is designed for continuous operation, as evidenced by its capability to poll positions indefinitely, making it ideal for applications that require real-time data monitoring.