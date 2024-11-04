# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2024 Ledger SAS
# SPDX-License-Identifier: LicenseRef-LEDGER
"""
This module provides Ragger tests for Derive Native Script Hash check
"""

from enum import IntEnum
from typing import List, Any
from dataclasses import dataclass, field


class NativeScriptType(IntEnum):
    PUBKEY_DEVICE_OWNED = 0x00
    PUBKEY_THIRD_PARTY = 0xF0
    ALL = 0x01
    ANY = 0x02
    N_OF_K = 0x03
    INVALID_BEFORE = 0x04
    INVALID_HEREAFTER = 0x05

class NativeScriptHashDisplayFormat(IntEnum):
    BECH32 = 0x01
    POLICY_ID = 0x02


@dataclass
class NativeScriptParamsDeviceOwnedPubkey:
    path: str

@dataclass
class NativeScript:
    type: NativeScriptType
    params: Any

@dataclass
class NativeScriptParamsThirdPartyPubkey:
    keyHashHex: str

@dataclass
class NativeScriptParamsAll:
    scripts: List[NativeScript] = field(default_factory=list)

@dataclass
class NativeScriptParamsAny:
    scripts: List[NativeScript] = field(default_factory=list)

@dataclass
class NativeScriptParamsNofK:
    requiredCount: int
    scripts: List[NativeScript] = field(default_factory=list)

@dataclass
class NativeScriptParamsInvalid:
    slot: int

@dataclass
class ValidNativeScriptTestCase:
    name: str
    script: NativeScript
    displayFormat: NativeScriptHashDisplayFormat
    expectedHash: str


# pylint: disable=line-too-long
ValidNativeScriptTestCases = [
    ValidNativeScriptTestCase("PUBKEY - device owned",
                              NativeScript(NativeScriptType.PUBKEY_DEVICE_OWNED,
                                           NativeScriptParamsDeviceOwnedPubkey("m/1852'/1815'/0'/0/0")),
                              NativeScriptHashDisplayFormat.BECH32,
                              "5102a193b3d5f0c256fcc425836ffb15e7d96d3389f5e57dc6bea726"),
    ValidNativeScriptTestCase("PUBKEY - third party",
                              NativeScript(NativeScriptType.PUBKEY_THIRD_PARTY,
                                           NativeScriptParamsThirdPartyPubkey("3a55d9f68255dfbefa1efd711f82d005fae1be2e145d616c90cf0fa9")),
                              NativeScriptHashDisplayFormat.BECH32,
                              "855228f5ecececf9c85618007cc3c2e5bdf5e6d41ef8d6fa793fe0eb"),
    ValidNativeScriptTestCase("PUBKEY - third party (script hash displayed as policy id)",
                              NativeScript(NativeScriptType.PUBKEY_THIRD_PARTY,
                                           NativeScriptParamsThirdPartyPubkey("3a55d9f68255dfbefa1efd711f82d005fae1be2e145d616c90cf0fa9")),
                              NativeScriptHashDisplayFormat.POLICY_ID,
                              "855228f5ecececf9c85618007cc3c2e5bdf5e6d41ef8d6fa793fe0eb"),
    ValidNativeScriptTestCase("ALL script)",
                              NativeScript(NativeScriptType.ALL,
                                           NativeScriptParamsAll(
                                           [NativeScript(NativeScriptType.PUBKEY_THIRD_PARTY,
                                                         NativeScriptParamsThirdPartyPubkey("c4b9265645fde9536c0795adbcc5291767a0c61fd62448341d7e0386")),
                                            NativeScript(NativeScriptType.PUBKEY_THIRD_PARTY,
                                                         NativeScriptParamsThirdPartyPubkey("0241f2d196f52a92fbd2183d03b370c30b6960cfdeae364ffabac889"))])),
                              NativeScriptHashDisplayFormat.BECH32,
                              "af5c2ce476a6ede1c879f7b1909d6a0b96cb2081391712d4a355cef6"),
]
