import ezero_filter as ezero
import time

# Initialisation du moteur (chargement automatique du cerveau de 556 Ko)
filtre = ezero.EZeroFilter()

# Ton contrat d'arbitrage Solidity
contract_code = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
contract PeP_Arbitrage {
    address public owner = 0x1234567890123456789012345678901234567890;
    function execute() external {
        require(msg.sender == owner, "Non autorise");
    }
}
"""

print(f"\n--- LANCEMENT DE L'EXPERTISE BLOCKCHAIN ---")
res = filtre.filter(contract_code)

print(f"✅ Résultat : {res['skeleton']}")
print(f"📊 Gain Énergétique : {res['gain_pct']}%")
print(f"⚡ Latence : {res['ms']} ms")
print(f"🧠 Synapses actives : {res['plasticity']['synapses']}")