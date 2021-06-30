from pathlib import Path
import yaml
import click

from brownie import Token, MillennialVault, MillennialAutoCompoundTomb, MillennialAutoCompoundSpirit, MillennialAutoCompoundBoo, Registry, accounts, network, web3, MillennialAutoCompoundPopsicle
from eth_utils import is_checksum_address
from semantic_version import Version


DEFAULT_VAULT_NAME = lambda token: f"{token.symbol()} mlnlVault"
DEFAULT_VAULT_SYMBOL = lambda token: f"mlnl{token.symbol()}"

PACKAGE_VERSION = yaml.safe_load(
    (Path(__file__).parent.parent / "ethpm-config.yaml").read_text()
)["version"]


def get_address(msg: str, default: str = None) -> str:
    val = click.prompt(msg, default=default)

    # Keep asking user for click.prompt until it passes
    while True:

        if is_checksum_address(val):
            return val
        elif addr := web3.ens.address(val):
            click.echo(f"Found ENS '{val}' [{addr}]")
            return addr

        click.echo(
            f"I'm sorry, but '{val}' is not a checksummed address or valid ENS record"
        )
        # NOTE: Only display default once
        val = click.prompt(msg)


def main():
    click.echo(f"You are using the '{network.show_active()}' network")
    dev = accounts.load(click.prompt("Account", type=click.Choice(accounts.load())))
    click.echo(f"You are using: 'dev' [{dev.address}]")

    click.echo(
        f"""
        Release Information

         local package version: {PACKAGE_VERSION}
        """
    )

    spirit_ftm = Token.at("0x30748322b6e34545dbe0788c421886aeb5297789")
    boo_ftm = Token.at("0xEc7178F4C41f346b2721907F5cF7628E388A7a58")
    dai_spirit = Token.at("0xffbfc0446ca725b21256461e214e9d472f9be390")
    ftm_mim = Token.at("0xb32b31dfafbd53e310390f641c7119b5b9ea0488")
    ftm_tomb = Token.at("0x2A651563C9d3Af67aE0388a5c8F89b867038089e")
    ftm_tshare = Token.at("0x4733bc45eF91cF7CcEcaeeDb794727075fB209F2")
    ftm_ice_spooky = Token.at("0x623ee4a7f290d11c11315994db70fb148b13021d")
    ftm_usdc_spirit = Token.at("0xe7E90f5a767406efF87Fdad7EB07ef407922EC1D")
    ftm_fusdt_spooky = Token.at("0x5965e53aa80a0bcf1cd6dbdd72e6a9b2aa047410")
    ftm_wbtc_spooky = Token.at("0xFdb9Ab8B9513Ad9E419Cf19530feE49d412C3Ee3")
    ftm_weth_spooky = Token.at("0xf0702249F4D3A25cD3DED7859a165693685Ab577")

    #tokens = [(spirit_ftm, MillennialAutoCompoundSpirit, 1), (boo_ftm, MillennialAutoCompoundBoo, 0)]
    #tokens = [(boo_ftm, MillennialAutoCompoundBoo, 0)]
    #tokens = [(dai_spirit, MillennialAutoCompoundSpirit, 25)]
    #tokens = [(ftm_mim, MillennialAutoCompoundSpirit, 30)]
    #tokens = [(ftm_tomb, MillennialAutoCompoundTomb, 0), (ftm_tshare, MillennialAutoCompoundTomb, 1)]
    #tokens = [(ftm_ice_spooky, MillennialAutoCompoundPopsicle, 1)]
    #tokens = [(ftm_usdc_spirit, MillennialAutoCompoundSpirit, 4)]
    #tokens = [(ftm_fusdt_spooky, MillennialAutoCompoundBoo, 1)]

    tokens = [(ftm_weth_spooky, MillennialAutoCompoundBoo, 5)]

    gov = dev.address

    rewards = gov
    guardian = gov
    management = gov

    for token, strat, poolId in tokens:
        name = click.prompt(f"Set description", default=DEFAULT_VAULT_NAME(token))
        symbol = click.prompt(f"Set symbol", default=DEFAULT_VAULT_SYMBOL(token))

        click.echo(
            f"""
        Vault Deployment Parameters

        token address: {token.address}
        token symbol: {DEFAULT_VAULT_SYMBOL(token)}
            governance: {gov}
            management: {management}
            rewards: {rewards}
            guardian: {guardian}
            poolId: {poolId}
                name: '{name}'
                symbol: '{symbol}'
        """
        )

        if click.confirm("Deploy New Vault"):
            args = [
                token,
                name if name != DEFAULT_VAULT_NAME(token) else "",
                symbol if symbol != DEFAULT_VAULT_SYMBOL(token) else "",
                12000
            ]
            vault = MillennialVault.deploy(*args, {'from': dev})
            click.echo(f"New {name} Vault Release deployed [{vault.address}]")
            strategy = strat.deploy(token.address, poolId, vault.address, gov, {'from': dev})
            click.echo(f"New {name} Strategy Release deployed [{strategy.address}]")
            vault.initialize(strategy.address, {'from': dev})
