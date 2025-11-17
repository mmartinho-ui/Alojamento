import json
import os
from typing import List, Dict, Optional

class GestorDados:
    def __init__(self, ficheiro_bd: str):
        self.ficheiro_bd = ficheiro_bd
        self.dados = self.carregar_dados()

    def carregar_dados(self) -> List[Dict]:
        if not os.path.exists(self.ficheiro_bd) or os.path.getsize(self.ficheiro_bd) == 0:
            self.guardar_dados([])
            return []
        try:
            with open(self.ficheiro_bd, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def guardar_dados(self, dados: List[Dict]):
        try:
            with open(self.ficheiro_bd, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao guardar: {e}")

    def obter_todos(self) -> List[Dict]:
        return self.dados

    def adicionar(self, objeto_dado) -> bool:
        self.dados.append(objeto_dado.to_dict())
        
        self.guardar_dados(self.dados)
        return True
    
    def encontrar_por_campo(self, campo: str, valor) -> Optional[Dict]:
        for item in self.dados:
            if item.get(campo) == valor:
                return item
        return None

    def gerar_novo_id(self, campo_id: str) -> int:
        if not self.dados: return 1
        return max([item.get(campo_id, 0) for item in self.dados]) + 1
    
    def eliminar_por_campo(self, campo: str, valor) -> bool:
        item_para_eliminar = self.encontrar_por_campo(campo, valor)
        
        if item_para_eliminar:
            self.dados.remove(item_para_eliminar)
            self.guardar_dados(self.dados)
            return True
        else:
            return False