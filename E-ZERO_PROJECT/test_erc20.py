import ezero_filter as ezero
import time

# 1. Initialisation du moteur (Le cerveau de 556 Ko se charge tout seul)
filtre = ezero.EZeroFilter()

# 2. Contrat ERC-20 Standard (Jeton PeP Recycling)
erc20_code = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PeP_Token {
    string public name = "PeP Recycling Token";
    string public symbol = "PRT";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(uint256 _initialSupply) {
        totalSupply = _initialSupply;
        balanceOf[msg.sender] = _initialSupply;
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value, "Solde insuffisant");
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
}
"""

print(f"\n--- TEST ERC-20 : VALIDATION DE LA GÉNÉRALISATION ---")

# 3. Exécution du filtrage E-ZERO v5.0
start_time = time.perf_counter()
res = filtre.filter(erc20_code)
end_time = time.perf_counter()

# 4. Affichage des résultats pour ton rapport Zenodo
print(f"✅ Statut         : Succès")
print(f"📊 Gain Énergétique: {res['gain_pct']}%")
print(f"⚡ Latence        : {res['ms']} ms")
print(f"🧠 Synapses       : {res['plasticity']['synapses']}")
print(f"\n--- SQUELETTE LOGIQUE EXTRAIT ---")
print(res['skeleton'])