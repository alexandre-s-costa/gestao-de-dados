import pandas as pd
import matplotlib.pyplot as plt

# Carregar o CSV (substitua pelo caminho real)
df = pd.read_csv("C:/Users/xanda/Downloads/investidores_limpo.csv", sep=";")

# ================================
# 1. Temporalidade 
# - Data de Adesão deve ser menor ou igual à data atual
# ================================
df['Data de Adesao'] = pd.to_datetime(df['Data de Adesao'], dayfirst=True, errors='coerce')
temporalidade = (df['Data de Adesao'] <= pd.Timestamp.today()).mean() * 100

# ================================
# 2. Consistência
# - Se "Operou 12 Meses" == 'S'
# ================================
df['consistencia'] = ~((df['Operou 12 Meses'] == 'S') & (df['Situacao da Conta'] == 'D'))
consistencia_percent = df['consistencia'].mean() * 100

# ================================
# 3. Validade
# - Idade >= 18
# - UF
# ================================
ufs_validas = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT',
               'MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO',
               'RR','SC','SP','SE','TO']
df['validade'] = (df['Idade'] >= 18) & (df['UF do Investidor'].isin(ufs_validas))
validade_percent = df['validade'].mean() * 100

# ================================
# 4. Unicidade
# ================================
unicidade_percent = df['Codigo do Investidor'].is_unique * 100

# ================================
# 5. Acurácia
# - Idade plausível (18–90)
# ================================
df['acuracia'] = df['Idade'].between(18, 90)
acuracia_percent = df['acuracia'].mean() * 100

# ================================
# Resumo em DataFrame
# ================================
qualidade = pd.DataFrame({
    'Dimensão': ['Temporalidade', 'Consistência', 'Validade', 'Unicidade', 'Acurácia'],
    'Percentual (%)': [
        temporalidade,
        consistencia_percent,
        validade_percent,
        unicidade_percent,
        acuracia_percent
    ]
})

print(qualidade)

# ================================
# Visualização com rótulos
# ================================
plt.figure(figsize=(8,5))
bars = plt.bar(qualidade['Dimensão'], qualidade['Percentual (%)'], color='skyblue')
plt.ylim(0, 110)
plt.title("Monitoramento da Qualidade dos Dados")
plt.ylabel("Percentual (%)")

# Inserir rótulos nas barras
for bar in bars:
    altura = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, altura + 1, 
             f"{altura:.1f}%", ha='center', va='bottom', fontsize=10)

plt.show()
