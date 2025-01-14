#ifndef H_CARDANO_APP_GET_PUBLIC_KEYS_UI
#define H_CARDANO_APP_GET_PUBLIC_KEYS_UI

// ctx->ui_state is shared between the intertwined UI state machines
// it should be set to this value at the beginning and after a UI state machine is finished
static int UI_STEP_NONE = 0;

// ============================== derivation and UI state machine for one key
// ==============================

enum {
    GET_KEY_UI_STEP_WARNING = 200,
    GET_KEY_UI_STEP_PROMPT,
    GET_KEY_UI_STEP_DISPLAY,
    GET_KEY_UI_STEP_CONFIRM,
    GET_KEY_UI_STEP_RESPOND,
};

void getPublicKeys_respondOneKey_ui_runStep();

// ============================== INIT ==============================

enum {
    HANDLE_INIT_UI_STEP_CONFIRM = 100,
    HANDLE_INIT_UI_STEP_RESPOND,  // WARNING: this must be the last valid step, see below
};

void getPublicKeys_handleInit_ui_runStep();
#endif  // H_CARDANO_APP_GET_PUBLIC_KEYS_UI
