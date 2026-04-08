import ezero_filter as ezero

# 1. Charger le cerveau de 556 Ko
ezero.load_memory("ezero_memory.json")

# 2. Autoriser un petit apprentissage pour le nouveau langage
ezero.config.SYNAPTIC_LIMIT = 22000 

contract_code = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PeP_Arbitrage {
    address public owner;
    uint256 public constant MIN_PROFIT = 0.5 ether;

    constructor() {
        owner = msg.sender;
    }

    function executeTrade(address _tokenA, address _tokenB, uint256 _amount) external {
        require(msg.sender == owner, "Not authorized");
        // Logique de calcul complexe pour le recyclage des jetons
        uint256 profit = _amount * 2; 
        require(profit > MIN_PROFIT, "Profit too low");
    }
}
"""

# Test de filtrage
resultat = ezero.filter(contract_code)

print(f"--- RÉSULTAT SOLIDITY ---")
print(f"Original : {len(contract_code)} caractères")
print(f"Filtré   : {len(resultat['skeleton'])} caractères")
print(f"Gain     : {resultat['gain_pct']}%")
print(f"Synapses : {ezero.get_synapse_count()}")
print(f"\nSquelette : \n{resultat['skeleton']}")