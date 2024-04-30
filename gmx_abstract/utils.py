from gmx_python_sdk.scripts.v2.gmx_utils import Config, get_config
from gmx_abstract.models import Position, TokenBalance
from typing import List, Tuple
from web3 import Web3
from gmx_abstract import TOKEN_ABI, ERC_20_DATA

def configure(private_key: str, address: str, rpc_url: str):
    """
    Configures the GMX trading environment with specified user credentials and blockchain RPC details.

    Parameters:
    ----------
    private_key : str
        The private key of the user's wallet.
    address : str
        The public address of the user's wallet.
    rpc_url : str
        The RPC URL of the Arbitrum blockchain to connect to.

    Returns:
    -------
    None
        Modifies the configuration in place by updating or setting the user's configuration.
    """
    config_data ={
        "arbitrum": {
            "rpc": rpc_url,
            "chain_id": "42161"
        },
        "avalanche": {
            "rpc": "https://api.avax.network/ext/bc/C/rpc",
            "chain_id": "43114"
        },

        "private_key": private_key,
        "user_wallet_address": address
    }

    config_object = Config()

    new_config = config_object.load_config()

    for key in config_data:
        new_config[key] = config_data[key]

    config_object.set_config(new_config)


def position_are_the_same(old_positions: List[Position], new_positions: List[Position]) -> bool:
    """
    Determines whether two lists of positions are identical.

    Parameters:
    ----------
    old_positions : List[Position]
        The list of initial trading positions.
    new_positions : List[Position]
        The list of updated trading positions to compare against.

    Returns:
    -------
    bool
        True if both lists contain the same positions, False otherwise.
    """
    if len(old_positions) != len(new_positions):
        return False
    
    for old_position in old_positions:
        if not old_position in new_positions:
            return False
        
    return True


def determine_added_and_removed_positions(old_positions: List[Position], new_positions: List[Position]) \
    -> Tuple[List[Position], List[Position]]:
    """
    Identifies positions that have been added or removed when comparing two lists of trading positions.

    Parameters:
    ----------
    old_positions : List[Position]
        The list of original trading positions.
    new_positions : List[Position]
        The list of new trading positions to compare against.

    Returns:
    -------
    Tuple[List[Position], List[Position]]
        A tuple containing two lists: positions that have been added and positions that have been removed.
    """
    added_positions = []
    removed_positions = []

    old_position_ids = [ position.position_id for position in old_positions ]
    new_position_ids = [ position.position_id for position in new_positions ]

    for position in old_positions:
        if position.position_id not in new_position_ids:
            removed_positions.append(position)

    for position in new_positions:
        if position.position_id not in old_position_ids:
            added_positions.append(position)

    return added_positions, removed_positions


def get_erc20tokens(w3: Web3, address: str) -> List[TokenBalance]:
    """
    Retrieves the token balances for a specified address from a predefined list of ERC-20 tokens.

    Args:
    w3 (Web3): An instance of Web3 to interact with the Ethereum blockchain.
    address (str): The Ethereum address from which the token balances will be retrieved.

    Returns:
    List[TokenBalance]: A list of TokenBalance objects, each containing the balance, name,
                        and contract ID for each ERC-20 token.
    """
    token_balances = []

    decimals = 18  # Default decimals set to 18

    for contract_info in ERC_20_DATA.get("erc20Tokens", []):
        token_address = contract_info.get("address")
        coin_name = contract_info.get("coin_name")

        checksum_address = w3.to_checksum_address(token_address)

        token_contract = w3.eth.contract(checksum_address, abi=TOKEN_ABI)

        decimals = token_contract.functions.decimals().call()

        balance_wei = token_contract.functions.balanceOf(w3.to_checksum_address(address)).call()
        balance_token_units = balance_wei / 10 ** decimals

        token_balances.append(
            TokenBalance(
                balance=balance_token_units,
                name=coin_name,
                contract_id=token_address
            )
        )

    return token_balances

def get_eth_balance(w3: Web3, address: str) -> float:
    """
    Retrieves the Ether balance for a specified address.

    Args:
    w3 (Web3): An instance of Web3 to interact with the Ethereum blockchain.
    address (str): The Ethereum address from which the Ether balance will be retrieved.

    Returns:
    float: The Ether balance of the specified address.
    """
    checksum_address = w3.to_checksum_address(address)
    balance_wei = w3.eth.get_balance(checksum_address)
    balance = w3.from_wei(balance_wei, 'ether')

    return balance
