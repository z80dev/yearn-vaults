#!/usr/bin/env python3
import click
import time
from brownie import Token, MillennialVault, MillennialAutoCompoundSpirit, MillennialAutoCompoundPopsicle, MillennialAutoCompoundBoo, MillennialAutoCompoundTomb, Registry, accounts, network, web3

SPIRIT_STRATS = ["0xf27556CEE31d4545e4744fDf71f58424FC251AaD", "0x585120EcDF4ed78CE76384389a4aE5f374F00f01", "0xba18b0ba8f71a41cda7c1d3dfa7c9371677786b3", "0xd8b2cc0b9ebb4e029c0c61ca0625cf8ba3d07534"]

SPOOKY_STRATS = ["0x6f9eaFC66A33Ef304A2e24853642Fa1f5187829e", "0xAbd18C951e8bd0Bd3634Ab35a1dAf40Ff6A490dE", "0xd71f7444829421031947C027afe45f1b48A25329", "0xf1F9DF3e4572dd27cc76141f4E59186FEd9dFE04", "0x17d74fb377F2596c8fc8025aA38e14C7ab0aB04e"]

TOMB_STRATS = ["0xd64f6E866262Aa033070C2DD23c0259b8C920a48", "0x66f0b68059f78339E44A2C93D913Bb54A4D6116c"]

POP_STRATS = ["0xF649a6735b542a414d284BbCb9f17eF8Cfb90804"]

def main():
    click.echo(f"You are using the '{network.show_active()}' network")
    dev = accounts.load('harvester')
    click.echo(f"You are using: 'dev' [{dev.address}]")
    while True:
        click.echo("Harvesting Spirit Vaults")
        for s in SPIRIT_STRATS:
            try:
                strategy = MillennialAutoCompoundSpirit.at(s)
                h = strategy.harvest({'from': dev})
                print(h)
            except:
                pass
        click.echo("Harvesting Spooky Vaults")
        for s in SPOOKY_STRATS:
            try:
                strategy = MillennialAutoCompoundBoo.at(s)
                h = strategy.harvest({'from': dev})
                print(h)
            except:
                pass
        click.echo("Harvesting Tomb Vaults")
        for s in TOMB_STRATS:
            try:
                strategy = MillennialAutoCompoundTomb.at(s)
                h = strategy.harvest({'from': dev})
                print(h)
            except:
                pass
        click.echo("Harvesting Popsicle Vaults")
        for s in POP_STRATS:
            try:
                strategy = MillennialAutoCompoundPopsicle.at(s)
                h = strategy.harvest({'from': dev})
                print(h)
            except:
                pass
        time.sleep(600)
