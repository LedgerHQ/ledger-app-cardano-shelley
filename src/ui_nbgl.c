/*******************************************************************************
 **   Ledger App - Cardano Wallet (c) 2022 Ledger
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 ********************************************************************************/
#ifdef HAVE_NBGL
#include "app_mode.h"
#include "nbgl_use_case.h"
#include "state.h"
#include "ui.h"
#include "uiHelpers.h"
#include "uiScreens_nbgl.h"

#define MAX_LINE_PER_PAGE_COUNT 10
#define MAX_TAG_CONTENT_CHAR_PER_LINE 18
#define MAX_TAG_PER_PAGE_COUNT 4
#define MAX_TAG_TITLE_LINE_LENGTH 30
#define MAX_TAG_CONTENT_LENGTH 200
#define MAX_TEXT_STRING 50
#define PENDING_ELEMENT_INDEX MAX_TAG_PER_PAGE_COUNT
enum {
  CANCEL_PROMPT_TOKEN = 1,
  ACCEPT_PAGE_TOKEN,
  CONFIRMATION_STATUS_TOKEN,
};

typedef struct {
  char *confirmedStatus; // text displayed in confirmation page (after long press)
  char *rejectedStatus;  // text displayed in rejection page (after reject confirmed)
  callback_t approvedCallback;
  callback_t rejectedCallback;
  callback_t pendingCallback;
  bool pendingElement;
  uint8_t currentLineCount;
  uint8_t currentElementCount;
  char tagTitle[MAX_TAG_PER_PAGE_COUNT + 1][MAX_TAG_TITLE_LINE_LENGTH];
  char tagContent[MAX_TAG_PER_PAGE_COUNT + 1][MAX_TAG_CONTENT_LENGTH];
  char pageText[2][MAX_TEXT_STRING];
  bool lightConfirmation;
  nbgl_layoutTagValueList_t pairList;
} UiContext_t;

static nbgl_page_t *pageContext;
static nbgl_layoutTagValue_t tagValues[5];
static UiContext_t uiContext = {
    .rejectedStatus = NULL,
    .confirmedStatus = NULL,
    .currentLineCount = 0,
    .currentElementCount = 0,
    .pendingElement = false,
    .lightConfirmation = 0,
};

// Forward declaration
static void display_cancel(void);
static void display_confirmation_status(void);
static void display_cancel_status(void);
static void trigger_callback(callback_t userAcceptCallback);

static void release_context(void) {
  if (pageContext != NULL) {
    nbgl_pageRelease(pageContext);
    pageContext = NULL;
  }
}

static inline uint8_t get_element_line_count(const char *line) {
  return strlen(line) / MAX_TAG_CONTENT_CHAR_PER_LINE + 2;
}

static void set_callbacks(callback_t approvedCallback, callback_t rejectedCallback){
    uiContext.approvedCallback = approvedCallback;
    uiContext.rejectedCallback = rejectedCallback;
}
    
static void fill_current_element(const char* text, const char* content) {
  strncpy(uiContext.tagTitle[uiContext.currentElementCount], text, MAX_TAG_TITLE_LINE_LENGTH);
  strncpy(uiContext.tagContent[uiContext.currentElementCount], content, MAX_TAG_CONTENT_LENGTH);

  uiContext.currentElementCount++;
  uiContext.currentLineCount += get_element_line_count(content);
}

static void fill_pending_element(const char* text, const char* content) {
  strncpy(uiContext.tagTitle[PENDING_ELEMENT_INDEX], text, MAX_TAG_TITLE_LINE_LENGTH);
  strncpy(uiContext.tagContent[PENDING_ELEMENT_INDEX], content, MAX_TAG_CONTENT_LENGTH);

  uiContext.pendingElement = true;
}

static void reset_transaction_current_context(void) {
  uiContext.currentElementCount = 0;
  uiContext.currentLineCount = 0;
}

void nbgl_reset_transaction_full_context(void) {
  reset_transaction_current_context();
  uiContext.lightConfirmation = false;
  uiContext.rejectedStatus = NULL;
  uiContext.confirmedStatus = NULL;
}

void set_light_confirmation(bool needed) {
  uiContext.lightConfirmation = needed;
}

static void display_callback(int token, unsigned char index) {
  (void)index;

  release_context(); 

  switch (token) {
  case CANCEL_PROMPT_TOKEN:
    display_cancel();
    break;
  case ACCEPT_PAGE_TOKEN:
    uiContext.approvedCallback();
    break;
  case CONFIRMATION_STATUS_TOKEN:
    display_confirmation_status();
    break;
  default:
    TRACE("%d unknown", token);
  }
}

static void _display_confirmation(void) {
  TRACE("_confirmation");

  release_context();

  if (uiContext.pendingCallback) {
    uiContext.approvedCallback = uiContext.pendingCallback;
    uiContext.pendingCallback = NULL;
  }

  nbgl_pageNavigationInfo_t info = {
      .activePage = 0,
      .nbPages = 0,
      .navType = NAV_WITH_TAP,
      .progressIndicator = true,
      .navWithTap.backButton = false,
      .navWithTap.nextPageText = NULL,
      .navWithTap.quitText = "Reject",
      .quitToken = CANCEL_PROMPT_TOKEN,
      .tuneId = TUNE_TAP_CASUAL};

  nbgl_pageContent_t content = {
      .type = INFO_LONG_PRESS,
      .infoLongPress.icon = &C_cardano_64,
      .infoLongPress.text = uiContext.pageText[0],
      .infoLongPress.longPressText = (char *)"Hold to approve",
      .infoLongPress.longPressToken = CONFIRMATION_STATUS_TOKEN,
      .infoLongPress.tuneId = TUNE_TAP_NEXT};

  pageContext = nbgl_pageDrawGenericContent(&display_callback, &info, &content);

#ifdef HEADLESS
  nbgl_refresh();
  trigger_callback(uiContext.approvedCallback);
#endif
}

static void light_confirm_callback(bool confirm) {
  if (confirm) {
    display_confirmation_status();
  } else {
    display_cancel_status();
  }
}

static void _display_light_confirmation(void) {
  TRACE("_light_confirmation");
  if (uiContext.pendingCallback) {
    uiContext.approvedCallback = uiContext.pendingCallback;
    uiContext.pendingCallback = NULL;
  }

  nbgl_useCaseChoice(&C_cardano_64, uiContext.pageText[0], (char *)"",
                     (char *)"Confirm", (char *)"Cancel", light_confirm_callback);

#ifdef HEADLESS
  trigger_callback(uiContext.approvedCallback);
#endif
}

static void display_cancel(void) {
  if (uiContext.lightConfirmation) {
    display_cancel_status();
  } else {
    nbgl_useCaseConfirm((char *)"Reject ?", NULL, (char *)"Yes, Reject",
                        (char *)"Go back", display_cancel_status);
  }
}

static void cancellation_status_callback(void) {
  if (uiContext.rejectedCallback) {
    uiContext.rejectedCallback();
  }
  ui_idle_flow();
}

static void display_cancel_status(void) {
  ui_idle();

  if (uiContext.rejectedStatus) {
    nbgl_useCaseStatus(uiContext.rejectedStatus, false, cancellation_status_callback);
  } else {
    nbgl_useCaseStatus((char *)"Action rejected", false, cancellation_status_callback);
  }
}

static void _display_page(void) {
  TRACE("_page");

  release_context();

  for (uint8_t i = 0; i < uiContext.currentElementCount; i++) {
    tagValues[i].item = uiContext.tagTitle[i];
    tagValues[i].value = uiContext.tagContent[i];
  }

  nbgl_pageNavigationInfo_t info = {
      .activePage = 0,
      .nbPages = 0,
      .navType = NAV_WITH_TAP,
      .progressIndicator = true,
      .navWithTap.backButton = false,
      .navWithTap.nextPageText = (char *)"Tap to continue",
      .navWithTap.nextPageToken = ACCEPT_PAGE_TOKEN,
      .navWithTap.quitText = (char *)"Cancel",
      .quitToken = CANCEL_PROMPT_TOKEN,
      .tuneId = TUNE_TAP_CASUAL};

  nbgl_pageContent_t content = {
      .type = TAG_VALUE_LIST,
      .tagValueList.nbPairs = uiContext.currentElementCount,
      .tagValueList.pairs = (nbgl_layoutTagValue_t *)tagValues};

  pageContext = nbgl_pageDrawGenericContent(&display_callback, &info, &content);
  reset_transaction_current_context();

#ifdef HEADLESS
  nbgl_refresh();
  trigger_callback(uiContext.approvedCallback);
#endif
}

static void _display_prompt(void) {
  TRACE("_prompt");
  if (uiContext.pendingCallback) {
    uiContext.approvedCallback = uiContext.pendingCallback;
    uiContext.pendingCallback = NULL;
  }

  nbgl_useCaseReviewStart(&C_cardano_64, uiContext.pageText[0],
                          uiContext.pageText[1], (char *)"Reject if not sure",
                          uiContext.approvedCallback, &display_cancel);
#ifdef HEADLESS
  nbgl_refresh();
  trigger_callback(uiContext.approvedCallback);
#endif
}

static void _display_warning(void) {
  TRACE("_warning");
  if (uiContext.pendingCallback) {
    uiContext.approvedCallback = uiContext.pendingCallback;
    uiContext.pendingCallback = NULL;
  }

  nbgl_useCaseReviewStart(&C_warning64px, (char *)"WARNING",
                          uiContext.pageText[0], (char *)"Reject if not sure",
                          uiContext.approvedCallback, &display_cancel);
#ifdef HEADLESS
  nbgl_refresh();
  trigger_callback(uiContext.approvedCallback);
#endif
}

static void confirmation_status_callback(void) {
  if (uiContext.confirmedStatus) {
    nbgl_useCaseStatus(uiContext.confirmedStatus, true, ui_idle_flow);
  } else {
    nbgl_useCaseStatus((char *)"ACTION\nCONFIRMED", true, ui_idle_flow);
  }

}

static void display_confirmation_status(void) {
  if (uiContext.approvedCallback) {
    uiContext.approvedCallback();
  }

  trigger_callback(&confirmation_status_callback);
}

static void display_address_callback(void) {
  uint8_t address_index = 0;

  // Address field is not displayed in pairList, so there is one element less.
  uiContext.pairList.nbPairs = uiContext.currentElementCount - 1;
  uiContext.pairList.pairs = tagValues;

  uiContext.confirmedStatus = (char *)"ADDRESS\nVERIFIED";
  uiContext.rejectedStatus = (char *)"Address rejected";

  for (uint8_t i = 0; i < uiContext.currentElementCount; i++) {
    if (strcmp(uiContext.tagTitle[i], "Address")) {
      tagValues[i].item = uiContext.tagTitle[i];
      tagValues[i].value = uiContext.tagContent[i];
    }
    else {
      address_index = i;
    }
  }

  nbgl_useCaseAddressConfirmationExt(uiContext.tagContent[address_index], light_confirm_callback, &uiContext.pairList);

#ifdef HEADLESS
  nbgl_refresh();
  trigger_callback(&display_confirmation_status);
#endif
}

static void trigger_callback(callback_t userAcceptCallback) {
  // Hack to trigger a callback from NBGL while leaving the screen untouched
  nbgl_layoutDescription_t layoutDescription;
  nbgl_layout_t *layout = NULL;
  nbgl_layoutCenteredInfo_t centeredInfo = {
    .text1 = NULL,
    .text2 = NULL,
    .text3 = NULL,
    .style = 0,
    .icon = NULL,
    .offsetY = 0
  };

  release_context();

  layoutDescription.modal = false;
  layoutDescription.withLeftBorder = true;

  layoutDescription.onActionCallback = NULL;
  layoutDescription.tapActionText = (char *)"";
  layoutDescription.tapActionToken = 0;
  layoutDescription.tapTuneId = TUNE_TAP_CASUAL;

  layoutDescription.ticker.tickerCallback = userAcceptCallback;
  layoutDescription.ticker.tickerIntervale = 0;
  layoutDescription.ticker.tickerValue = 100;
  pageContext = nbgl_layoutGet(&layoutDescription);

  nbgl_layoutAddCenteredInfo(layout, &centeredInfo);
}

static void handle_pending_element(void) {
    TRACE("Add pending element");
    ASSERT(uiContext.currentElementCount == 0);
    ASSERT(uiContext.currentLineCount == 0);

    fill_current_element(uiContext.tagTitle[PENDING_ELEMENT_INDEX], uiContext.tagContent[PENDING_ELEMENT_INDEX]);

    uiContext.pendingElement = false;
}

static void _display_page_or_call_function(callback_t callback) {
  if (uiContext.pendingElement) {
      handle_pending_element();
  }

  if (uiContext.currentElementCount > 0) {
    uiContext.pendingCallback = uiContext.approvedCallback;
    uiContext.approvedCallback = callback;
    _display_page();
  } else {
    callback();
  }
}

// Fillers
void force_display(callback_t userAcceptCallback, callback_t userRejectCallback) {
  if (uiContext.currentLineCount > 0) {
    TRACE("Force page display");
    set_callbacks(userAcceptCallback, userRejectCallback);
    _display_page();
  } else {
    TRACE("Nothing to do");
    trigger_callback(userAcceptCallback);
  }
}

void fill_and_display_if_required(const char *line1, const char *line2,
                                  callback_t userAcceptCallback,
                                  callback_t userRejectCallback) {

  ASSERT(strlen(line1) <= MAX_TAG_TITLE_LINE_LENGTH);
  ASSERT(strlen(line2) <= MAX_TAG_CONTENT_LENGTH);

  if (uiContext.pendingElement) {
      handle_pending_element();
  }

  if (uiContext.currentLineCount + get_element_line_count(line2) >
      MAX_LINE_PER_PAGE_COUNT) {
    TRACE("Display page and add pending element");
    fill_pending_element(line1, line2);
    set_callbacks(userAcceptCallback, userRejectCallback);
    _display_page();
  } else {
    TRACE("Add element to page");
    fill_current_element(line1, line2);
    trigger_callback(userAcceptCallback);
  }
}

void fill_and_display_new_page(const char *line1, const char *line2,
                               callback_t userAcceptCallback,
                               callback_t userRejectCallback) {

  ASSERT(strlen(line1) <= MAX_TAG_TITLE_LINE_LENGTH);
  ASSERT(strlen(line2) <= MAX_TAG_CONTENT_LENGTH);

  if (uiContext.pendingElement) {
      handle_pending_element();
  }

  if (uiContext.currentLineCount > 0) {
    TRACE("Display page and add pending element");
    fill_pending_element(line1, line2);

    display_page(userAcceptCallback, userRejectCallback);
  } else {
    TRACE("Add element to page");
    fill_current_element(line1, line2);
    uiContext.currentLineCount += get_element_line_count(line2);
    display_continue(userAcceptCallback);
  }
}

void fill_address_data(char *text, char *content) {
  fill_current_element(text, content);
}

void display_confirmation(const char *text1, const char *text2,
                          const char *confirmText, const char *rejectText,
                          callback_t userAcceptCallback,
                          callback_t userRejectCallback) {
  TRACE("Displaying confirmation");

  uiContext.confirmedStatus = (char *)confirmText;
  uiContext.rejectedStatus = (char *)rejectText;

  set_callbacks(userAcceptCallback, userRejectCallback);

  strncpy(uiContext.pageText[0], text1, MAX_TEXT_STRING);
  strncpy(uiContext.pageText[1], text2, MAX_TEXT_STRING);

  if (uiContext.lightConfirmation) {
      _display_page_or_call_function(&_display_light_confirmation);
  } else {
      _display_page_or_call_function(&_display_confirmation);
  }
}

void display_prompt(const char *text1, const char *text2,
                    callback_t userAcceptCallback, callback_t userRejectCallback) {
  TRACE("Displaying Prompt");

  set_callbacks(userAcceptCallback, userRejectCallback);

  strncpy(uiContext.pageText[0], text1, MAX_TEXT_STRING);
  strncpy(uiContext.pageText[1], text2, MAX_TEXT_STRING);

  _display_page_or_call_function(&_display_prompt);
}

void display_warning(const char *text, callback_t userAcceptCallback,
                     callback_t userRejectCallback) {
  TRACE("Displaying Warning");

  set_callbacks(userAcceptCallback, userRejectCallback);
  strncpy(uiContext.pageText[0], text, MAX_TEXT_STRING);
  _display_page_or_call_function(&_display_warning);
}

void display_address(callback_t userAcceptCallback, callback_t userRejectCallback) {
  TRACE("Displaying Address");

  set_callbacks(userAcceptCallback, userRejectCallback);
  nbgl_useCaseReviewStart(&C_cardano_64, (char *)"Verify Cardano\naddress",
                          NULL, (char *)"Cancel", display_address_callback,
                          display_cancel_status);
#ifdef HEADLESS
  nbgl_refresh();
  trigger_callback(&display_address_callback);
#endif
}

void display_error(void) {
  TRACE("Displaying Error");

  nbgl_reset_transaction_full_context();
  nbgl_useCaseStatus((char *)"An error has occurred", false, ui_idle_flow);
}

#endif // HAVE_NBGL
