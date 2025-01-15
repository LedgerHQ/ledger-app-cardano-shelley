# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2024 Ledger SAS
# SPDX-License-Identifier: LicenseRef-LEDGER
"""
This module provides Ragger tests for Address check
"""

from typing import List, Optional
from dataclasses import dataclass

from ragger.navigator import NavInsID

from application_client.app_def import NetworkDesc, AddressType, Mainnet, Testnet, FakeNet


@dataclass
class DeriveAddressTestCase:
    name: str
    netDesc: NetworkDesc
    addrType: AddressType
    spendingValue: str      # spending path or keyHash
    stakingValue: str = ""  # staking path or keyHash
    result: str = ""
    nano_nav_confirm: Optional[List[NavInsID]] = None  # list of specific navigation instructions for Nano
    nano_nav_show: Optional[List[NavInsID]] = None  # list of specific navigation instructions for Nano


def pointer_to_str(blockIndex: int, txIndex: int, certificateIndex: int) -> str:
    data: str = ""
    data += f"{blockIndex.to_bytes(4, 'big').hex()}"
    data += f"{txIndex.to_bytes(4, 'big').hex()}"
    data += f"{certificateIndex.to_bytes(4, 'big').hex()}"
    return data


# pylint: disable=line-too-long
byronTestCases = [
    DeriveAddressTestCase("Mainnet 1",
                  Mainnet,
                  AddressType.BYRON,
                  "m/44'/1815'/1'/0/55'",
                  "",
                  "Ae2tdPwUPEZELF6oijm8VFmhWpujnNzyG2zCf4RxfhmWqQKHo2drRD5Uhah"),
    DeriveAddressTestCase("Mainnet 2",
                  Mainnet,
                  AddressType.BYRON,
                  "m/44'/1815'/1'/0/12'",
                  "",
                  "Ae2tdPwUPEYyiPZzoMSN9GJMNZnn3S6ZAErrezee9s1bH6tjaX6m9Cyf3Wy"),
    DeriveAddressTestCase("Mainnet 3",
                  Mainnet,
                  AddressType.BYRON,
                  "m/44'/1815'/101'/0/12'",
                  "",
                  "Ae2tdPwUPEZ8DtpNK9twc8YXCoJ39Uwzc2FWqo1KvGsB8Kvhk14buuESy6g"),
    DeriveAddressTestCase("Mainnet 4",
                  Mainnet,
                  AddressType.BYRON,
                  "m/44'/1815'/0'/0/1000001'",
                  "",
                  "Ae2tdPwUPEZFxaTJw6iova9Crfc3QuoRJSdudsp5z5a9Ee7gQH7oNKrM6cW"),
    DeriveAddressTestCase("Testnet 1",
                  Testnet,
                  AddressType.BYRON,
                  "m/44'/1815'/1'/0/12'",
                  "",
                  "2657WMsDfac5GGdHMD6sR22tyhmFvuPrBZ79hvEvuisyUK9XCcB3nu8JecKuCXEkr"),
]


rejectTestCases = [
    DeriveAddressTestCase("path too short",
             Mainnet,
             AddressType.BYRON,
             "m/44'/1815'/1'"),
    DeriveAddressTestCase("invalid path",
             Mainnet,
             AddressType.BYRON,
             "m/44'/1815'/1'/5/10'"),
    DeriveAddressTestCase("Byron with Shelley path",
             Mainnet,
             AddressType.BYRON,
             "m/1852'/1815'/1'/0/10"),
    DeriveAddressTestCase("base key/key with Byron spending path",
             Mainnet,
             AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
             "m/44'/1815'/1'/0/1",
             "m/1852'/1815'/1'/2/0"),
    DeriveAddressTestCase("base key/key with wrong spending path",
             Mainnet,
             AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
             "m/1852'/1815'/1'/2/0",
             "m/1852'/1815'/1'/2/0"),
    DeriveAddressTestCase("base key/key with wrong staking path 1",
             Mainnet,
             AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
             "m/1852'/1815'/1'/0/0",
             "m/1852'/1815'/1'/0/1"),
    DeriveAddressTestCase("base key/script with Byron spending path",
             Mainnet,
             AddressType.BASE_PAYMENT_KEY_STAKE_SCRIPT,
             "m/44'/1815'/1'/0/1",
             "222a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277"),
    DeriveAddressTestCase("base address scripthash/keyhash not allowed",
             Mainnet,
             AddressType.BASE_PAYMENT_SCRIPT_STAKE_KEY,
             "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
             "222a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277"),
    DeriveAddressTestCase("pointer with Byron spending path",
             Mainnet,
             AddressType.POINTER_KEY,
             "m/44'/1815'/1'/0/0",
             pointer_to_str(1, 2, 3)),
    DeriveAddressTestCase("pointer with wrong spending path",
             Mainnet,
             AddressType.POINTER_KEY,
             "m/1852'/1815'/1'/2/0",
             pointer_to_str(1, 2, 3)),
    DeriveAddressTestCase("enterprise with Byron spending path",
             Mainnet,
             AddressType.ENTERPRISE_KEY,
             "m/44'/1815'/1'/0/0"),
    DeriveAddressTestCase("enterprise with wrong spending path",
             Mainnet,
             AddressType.ENTERPRISE_KEY,
             "m/1852'/1815'/1'/2/0"),
]


shelleyTestCasesNoConfirm = [
    DeriveAddressTestCase("base address path/path 1",
                    FakeNet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
                    "m/1852'/1815'/0'/0/1",
                    "m/1852'/1815'/0'/2/0",
                    "addr1qdd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63vcayfawlf9hwv2fzuygt2km5v92kvf8e3s3mk7ynxw77cwqdquehe",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/path 2",
                    Testnet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
                    "m/1852'/1815'/0'/0/1",
                    "m/1852'/1815'/0'/2/0",
                    "addr_test1qpd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63vcayfawlf9hwv2fzuygt2km5v92kvf8e3s3mk7ynxw77cwq9nnhk4",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] * 2 + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/path multidelegation stake key usual",
                    Testnet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
                    "m/1852'/1815'/0'/0/1",
                    "m/1852'/1815'/0'/2/60",
                    "addr_test1qpd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63vl404mjsaz2xyzvegxxrpx5ltrjgy4qws4ataqtv5lp2h3q30eyjm",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] * 2 + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/keyHash 1",
                    Testnet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
                    "m/1852'/1815'/0'/0/1",
                    "1d227aefa4b773149170885aadba30aab3127cc611ddbc4999def61c",
                    "addr_test1qpd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63vcayfawlf9hwv2fzuygt2km5v92kvf8e3s3mk7ynxw77cwq9nnhk4",
                    nano_nav_show=[NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] * 2 + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/keyHash 2",
                    FakeNet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
                    "m/1852'/1815'/0'/0/1",
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "addr1qdd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63vcj922xhxkn6twlq2wn4q50q352annk3903tj00h45mgfmswz93l5",
                    nano_nav_show=[NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address scriptHash/path",
                    FakeNet,
                    AddressType.BASE_PAYMENT_SCRIPT_STAKE_KEY,
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "m/1852'/1815'/0'/2/0",
                    "addr1zvfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yacayfawlf9hwv2fzuygt2km5v92kvf8e3s3mk7ynxw77cwq8dxrpu",
                    nano_nav_show=[NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address scriptHash/path multidelegation",
                    FakeNet,
                    AddressType.BASE_PAYMENT_SCRIPT_STAKE_KEY,
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "m/1852'/1815'/0'/2/3",
                    "addr1zvfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yauc4nklr34kj8uk8kfgz3lkv6tu0ndr3x0rp3snqdayaxgqwrgxu2",
                    nano_nav_show=[NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/scriptHash",
                    FakeNet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_SCRIPT,
                    "m/1852'/1815'/0'/0/1",
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "addr1ydd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63vcj922xhxkn6twlq2wn4q50q352annk3903tj00h45mgfmssu7w24",
                    nano_nav_show=[NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address scriptHash/scriptHash",
                    FakeNet,
                    AddressType.BASE_PAYMENT_SCRIPT_STAKE_SCRIPT,
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "addr1xvfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yacj922xhxkn6twlq2wn4q50q352annk3903tj00h45mgfms63y5us",
                    nano_nav_show=[NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("enterprise path 1",
                    Testnet,
                    AddressType.ENTERPRISE_KEY,
                    "m/1852'/1815'/0'/0/1",
                    "",
                    "addr_test1vpd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63vc7t2fks",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("enterprise path 2",
                    FakeNet,
                    AddressType.ENTERPRISE_KEY,
                    "m/1852'/1815'/0'/0/1",
                    "",
                    "addr1vdd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63vc9wh7em",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("enterprise script 1",
                    Testnet,
                    AddressType.ENTERPRISE_SCRIPT,
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "",
                    "addr_test1wqfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yacn4n6n2",
                    nano_nav_show=[NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("enterprise script 2",
                    FakeNet,
                    AddressType.ENTERPRISE_SCRIPT,
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "",
                    "addr1wvfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yacgswdup",
                    nano_nav_show=[NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("pointer path 1",
                    Testnet,
                    AddressType.POINTER_KEY,
                    "m/1852'/1815'/0'/0/1",
                    pointer_to_str(1, 2, 3),
                    "addr_test1gpd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63vcpqgpsg6s2p6",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("pointer path 2",
                    FakeNet,
                    AddressType.POINTER_KEY,
                    "m/1852'/1815'/0'/0/1",
                    pointer_to_str(24157, 177, 42),
                    "addr1gdd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63vuph3wczvf288aeyu",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("pointer path 3",
                    FakeNet,
                    AddressType.POINTER_KEY,
                    "m/1852'/1815'/0'/0/1",
                    pointer_to_str(0, 0, 0),
                    "addr1gdd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63vcqqqqqnnd32q",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("pointer script 1",
                    Testnet,
                    AddressType.POINTER_SCRIPT,
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    pointer_to_str(1, 2, 3),
                    "addr_test12qfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yacpqgpsrwzzw9",
                    nano_nav_show=[NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("pointer script 2",
                    FakeNet,
                    AddressType.POINTER_SCRIPT,
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    pointer_to_str(24157, 177, 42),
                    "addr12vfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yauph3wczvf2sykph7",
                    nano_nav_show=[NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("pointer script 3",
                    FakeNet,
                    AddressType.POINTER_SCRIPT,
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    pointer_to_str(0, 0, 0),
                    "addr12vfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yacqqqqqc8le9l",
                    nano_nav_show=[NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("reward path 1",
                    Testnet,
                    AddressType.REWARD_KEY,
                    "",
                    "m/1852'/1815'/0'/2/0",
                    "stake_test1uqwjy7h05jmhx9y3wzy94td6xz4txynuccgam0zfn800v8q8mmqwc",
                    nano_nav_show=[NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("reward path 2",
                    FakeNet,
                    AddressType.REWARD_KEY,
                    "",
                    "m/1852'/1815'/0'/2/0",
                    "stake1uvwjy7h05jmhx9y3wzy94td6xz4txynuccgam0zfn800v8qqucf2t",
                    nano_nav_show=[NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("reward multidelegation usual",
                    Testnet,
                    AddressType.REWARD_KEY,
                    "",
                    "m/1852'/1815'/0'/2/1",
                    "stake_test1uqktgr9psuz0fxggkx9ald8wu8kgpckr2d9kjfxrum6sm3qp87652",
                    nano_nav_show=[NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("reward script 1",
                    Testnet,
                    AddressType.REWARD_SCRIPT,
                    "",
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "stake_test17qfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yacnadzyq",
                    nano_nav_show=[NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("reward script 2",
                    FakeNet,
                    AddressType.REWARD_SCRIPT,
                    "",
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "stake17vfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yac56wtqn",
                    nano_nav_show=[NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
]

nav_inst_1 = [NavInsID.BOTH_CLICK] * 3 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2
nav_inst_2 = [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 3

shelleyTestCasesWithConfirm = [
    DeriveAddressTestCase("base address path/path unusual spending path account",
                    FakeNet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
                    "m/1852'/1815'/101'/0/1",
                    "m/1852'/1815'/0'/2/0",
                    "addr1qv6dcymepkghuyt0za9jxg5hn89art9y8yjcvhxclxdhndsayfawlf9hwv2fzuygt2km5v92kvf8e3s3mk7ynxw77cwqdqq9xn",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 3 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/path unusual spending path address index",
                    FakeNet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
                    "m/1852'/1815'/1'/0/1000001",
                    "m/1852'/1815'/0'/2/0",
                    "addr1q08rwk27cdm6vcp272pqcwq3t3gzea0q5xws2z84zzejrkcayfawlf9hwv2fzuygt2km5v92kvf8e3s3mk7ynxw77cwq2cxp3q",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 3 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/path unusual staking path account",
                    FakeNet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
                    "m/1852'/1815'/10'/0/4",
                    "m/1852'/1815'/101'/2/0",
                    "addr1qwpug24twgud02405vncq9gmthq3r8e3a6l3855r8jpkgjnfwjwuljn5a0p37d4yvxevnte42mffrpmf4823vcdq62xqm8xq3j",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 3 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/path multidelegation stake key unusual account",
                    FakeNet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
                    "m/1852'/1815'/0'/0/1",
                    "m/1852'/1815'/101'/2/60",
                    "addr1qdd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63vmugd5zn06wnjkd3e4gz260kt832axwmcruch85mkpqnv2qzt38al",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 3 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/path multidelegation stake key unusual index",
                    FakeNet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
                    "m/1852'/1815'/0'/0/1",
                    "m/1852'/1815'/0'/2/1000001",
                    "addr1qdd9xypc9xnnstp2kas3r7mf7ylxn4sksfxxypvwgnc63v7z7lu6g8ncaa9ksx9q5lg2676a59a93y6fv86qzzdx4k5qjp9hw2",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 3 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/keyHash unusual account",
                    Testnet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
                    "m/1852'/1815'/101'/0/1",
                    "1d227aefa4b773149170885aadba30aab3127cc611ddbc4999def61c",
                    "addr_test1qq6dcymepkghuyt0za9jxg5hn89art9y8yjcvhxclxdhndsayfawlf9hwv2fzuygt2km5v92kvf8e3s3mk7ynxw77cwq9n0t8l",
                    nav_inst_1,
                    [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] * 2 + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/keyHash unusual address index",
                    Testnet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_KEY,
                    "m/1852'/1815'/0'/0/1'",
                    "1d227aefa4b773149170885aadba30aab3127cc611ddbc4999def61c",
                    "addr_test1qppn39wu9az8zv5c6k59ke0j2udmjzy42uelpsjjcadf0fgayfawlf9hwv2fzuygt2km5v92kvf8e3s3mk7ynxw77cwqelwlvz",
                    nav_inst_1,
                    [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] * 2 + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address scriptHash/path unusual account",
                    Testnet, AddressType.BASE_PAYMENT_SCRIPT_STAKE_KEY,
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "m/1852'/1815'/200'/2/0",
                    "addr_test1zqfz49rtntfa9h0s98f6s28sg69weemgjhc4e8hm66d5yaad7dqp9clvjdu902n5app3d70rnkax3wjy8n78fz29uhfqzs7q26",
                    nav_inst_2,
                    [NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] * 2 + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/scriptHash unusual account",
                    Testnet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_SCRIPT,
                    "m/1852'/1815'/101'/0/1",
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "addr_test1yq6dcymepkghuyt0za9jxg5hn89art9y8yjcvhxclxdhndsj922xhxkn6twlq2wn4q50q352annk3903tj00h45mgfmsc0du6n",
                    nav_inst_1,
                    [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] * 2 + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("base address path/scriptHash unusual address index",
                    Testnet,
                    AddressType.BASE_PAYMENT_KEY_STAKE_SCRIPT,
                    "m/1852'/1815'/0'/0/1'",
                    "122a946b9ad3d2ddf029d3a828f0468aece76895f15c9efbd69b4277",
                    "addr_test1yppn39wu9az8zv5c6k59ke0j2udmjzy42uelpsjjcadf0fgj922xhxkn6twlq2wn4q50q352annk3903tj00h45mgfmsyrvg3w",
                    nav_inst_1,
                    [NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] + [NavInsID.RIGHT_CLICK] * 2 + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("pointer address unusual account",
                    Testnet,
                    AddressType.POINTER_KEY,
                    "m/1852'/1815'/1000'/0/1",
                    pointer_to_str(1, 0, 0),
                    "addr_test1gq8vvh30wke6m5wl2xgwg5luus7zl0pr8kewjzq0wyyga6gpqqqqze3mqg",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 3 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("pointer address unusual address index",
                    Testnet,
                    AddressType.POINTER_KEY,
                    "m/1852'/1815'/0'/0/1'",
                    pointer_to_str(0, 7, 0),
                    "addr_test1gppn39wu9az8zv5c6k59ke0j2udmjzy42uelpsjjcadf0fgqquqqpn6uug",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 3 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("reward multidelegation unusual account",
                    Testnet,
                    AddressType.REWARD_KEY,
                    "",
                    "m/1852'/1815'/101'/2/1",
                    "stake_test1up0umv478zejdvynrddaddjzcztnmm2phsqs77cghyuah6qnjw5hh",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("reward multidelegation unusual index",
                    Testnet,
                    AddressType.REWARD_KEY,
                    "",
                    "m/1852'/1815'/0'/2/20000000",
                    "stake_test1urgn94qu0ewtt6f7l4sp6jm5vjv5u3gktevzy46s2qn92yshap4ze",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
    DeriveAddressTestCase("reward path unusual account",
                    FakeNet,
                    AddressType.REWARD_KEY,
                    "",
                    "m/1852'/1815'/300'/2/0",
                    "stake1u08h6dxajsaatnakylrd4pdhfrv7z3lkzgsq60fhvejux0gpcrd2j",
                    nano_nav_show=[NavInsID.BOTH_CLICK] * 2 + [NavInsID.RIGHT_CLICK] + [NavInsID.BOTH_CLICK] * 2),
]
