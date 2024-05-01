from gmx_abstract.utils import (
    configure,
    position_are_the_same,
    get_erc20tokens,
    get_eth_balance
)
from gmx_abstract.models import Position, TokenBalance
from gmx_abstract.errors import PositionFetchError
from typing import List, Iterator, Tuple
from gmx_python_sdk.scripts.v2.get.get_open_positions import GetOpenPositions
from gmx_python_sdk.scripts.v2.order.create_deposit_order import DepositOrder
from gmx_python_sdk.scripts.v2.order.liquidity_argument_parser import LiquidityArgumentParser


from time import sleep
from datetime import datetime
import requests
from web3 import Web3


class GmxClient:
    """
    A client for interacting with GMX positions through the Ethereum blockchain.

    Attributes:
        address (str): The Ethereum address associated with the client.
        rpc_url (str): The RPC URL used to connect to the Ethereum network.

    Methods:
        get_positions(address): Retrieves open positions for a specified Ethereum address.
        get_my_positions(): Retrieves open positions associated with the client's Ethereum address.
        poll_positions(address, wait_seconds): Periodically checks for changes in positions at a specified Ethereum address.
    """

    def __init__(self, address: str, private_key: str, rpc_url: str):
        """
        Initializes the GmxClient with an Ethereum address, private key, and RPC URL.

        Parameters:
            address (str): The Ethereum address to associate with this client.
            private_key (str): The private key for the Ethereum address, used to configure API access.
            rpc_url (str): The RPC URL to connect to the Ethereum network.
        """
        configure(private_key, address, rpc_url)
        self.address = address
        self.rpc_url = rpc_url
        self.web3_client = Web3(Web3.HTTPProvider(rpc_url))
        if not self.web3_client.is_connected():
            raise ValueError("Invalid RPC URL")

    def get_positions(self, address: str) -> List[Position]:
        """
        Fetches open positions for a specified Ethereum address.

        Parameters:
            address (str): The Ethereum address to retrieve positions for.

        Returns:
            List[Position]: A list of Position objects representing the open positions.

        Raises:
            PositionFetchError: If there is an error in fetching positions due to a JSON decode error.
        """
        try:
            positions = GetOpenPositions(chain='arbitrum', address=address)
            return [Position(position_id=key, data=data) for key, data in positions.get_data().items()]
        except NameError:
            return []
        except requests.exceptions.JSONDecodeError as e:
            raise PositionFetchError(e.request, e.response)

    def get_my_positions(self) -> List[Position]:
        """
        Retrieves open positions associated with the client's Ethereum address.

        Returns:
            List[Position]: A list of Position objects representing the open positions.
        """
        return self.get_positions(self.address)
    
    def poll_positions(self, address: str, wait_seconds: int, debug : bool = False) -> Iterator[Tuple[List[Position], List[Position]]]:
        """
        Periodically checks and emits changes in positions for a specified Ethereum address.

        Parameters:
            address (str): The Ethereum address to poll for changes in positions.
            wait_seconds (int): The interval, in seconds, between each poll.

        Yields:
            Tuple[List[Position], List[Position]]: A tuple containing lists of Position objects before and after changes detected.

        Notes:
            This function runs indefinitely until manually stopped. It tracks the duration of each poll cycle and logs the time taken.
        """
        last_positions = self.get_positions(address=address)
        rounds = 0
        while True:
            sleep(wait_seconds)
            start = datetime.now()
            try:
                new_positions = self.get_positions(address=address)
                rounds += 1
                if not position_are_the_same(last_positions, new_positions):
                    yield (last_positions, new_positions)
                last_positions = new_positions
            except PositionFetchError as e:
                if debug:
                    print('Error during position fetch:', e)
            except Exception as e:
                if debug:
                    print('Unexpected error:', e)

            end = datetime.now()
            if debug:
                print(f"{rounds} - took {(end - start).total_seconds()} seconds ({self.rpc_url})")

    def get_collateral_balances(self, address: str) -> List[TokenBalance]:
        """
        Retrieves the balance of ERC20 tokens and Ether for a given address.

        This function fetches balances of all ERC20 tokens associated with the provided address
        using the `get_erc20tokens` method, and adds the Ether balance. The balance of Ether is 
        retrieved by the `get_eth_balance` method, and represented as a `TokenBalance` object
        with an empty `contract_id` to distinguish it from ERC20 tokens.

        Parameters:
        - address (str): The Ethereum address to query the balances for.

        Returns:
        - List[TokenBalance]: A list of `TokenBalance` objects, each representing the balance 
        of a specific token (ERC20 or Ether) at the given address.
        """
        return get_erc20tokens(self.web3_client, address) + [
            TokenBalance(
                balance=get_eth_balance(w3=self.web3_client, address=address),
                contract_id="",
                name="ETH"
            )
        ]

    def get_my_collateral_balances(self) -> List[TokenBalance]:
        """
        Retrieves the collateral balances (ERC20 tokens and Ether) for the user's address.

        This function acts as a convenience wrapper around `get_collateral_balances` by
        directly using the user's stored address to fetch the balances. It simplifies
        access to collateral balances for the predefined user address.

        Returns:
        - List[TokenBalance]: A list of `TokenBalance` objects, each representing the balance 
        of a specific token (ERC20 or Ether) at the user's address.
        """
        return self.get_collateral_balances(self.address)
