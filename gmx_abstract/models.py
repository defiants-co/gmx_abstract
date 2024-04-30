class Position:
    """
    A class to represent a trading position.

    Attributes:
    -----------
    position_id : str
        Unique identifier for the trading position. (example: BTC_long, ETH_short)
    account : str
        Account identifier where the position is held.
    market : str
        The trading market for the position.
    market_symbol : str
        The symbol representing the trading market.
    collateral_token : str
        The token used as collateral for the position.
    position_size : float
        The size of the position.
    size_in_tokens : float
        The size of the position measured in tokens.
    entry_price : float
        The price at which the position was entered.
    initial_collateral_amount : float
        Initial amount of collateral deposited for the position.
    initial_collateral_amount_usd : float
        Initial amount of collateral in USD.
    leverage : float
        Leverage applied to the position.
    borrowing_factor : float
        Factor by which the position is leveraged in terms of borrowing.
    funding_fee_amount_per_size : float
        Funding fee applied per unit size of the position.
    long_token_claimable_funding_amount_per_size : float
        Claimable funding amount per unit size for long positions.
    short_token_claimable_funding_amount_per_size : float
        Claimable funding amount per unit size for short positions.
    position_modified_at : str
        Timestamp of the last modification of the position.
    is_long : bool
        True if the position is long, False if it is short.
    percent_profit : float
        Percentage of profit or loss on the position.
    mark_price : float
        Current market price of the position's asset.

    Methods:
    --------
    __init__(self, data, position_id)
        Initializes the Position object with the given data and position ID.
    __repr__(self)
        Returns a formatted string representation of the Position object.
    __eq__(self, other)
        Compares this position with another to check for equality.
    __sub__(self, other)
        Subtracts one position from another to create a PositionDelta.
    json(self)
        Serializes the object to a JSON-compatible dictionary representation.
    """
    def __init__(self, data, position_id):
        """
        Initializes the attributes of the Position class with data retrieved
        from a dictionary based on the position_id.
        """
        self.position_id = position_id
        self.account = data['account']
        self.market = data['market']
        self.market_symbol = data['market_symbol'][0]
        self.collateral_token = data['collateral_token']
        self.position_size = data['position_size']
        self.size_in_tokens = data['size_in_tokens']
        self.entry_price = data['entry_price']
        self.initial_collateral_amount = data['inital_collateral_amount']
        self.initial_collateral_amount_usd = data['inital_collateral_amount_usd'][0]
        self.leverage = data['leverage']
        self.borrowing_factor = data['borrowing_factor']
        self.funding_fee_amount_per_size = data['funding_fee_amount_per_size']
        self.long_token_claimable_funding_amount_per_size = data['long_token_claimable_funding_amount_per_size']
        self.short_token_claimable_funding_amount_per_size = data['short_token_claimable_funding_amount_per_size']
        self.position_modified_at = data['position_modified_at']
        self.is_long = data['is_long']
        self.percent_profit = data['percent_profit']
        self.mark_price = data['mark_price']

    def __repr__(self):
        """
        Returns a string representation of the Position object, including
        the position ID and key position attributes for quick reference.
        """
        return (f"Position(position_id={self.position_id!r}, market={self.market!r}, "
                f"market_symbol={self.market_symbol!r}, entry_price={self.entry_price}, "
                f"position_size={self.position_size}, is_long={self.is_long}, "
                f"mark_price={self.mark_price})")
    def __eq__(self, other):
        """
        Compares this position with another position to check for equality.

        Parameters:
        -----------
        other : Position
            The other position to compare against.

        Returns:
        --------
        bool
            True if all attributes of both positions are the same, considering
            floating point precision for numeric values; otherwise, False.

        Notes:
        ------
        The comparison checks for the exact match of string attributes and an
        almost equality (considering floating point precision) for float attributes.

        The comparison also goes beyond checking if the position id's are the same. 
        If you want to find one position in another list where the underlying amounts
        have changed, use self.position_id == other.position_id instead of equals.
        """
        if not isinstance(other, Position):
            return False
        
        return (
            self.account == other.account and
            self.market == other.market and
            self.market_symbol == other.market_symbol and
            self.collateral_token == other.collateral_token and
            abs(self.position_size - other.position_size) < 1e-10 and
            self.size_in_tokens == other.size_in_tokens and
            abs(self.entry_price - other.entry_price) < 1e-6 and
            self.initial_collateral_amount == other.initial_collateral_amount and
            self.initial_collateral_amount_usd == other.initial_collateral_amount_usd and
            abs(self.leverage - other.leverage) < 1e-6 and
            self.borrowing_factor == other.borrowing_factor and
            self.funding_fee_amount_per_size == other.funding_fee_amount_per_size and
            self.long_token_claimable_funding_amount_per_size == other.long_token_claimable_funding_amount_per_size and
            self.short_token_claimable_funding_amount_per_size == other.short_token_claimable_funding_amount_per_size and
            self.position_modified_at == other.position_modified_at and
            self.is_long == other.is_long # and
            # abs(self.percent_profit - other.percent_profit) < 1e-6 and
            # abs(self.mark_price - other.mark_price) < 1e-6
        )

    def __sub__(self, other):
        """
        Subtracts one position from another to create a PositionDelta, representing the change between them.

        Parameters:
        -----------
        other : Position
            The position to subtract from this position.

        Returns:
        --------
        PositionDelta
            A new PositionDelta object showing the differences between the two positions.

        Raises:
        ------
        ValueError
            If the positions do not have the same position_id or if 'other' is not an instance of Position.

        Notes:
        ------
        The method is intended for positions with the same position_id, ensuring they are comparable.
        """
        if not isinstance(other, Position):
            raise ValueError("Positions can only be subtracted from other positions")

        if not self.position_id == other.position_id:
            raise ValueError("Positions must have the same id (market and direction) to be comparable")

        return PositionDelta(self, other)

    def json(self):
        """
        Serializes the Position object to a JSON-compatible dictionary representation.

        Returns:
        --------
        dict
            A dictionary containing all attributes of the Position object with keys matching
            the attribute names and values representing the current state of the object.

        Notes:
        ------
        This method is useful for converting the position's state into a format that can be
        easily exported or used in APIs, ensuring that all numerical and string attributes
        are directly translatable into JSON format.
        """
        return {
            "position_id": self.position_id,
            "account": self.account,
            "market": self.market,
            "market_symbol": self.market_symbol,
            "collateral_token": self.collateral_token,
            "position_size": self.position_size,
            "size_in_tokens": self.size_in_tokens,
            "entry_price": self.entry_price,
            "initial_collateral_amount": self.initial_collateral_amount,
            "initial_collateral_amount_usd": self.initial_collateral_amount_usd,
            "leverage": self.leverage,
            "borrowing_factor": self.borrowing_factor,
            "funding_fee_amount_per_size": self.funding_fee_amount_per_size,
            "long_token_claimable_funding_amount_per_size": self.long_token_claimable_funding_amount_per_size,
            "short_token_claimable_funding_amount_per_size": self.short_token_claimable_funding_amount_per_size,
            "position_modified_at": self.position_modified_at,
            "is_long": self.is_long,
            "percent_profit": self.percent_profit,
            "mark_price": self.mark_price
        }


class PositionDelta:
    """
    A class to represent the delta (change) between two trading positions.

    Attributes:
    -----------
    delta_collateral_amount : float
        Change in the initial collateral amount.
    delta_collateral_amount_usd : float
        Change in the initial collateral amount in USD.
    delta_leverage : float
        Change in leverage.
    delta_percent_profit : float
        Change in percentage of profit or loss.
    delta_mark_price : float
        Change in the market price of the position's asset.

    Methods:
    --------
    __init__(self, initial_position, new_position)
        Initializes the PositionDelta object with two Position instances.
    __repr__(self)
        Return a formatted string representation of the PositionDelta object.
    """
    def __init__(self, initial_position: Position, new_position: Position):
        """
        Initializes the attributes of the PositionDelta class by calculating the
        differences between corresponding attributes of initial_position and
        new_position. This includes the collateral amount, collateral amount in USD,
        and leverage.
        """
        self.position_id = new_position.position_id
        self.delta_collateral_amount =  initial_position.initial_collateral_amount - new_position.initial_collateral_amount
        self.delta_collateral_amount_usd = initial_position.initial_collateral_amount_usd - new_position.initial_collateral_amount_usd
        self.delta_leverage = initial_position.leverage - new_position.leverage

    def __repr__(self):
        """
        Returns a string representation of the PositionDelta object, showing key differences
        such as the delta in collateral amount, collateral amount in USD, and leverage.
        This helps in quickly understanding the changes between two position states.
        """
        return (f"PositionDelta(initial_position_id={self.position_id}, "
                f"delta_collateral_amount={self.delta_collateral_amount}, "
                f"delta_collateral_amount_usd={self.delta_collateral_amount_usd:.2f}, "
                f"delta_leverage={self.delta_leverage:.2f}, "
        )

class TokenBalance:
    """
    A class to represent the balance of a specific token.

    Attributes:
        balance (int): The balance of the token.
        contract_id (str): The unique identifier of the token's contract.
        name (str): The name of the token.

    Methods:
        __str__(self): Returns a human-readable string representation of the TokenBalance.
    """

    def __init__(self, balance, contract_id, name):
        """
        Constructs all the necessary attributes for the TokenBalance object.

        Parameters:
            balance (float): The balance of the token.
            contract_id (str): The unique identifier of the token's contract.
            name (str): The name of the token.
        """
        self.balance = balance
        self.contract_id = contract_id
        self.name = name

    def __repr__(self):
        """
        String representation of the TokenBalance instance.

        Returns:
            str: A string that represents the TokenBalance object.
        """
        return f"TokenBalance(name={self.name}, contract_id={self.contract_id}, balance={self.balance})"

    def __str__(self):
        """
        String representation of the TokenBalance instance.

        Returns:
            str: A string that represents the TokenBalance object.
        """

        return self.__repr__()