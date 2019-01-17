#ifndef H_CARDANO_APP_BIP44
#define H_CARDANO_APP_BIP44

#include <os.h>
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

static const uint32_t BIP44_MAX_PATH_LENGTH = 10;

typedef struct {
	uint32_t path[BIP44_MAX_PATH_LENGTH];
	uint32_t length;
} bip44_path_t;


static const uint32_t BIP_44 = 44;
static const uint32_t ADA_COIN_TYPE = 1815;

static const uint32_t HARDENED_BIP32 = ((uint32_t) 1 << 31);

size_t bip44_parseFromWire(
        bip44_path_t* pathSpec,
        uint8_t* dataBuffer, size_t dataSize
);

// Indexes into pathSpec
enum {
	BIP44_I_PURPOSE = 0,
	BIP44_I_COIN_TYPE = 1,
	BIP44_I_ACCOUNT = 2,
	BIP44_I_CHAIN = 3,
	BIP44_I_ADDRESS = 4,
};


// Checks for /44'/1815'/account'
bool bip44_hasValidPrefix(const bip44_path_t* pathSpec);

bool bip44_containsAccount(const bip44_path_t* pathSpec);
bool bip44_hasValidAccount(const bip44_path_t* pathSpec);

bool bip44_containsChainType(const bip44_path_t* pathSpec);
bool bip44_hasValidChainType(const bip44_path_t* pathSpec);

bool bip44_containsAddress(const bip44_path_t* pathSpec);

bool isHardened(uint32_t value);

#endif
