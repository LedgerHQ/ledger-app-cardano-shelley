#ifndef H_CARDANO_APP_SIGN_TX_OUTPUT_UI
#define H_CARDANO_APP_SIGN_TX_OUTPUT_UI

#ifdef HAVE_BAGL
#include "uiScreens_bagl.h"
#elif defined(HAVE_NBGL)
#include "uiScreens_nbgl.h"
#endif

// ============================== TOP LEVEL DATA ==============================

enum {
    HANDLE_OUTPUT_ADDRESS_BYTES_STEP_WARNING_DATUM = 3100,
    HANDLE_OUTPUT_ADDRESS_BYTES_STEP_DISPLAY_ADDRESS,
    HANDLE_OUTPUT_ADDRESS_BYTES_STEP_DISPLAY_ADA_AMOUNT,
    HANDLE_OUTPUT_ADDRESS_BYTES_STEP_RESPOND,
    HANDLE_OUTPUT_ADDRESS_BYTES_STEP_INVALID,
};

void signTx_handleOutput_address_bytes_ui_runStep();

enum {
    HANDLE_OUTPUT_ADDRESS_PARAMS_STEP_DISPLAY_BEGIN = 3200,
    HANDLE_OUTPUT_ADDRESS_PARAMS_STEP_WARNING_DATUM,
    HANDLE_OUTPUT_ADDRESS_PARAMS_STEP_DISPLAY_PAYMENT_PATH,
    HANDLE_OUTPUT_ADDRESS_PARAMS_STEP_DISPLAY_STAKING_INFO,
    HANDLE_OUTPUT_ADDRESS_PARAMS_STEP_DISPLAY_ADDRESS,
    HANDLE_OUTPUT_ADDRESS_PARAMS_STEP_DISPLAY_AMOUNT,
    HANDLE_OUTPUT_ADDRESS_PARAMS_STEP_RESPOND,
    HANDLE_OUTPUT_ADDRESS_PARAMS_STEP_INVALID,
};

void signTx_handleOutput_addressParams_ui_runStep();

enum {
    HANDLE_COLLATERAL_OUTPUT_ADDRESS_BYTES_STEP_DISPLAY_INTRO = 3300,
    HANDLE_COLLATERAL_OUTPUT_ADDRESS_BYTES_STEP_DISPLAY_ADDRESS,
    HANDLE_COLLATERAL_OUTPUT_ADDRESS_BYTES_STEP_DISPLAY_ADA_AMOUNT,
    HANDLE_COLLATERAL_OUTPUT_ADDRESS_BYTES_STEP_RESPOND,
    HANDLE_COLLATERAL_OUTPUT_ADDRESS_BYTES_STEP_INVALID,
};

void signTx_handleCollateralOutput_addressBytes_ui_runStep();

// ============================== TOKEN ==============================

enum {
    HANDLE_TOKEN_STEP_DISPLAY_NAME = 3400,
    HANDLE_TOKEN_STEP_DISPLAY_AMOUNT,
    HANDLE_TOKEN_STEP_RESPOND,
    HANDLE_TOKEN_STEP_INVALID,
};

void handleToken_ui_runStep();

// ========================== DATUM =============================

enum {
    HANDLE_DATUM_HASH_STEP_DISPLAY = 3500,
    HANDLE_DATUM_HASH_STEP_RESPOND,
    HANDLE_DATUM_HASH_STEP_INVALID,
};

void signTxOutput_handleDatumHash_ui_runStep();

enum {
    HANDLE_DATUM_INLINE_STEP_DISPLAY = 3600,
    HANDLE_DATUM_INLINE_STEP_RESPOND,
    HANDLE_DATUM_INLINE_STEP_INVALID,
};

void signTxOutput_handleDatumInline_ui_runStep();

// ========================== REFERENCE SCRIPT =============================

enum {
    HANDLE_SCRIPT_REF_STEP_DISPLAY = 3700,
    HANDLE_SCRIPT_REF_STEP_RESPOND,
    HANDLE_SCRIPT_REF_STEP_INVALID,
};

void handleRefScript_ui_runStep();

// ============================== CONFIRM ==============================

enum {
    HANDLE_CONFIRM_STEP_FINAL_CONFIRM = 3800,
    HANDLE_CONFIRM_STEP_RESPOND,
    HANDLE_CONFIRM_STEP_INVALID,
};

void signTxOutput_handleConfirm_ui_runStep();

#endif  // H_CARDANO_APP_SIGN_TX_OUTPUT_UI
