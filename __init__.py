TOKEN_ABI = [
    {
        "constant": True,
        "inputs": [
            {
                "name": "who",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
	{
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
	{
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

ERC_20_DATA = {
    "erc20Tokens": [
        {
        "address": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
        "coin_name": "WBTC"
        },
        {
        "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
        "coin_name": "USDC"
        },
        {
        "address": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
        "coin_name": "USDC.e"
        }
    ]
}

