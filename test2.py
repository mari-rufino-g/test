import pandas as pd
import numpy as np

# Assumindo que os dados vêm em formato JSON correto
data = [item["json"] for item in items]
df = pd.DataFrame(data)

# Normalizar nomes das colunas
df.columns = df.columns.str.upper()

# Converter tipos de dados
df['TIM_DAY_ID'] = pd.to_datetime(df['TIM_DAY_ID'], format='%d/%m/%Y', errors='coerce')
df['METRIC_VALUE'] = pd.to_numeric(df['METRIC_VALUE'], errors='coerce')

# Remover linhas com dados inválidos
df = df.dropna(subset=['TIM_DAY_ID', 'METRIC_VALUE', 'SKILL_NAME'])

# Ordenar por SKILL_NAME e data para cálculos corretos
df = df.sort_values(['SKILL_NAME', 'METRIC_NAME', 'TIM_DAY_ID'])

# Reset index após ordenação
df = df.reset_index(drop=True)

# Definir as chaves para o groupby (incluindo METRIC_NAME se necessário)
keys = ['SKILL_NAME', 'METRIC_NAME']

# Calcular rolling stats
for window in [7, 14, 30]:
    # Calcular média móvel (deslocada 1 posição para não incluir o valor atual)
    rolling_mean = (
        df.groupby(keys)['METRIC_VALUE']
        .rolling(window, min_periods=1)
        .mean()
        .shift(1)
        .reset_index(level=keys, drop=True)
    )
    
    # Calcular desvio padrão móvel
    rolling_std = (
        df.groupby(keys)['METRIC_VALUE']
        .rolling(window, min_periods=1)
        .std(ddof=0)
        .shift(1)
        .reset_index(level=keys, drop=True)
    )
    
    # Atribuir valores calculados
    df[f'rolling_mean_{window}'] = rolling_mean.round(2)
    df[f'rolling_std_{window}'] = rolling_std.round(2)
    
    # Calcular Z-score (com proteção contra divisão por zero)
    z_score = np.where(
        rolling_std == 0, 
        0, 
        (df['METRIC_VALUE'] - rolling_mean) / rolling_std
    )
    df[f'z_score_{window}'] = np.round(z_score, 2)
    
    # Calcular mudança percentual (com proteção contra divisão por zero)
    pp_change = np.where(
        rolling_mean == 0, 
        0, 
        (df['METRIC_VALUE'] - rolling_mean) / rolling_mean * 100
    )
    df[f'pp_change_{window}'] = np.round(pp_change, 2)

# Criar coluna de data formatada
df['date'] = df['TIM_DAY_ID'].dt.strftime('%d/%m/%Y')

# Arredondar METRIC_VALUE
df['METRIC_VALUE'] = df['METRIC_VALUE'].round(2)

# Definir colunas desejadas (ajustando conforme dados disponíveis)
base_cols = ['date', 'SKILL_NAME', 'METRIC_VALUE', 'METRIC_NAME']

# Adicionar SIT_SITE_ID se existir
if 'SIT_SITE_ID' in df.columns:
    base_cols.insert(2, 'SIT_SITE_ID')

# Colunas de rolling stats
rolling_cols = (
    [f'rolling_mean_{w}' for w in [7, 14, 30]] +
    [f'pp_change_{w}' for w in [7, 14, 30]] +
    [f'z_score_{w}' for w in [7, 14, 30]]
)

cols = base_cols + rolling_cols

# Selecionar apenas colunas existentes
available_cols = [col for col in cols if col in df.columns]
df = df[available_cols]

# Ordenar por data (mais recente primeiro)
df = df.sort_values(['SKILL_NAME', 'METRIC_NAME', 'TIM_DAY_ID'], ascending=[True, True, False])

# Converter de volta para formato n8n
result = [{"json": row} for row in df.to_dict(orient="records")]

# Debug: Mostrar exemplo de cálculo
print("=== DEBUG: Exemplo de cálculo ===")
if len(df) > 0:
    # Pegar um exemplo específico
    example = df[(df['SKILL_NAME'] == 'mlcx') & (df['METRIC_NAME'] == 'CONVERSATION_FINISH_QTY')].head(10)
    if len(example) > 0:
        print("Dados ordenados por data (mais antigo primeiro para verificação):")
        example_sorted = example.sort_values('TIM_DAY_ID')
        for _, row in example_sorted.iterrows():
            print(f"{row['date']}: {row['METRIC_VALUE']} | Rolling Mean 7d: {row['rolling_mean_7']}")

return result
