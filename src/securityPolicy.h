#ifndef H_CARDANO_APP_SECURITY_POLICY
#define H_CARDANO_APP_SECURITY_POLICY

#include "bip44.h"

typedef enum {
	POLICY_ALLOW = 1,
	POLICY_DENY = 2,
	POLICY_PROMPT_BEFORE_RESPONSE = 3,
	POLICY_PROMPT_WARN_UNUSUAL = 4,
	POLICY_SHOW_BEFORE_RESPONSE = 5, // Show on display but do not ask for explicit confirmation
} security_policy_t;

security_policy_t policyForGetExtendedPublicKey(const bip44_path_t* pathSpec);

security_policy_t policyForShowDeriveAddress(const bip44_path_t* pathSpec);
security_policy_t policyForReturnDeriveAddress(const bip44_path_t* pathSpec);

security_policy_t policyForAttestUtxo();

security_policy_t policyForSignTxInit();
security_policy_t policyForSignTxInput();
security_policy_t policyForSignTxOutputAddress(const uint8_t* rawAddressBuffer, size_t rawAddressSize);
security_policy_t policyForSignTxOutputPath(const bip44_path_t* pathSpec);
security_policy_t policyForSignTxFee(uint64_t fee );
security_policy_t policyForSignTxWitness(const bip44_path_t* pathSpec);

#endif
