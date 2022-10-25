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
#include "nbgl_page.h"
#include "nbgl_touch.h"
#include "nbgl_use_case.h"
#include "state.h"
#include "ui.h"
#include "uiHelpers.h"
#include "uiScreens_nbgl.h"

#define PAGE_START 0
#define NB_PAGE_SETTING 2
#define IS_TOUCHABLE false
#define NB_INFO_FIELDS 3
#define NB_SETTINGS_SWITCHES 1

enum {
  SWITCH_APP_MODE_TOKEN = FIRST_USER_TOKEN,
};

static nbgl_layoutSwitch_t switches[NB_SETTINGS_SWITCHES];

static const char *const infoTypes[] = {"Version", "Developer", "Copyright"};
static const char *const infoContents[] = {APPVERSION, "Vacuumlabs",
                                           "(c) 2022 Ledger"};
static const int INS_NONE = -1;

// Settings
static void exit(void) { os_sched_exit(-1); }

static bool settings_navigation_callback(uint8_t page, nbgl_pageContent_t *content) {
  if (page == 0) {
    switches[0].text = (char *)"Enable expert mode";
    switches[0].subText = (char *)"Select application mode";
    switches[0].token = SWITCH_APP_MODE_TOKEN;
    switches[0].tuneId = TUNE_TAP_CASUAL;
    switches[0].initState = app_mode_expert();

    content->type = SWITCHES_LIST;
    content->switchesList.nbSwitches = NB_SETTINGS_SWITCHES;
    content->switchesList.switches = (nbgl_layoutSwitch_t *)switches;
  } else if (page == 1) {
    content->type = INFOS_LIST;
    content->infosList.nbInfos = NB_INFO_FIELDS;
    content->infosList.infoTypes = (const char **)infoTypes;
    content->infosList.infoContents = (const char **)infoContents;
  } else {
    return false;
  }
  return true;
}

static void settings_control_callback(int token, uint8_t index) {
  UNUSED(index);
  switch (token) {
  case SWITCH_APP_MODE_TOKEN:
    app_mode_set_expert(index);
    break;

  default:
    PRINTF("Should not happen !");
    break;
  }
}

static void ui_menu_settings(void) {
  nbgl_useCaseSettings((char *)"Cardano settings", PAGE_START, NB_PAGE_SETTING,
                       IS_TOUCHABLE, ui_idle_flow, settings_navigation_callback,
                       settings_control_callback);
}

void ui_idle_flow(void) {
  TRACE("RESETTING\n\n");
  nbgl_reset_transaction_full_context();
  nbgl_useCaseHome((char *)"Cardano", &C_cardano_64, NULL, true,
                   ui_menu_settings, exit);
}

void ui_idle(void) { 
    currentInstruction = INS_NONE; 
}
#endif // HAVE_NBGL
