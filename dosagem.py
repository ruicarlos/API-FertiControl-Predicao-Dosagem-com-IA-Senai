import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

num_amostras = 50000
formulas_npk_comuns = [
    (20, 10, 10), (4, 14, 8), (10, 20, 20), (30, 0, 10),
    (5, 10, 5), (15, 15, 15), (10, 10, 10), (25, 5, 5),
    (0, 20, 20)
]

dados_gerados = []

for _ in range(num_amostras):
    n, p, k = formulas_npk_comuns[np.random.randint(0, len(formulas_npk_comuns))]
    
    volume_kg = np.random.randint(100, 50001)
    
    massa_amonia_g = (volume_kg * 1000) * (n / 100)
    massa_fosfato_g = (volume_kg * 1000) * (p / 100)
    massa_potassio_g = (volume_kg * 1000) * (k / 100)
    
    fator_ruido = 1 + (np.random.rand() - 0.5) * 0.02
    
    dados_gerados.append({
        "N": n,
        "P": p,
        "K": k,
        "volume": volume_kg,
        "amonia": massa_amonia_g * fator_ruido,
        "fosfato": massa_fosfato_g * fator_ruido,
        "potassio": massa_potassio_g * fator_ruido,
    })

df = pd.DataFrame(dados_gerados)

df.to_csv("dosagem_dataset.csv", index=False)
print(f"Base de dados com {num_amostras} amostras salva em 'dosagem_dataset.csv'")

X = df[["N", "P", "K", "volume"]]
y = df[["amonia", "fosfato", "potassio"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

modelo_corrigido = LinearRegression()
modelo_corrigido.fit(X_train, y_train)

joblib.dump(modelo_corrigido, "modelo_dosagem_corrigido.pkl")


y_pred = modelo_corrigido.predict(X_test)
score_r2 = r2_score(y_test, y_pred)
print(f"\nDesempenho do modelo (R² Score): {score_r2:.4f}")

def prever_dosagem_corrigida(n, p, k, volume_kg):
    entrada = [[n, p, k, volume_kg]]
    pred = modelo_corrigido.predict(entrada)[0]
    return {
        "amonia (g)": round(pred[0], 2),
        "fosfato (g)": round(pred[1], 2),
        "potassio (g)": round(pred[2], 2),
    }
resposta = prever_dosagem_corrigida(4, 14, 8, 40000)
print(resposta)

meta_n = 40000 * 1000 * (4 / 100)
meta_p = 40000 * 1000 * (14 / 100)
meta_k = 40000 * 1000 * (8 / 100)
print(f"\nMetas para conformidade: Amônia={meta_n:,.2f}g, Fosfato={meta_p:,.2f}g, Potássio={meta_k:,.2f}g")
