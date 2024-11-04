# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: 2024 Ledger SAS
# SPDX-License-Identifier: LicenseRef-LEDGER
"""
This module provides Ragger tests for Derive Native Script Hash check
"""

import pytest

from ragger.backend import BackendInterface
from ragger.firmware import Firmware
from ragger.navigator import Navigator, NavInsID
from ragger.navigator.navigation_scenario import NavigateWithScenario

from application_client.app_def import Errors
from application_client.command_sender import CommandSender

from input_files.derive_native_script import ValidNativeScriptTestCases, ValidNativeScriptTestCase
from input_files.derive_native_script import NativeScript, NativeScriptType
from input_files.derive_native_script import NativeScriptParamsThirdPartyPubkey, NativeScriptHashDisplayFormat
from input_files.derive_native_script import NativeScriptParamsAll, NativeScriptParamsAny, NativeScriptParamsNofK

from utils import idTestFunc


@pytest.mark.parametrize(
    "testCase",
    ValidNativeScriptTestCases,
    ids=idTestFunc
)
def test_derive_native_script_hash(firmware: Firmware,
                                   backend: BackendInterface,
                                   navigator: Navigator,
                                   scenario_navigator: NavigateWithScenario,
                                   testCase: ValidNativeScriptTestCase,
                                    appFlags: dict) -> None:
    """Check Derive Native Script Hash"""

    if appFlags['isAppXS']:
        pytest.skip("Operational Certificate is not supported by 'AppXS' version")

    # Use the app interface instead of raw interface
    client = CommandSender(backend)

    _deriveNativeScriptHash_addScript(firmware, navigator, client, testCase.script, False)

    _deriveNativeScriptHash_finishWholeNativeScript(firmware, navigator, scenario_navigator, client, testCase)


def _deriveNativeScriptHash_addScript(firmware: Firmware,
                                      navigator: Navigator,
                                      client: CommandSender,
                                      script: NativeScript,
                                      complex_nav: bool) -> None:
    if script.type in [NativeScriptType.ALL, NativeScriptType.ANY, NativeScriptType.N_OF_K]:
        _deriveScriptHash_startComplexScript(firmware, navigator, client, script)
        assert isinstance(script.params, (NativeScriptParamsAll, NativeScriptParamsAny, NativeScriptParamsNofK))
        for subscript in script.params.scripts:
            _deriveNativeScriptHash_addScript(firmware, navigator, client, subscript, True)
    else:
        _deriveNativeScriptHash_addSimpleScript(firmware, navigator, client, script, complex_nav)


def _deriveNativeScriptHash_addSimpleScript(firmware: Firmware,
                                            navigator: Navigator,
                                            client: CommandSender,
                                            script: NativeScript,
                                            complex_nav: bool) -> None:
    """Send the add command for a simple script

    Args:
        firmware (Firmware): The firmware version
        client (CommandSender): The command sender instance
        navigator (Navigator): The navigator instance
        script (NativeScript): The script
    """

    with client.derive_script_add_simple(script):
        moves = []
        if firmware.is_nano:
            if complex_nav:
                moves += [NavInsID.BOTH_CLICK]
            if complex_nav or isinstance(script.params, NativeScriptParamsThirdPartyPubkey):
                moves += [NavInsID.RIGHT_CLICK]
            moves += [NavInsID.BOTH_CLICK]
        else:
            if complex_nav:
                moves += [NavInsID.TAPPABLE_CENTER_TAP]
            moves += [NavInsID.SWIPE_CENTER_TO_LEFT]
        navigator.navigate(moves)
    # Check the status (Asynchronous)
    response = client.get_async_response()
    assert response and response.status == Errors.SW_SUCCESS


def _deriveScriptHash_startComplexScript(firmware: Firmware,
                                         navigator: Navigator,
                                         client: CommandSender,
                                         script: NativeScript) -> None:
    """Send the add command for a complex script

    Args:
        firmware (Firmware): The firmware version
        client (CommandSender): The command sender instance
        navigator (Navigator): The navigator instance
        script (NativeScript): The script
    """

    with client.derive_script_add_complex(script):
        moves = []
        if firmware.is_nano:
            moves += [NavInsID.BOTH_CLICK]
        else:
            moves += [NavInsID.SWIPE_CENTER_TO_LEFT]
        navigator.navigate(moves)
    # Check the status (Asynchronous)
    response = client.get_async_response()
    assert response and response.status == Errors.SW_SUCCESS


def _deriveNativeScriptHash_finishWholeNativeScript(firmware: Firmware,
                                                    navigator: Navigator,
                                                    scenario_navigator: NavigateWithScenario,
                                                    client: CommandSender,
                                                    testCase: ValidNativeScriptTestCase) -> None:
    """Send the finish command for the whole native script

    Args:
        firmware (Firmware): The firmware version
        navigator (Navigator): The navigator instance
        scenario_navigator (NavigateWithScenario): The scenario navigator instance
        client (CommandSender): The command sender instance
        testCase (SignTxTestCase): The test case
    """

    with client.derive_script_finish(testCase.displayFormat):
        if firmware.is_nano:
            moves = []
            if testCase.displayFormat != NativeScriptHashDisplayFormat.POLICY_ID:
                moves += [NavInsID.RIGHT_CLICK]
            moves += [NavInsID.BOTH_CLICK]

            navigator.navigate(moves)
        else:
            scenario_navigator.address_review_approve(do_comparison=False)
    # Check the status (Asynchronous)
    response = client.get_async_response()
    assert response and response.status == Errors.SW_SUCCESS
    # Check the response
    assert response.data.hex() == testCase.expectedHash
    # TODO: Generate the payload and verify the signature
