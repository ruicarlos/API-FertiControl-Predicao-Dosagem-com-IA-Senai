import json
import datetime
import os
from decimal import Decimal
from app.database 

class BackupService:
    def __init__(self):
        self.backup_dir = "backups/"
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def _json_serializer(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return str(obj)

    def gerar_backup_logico(self):
        tabelas_do_sistema = [
            'usuarios',             
            'empresas',              
            'producoes',             
            'fertilizantes',         
            'sensores',              
            'rastreios',             
            'laudos',               
            'indicadores_dashboard'  
        ]

        dados_backup = {
            "metadata": {
                "data_geracao": datetime.datetime.now().isoformat(),
                "versao_sistema": "1.0.0",
                "entidades_exportadas": len(tabelas_do_sistema)
            },
            "dados": {}
        }

        try:
            for tabela in tabelas_do_sistema:
                print(f"Processando tabela: {tabela}...")
                
                 cursor.execute(f"SELECT * FROM {tabela}")
                 colunas = [desc[0] for desc in cursor.description]
                 registros = [dict(zip(colunas, row)) for row in cursor.fetchall()]
                
                dados_backup["dados"][tabela] = registros

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.backup_dir}backup_full_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(
                    dados_backup, 
                    f, 
                    indent=4, 
                    default=self._json_serializer 
                )
                
            print(f"Backup realizado com sucesso: {filename}")
            return filename

        except Exception as e:
            print(f"Erro crítico no backup: {str(e)}")
            return None
        finally:
             if conn: conn.close()
            pass

if __name__ == "__main__":
    service = BackupService()
    service.gerar_backup_logico()