import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Comparação de Smartphones",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.comparison-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
}
.spec-row {
    padding: 1rem;
    margin: 0.5rem 0;
    border-left: 4px solid #667eea;
    background-color: #f8f9fa;
    border-radius: 5px;
}
.recommendation-card {
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    margin: 0.5rem;
}
.best-choice {
    background-color: #d4edda;
    border: 2px solid #28a745;
    color: #155724;
}
.premium-choice {
    background-color: #cce7ff;
    border: 2px solid #007bff;
    color: #004085;
}
.budget-choice {
    background-color: #fff3cd;
    border: 2px solid #ffc107;
    color: #856404;
}
.progress-bar {
    background-color: #e9ecef;
    border-radius: 10px;
    height: 20px;
    margin: 5px 0;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 0.3s ease;
}
</style>
""", unsafe_allow_html=True)

# Base de dados dos smartphones
@st.cache_data
def load_phone_data():
    return {
        'iPhone 15 Pro': {
            'brand': 'Apple',
            'display_type': 'OLED',
            'screen_size': 6.1,
            'resolution': '1179 x 2556',
            'pixel_density': 460,
            'refresh_rate': 120,
            'brightness': 2000,
            'touch_sampling': 240,
            'durable_screen': True,
            'hdr10': True,
            'price': 7999,
            'launch_year': 2023,
            'emoji': '🍎'
        },
        'Galaxy S24': {
            'brand': 'Samsung',
            'display_type': 'OLED',
            'screen_size': 6.2,
            'resolution': '1080 x 2340',
            'pixel_density': 416,
            'refresh_rate': 120,
            'brightness': 2600,
            'touch_sampling': 240,
            'durable_screen': True,
            'hdr10': True,
            'price': 6499,
            'launch_year': 2024,
            'emoji': '📱'
        },
        'Vivo Y400 4G': {
            'brand': 'Vivo',
            'display_type': 'OLED',
            'screen_size': 6.67,
            'resolution': '1080 x 2400',
            'pixel_density': 395,
            'refresh_rate': 120,
            'brightness': 1200,
            'touch_sampling': 180,
            'durable_screen': False,
            'hdr10': False,
            'price': 1299,
            'launch_year': 2024,
            'emoji': '📳'
        },
        'Vivo Y400 5G': {
            'brand': 'Vivo',
            'display_type': 'OLED',
            'screen_size': 6.67,
            'resolution': '1080 x 2400',
            'pixel_density': 395,
            'refresh_rate': 120,
            'brightness': 1200,
            'touch_sampling': 180,
            'durable_screen': False,
            'hdr10': True,
            'price': 1599,
            'launch_year': 2024,
            'emoji': '📳'
        },
        'Xiaomi 14': {
            'brand': 'Xiaomi',
            'display_type': 'OLED',
            'screen_size': 6.36,
            'resolution': '1200 x 2670',
            'pixel_density': 460,
            'refresh_rate': 120,
            'brightness': 3000,
            'touch_sampling': 480,
            'durable_screen': True,
            'hdr10': True,
            'price': 4999,
            'launch_year': 2024,
            'emoji': '🤖'
        },
        'OnePlus Open': {
            'brand': 'OnePlus',
            'display_type': 'OLED Dobrável',
            'screen_size': 7.82,
            'resolution': '1440 x 2268',
            'pixel_density': 426,
            'refresh_rate': 120,
            'brightness': 2800,
            'touch_sampling': 1000,
            'durable_screen': True,
            'hdr10': True,
            'price': 8999,
            'launch_year': 2023,
            'emoji': '📲'
        }
    }

# Função para criar barra de progresso HTML
def create_progress_bar(value, max_value, color="#667eea", label=""):
    percentage = min((value / max_value) * 100, 100)
    return f"""
    <div style="margin: 5px 0;">
        <small>{label}</small>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {percentage}%; background-color: {color};"></div>
        </div>
        <small>{value} / {max_value}</small>
    </div>
    """

# Função para normalizar valores para comparação
def normalize_value(value, min_val, max_val):
    return ((value - min_val) / (max_val - min_val)) * 100

# Interface principal
def main():
    # Header
    st.markdown("""
    <div class="comparison-header">
        <h1>📱 Dashboard de Comparação de Smartphones</h1>
        <p>Compare as especificações dos principais smartphones do mercado brasileiro</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    phone_data = load_phone_data()
    
    # Sidebar para seleção de smartphones
    st.sidebar.header("🔧 Configurações da Comparação")
    
    # Informações sobre os dados
    st.sidebar.markdown("""
    ### 📊 Sobre os Dados
    - **Smartphones:** 6 modelos populares
    - **Especificações:** Display, performance, preço
    - **Atualização:** 2024
    """)
    
    # Seleção múltipla de smartphones
    selected_phones = st.sidebar.multiselect(
        "Selecione os smartphones para comparar:",
        options=list(phone_data.keys()),
        default=['iPhone 15 Pro', 'Galaxy S24', 'Xiaomi 14'],
        help="Selecione de 1 a 6 smartphones para análise detalhada"
    )
    
    if not selected_phones:
        st.warning("⚠️ Selecione pelo menos um smartphone para começar a comparação!")
        st.info("👈 Use a barra lateral para escolher os dispositivos")
        return
    
    # Filtros avançados
    st.sidebar.subheader("🎯 Filtros Avançados")
    
    # Filtro por marca
    available_brands = list(set([phone_data[phone]['brand'] for phone in selected_phones]))
    if len(available_brands) > 1:
        brand_filter = st.sidebar.multiselect(
            "Filtrar por marca:",
            options=available_brands,
            default=available_brands
        )
        selected_phones = [phone for phone in selected_phones if phone_data[phone]['brand'] in brand_filter]
    
    # Filtro por preço
    show_price_filter = st.sidebar.checkbox("Ativar filtro de preço")
    if show_price_filter:
        min_price = min([phone_data[phone]['price'] for phone in selected_phones])
        max_price = max([phone_data[phone]['price'] for phone in selected_phones])
        
        price_range = st.sidebar.slider(
            "Faixa de preço (R$)",
            min_value=int(min_price),
            max_value=int(max_price),
            value=(int(min_price), int(max_price)),
            step=500,
            format="R$ %d"
        )
        selected_phones = [
            phone for phone in selected_phones 
            if price_range[0] <= phone_data[phone]['price'] <= price_range[1]
        ]
    
    if not selected_phones:
        st.warning("⚠️ Nenhum smartphone atende aos filtros selecionados!")
        return
    
    # Estatísticas gerais
    st.sidebar.subheader("📈 Estatísticas")
    avg_price = np.mean([phone_data[phone]['price'] for phone in selected_phones])
    st.sidebar.metric("Preço Médio", f"R$ {avg_price:,.0f}")
    st.sidebar.metric("Dispositivos Selecionados", len(selected_phones))
    
    # Seção de cards dos dispositivos
    st.header("📋 Dispositivos Selecionados")
    
    cols = st.columns(min(len(selected_phones), 3))
    for i, phone in enumerate(selected_phones):
        with cols[i % 3]:
            data = phone_data[phone]
            st.markdown(f"""
            <div class="metric-card">
                <h3>{data['emoji']} {phone}</h3>
                <p><strong>{data['brand']}</strong></p>
                <p>📏 {data['screen_size']}" {data['display_type']}</p>
                <p>💰 R$ {data['price']:,}</p>
                <p>🗓️ {data['launch_year']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Análise comparativa com métricas
    st.header("📊 Análise Comparativa")
    
    # Preparar dados para comparação
    comparison_metrics = {}
    for phone in selected_phones:
        data = phone_data[phone]
        comparison_metrics[phone] = {
            'Densidade de Pixels': data['pixel_density'],
            'Brilho (nits)': data['brightness'],
            'Taxa de Toque (Hz)': data['touch_sampling'],
            'Tamanho da Tela (pol)': data['screen_size'],
            'Preço (R$)': data['price']
        }
    
    # Exibir métricas com barras de progresso
    metrics_to_show = ['Densidade de Pixels', 'Brilho (nits)', 'Taxa de Toque (Hz)']
    
    for metric in metrics_to_show:
        st.subheader(f"🔍 {metric}")
        values = [comparison_metrics[phone][metric] for phone in selected_phones]
        max_value = max(values)
        
        cols = st.columns(len(selected_phones))
        for i, phone in enumerate(selected_phones):
            with cols[i]:
                value = comparison_metrics[phone][metric]
                progress_percentage = (value / max_value) * 100
                
                # Escolher cor baseada na performance
                if progress_percentage >= 80:
                    color = "#28a745"  # Verde
                elif progress_percentage >= 60:
                    color = "#ffc107"  # Amarelo
                else:
                    color = "#dc3545"  # Vermelho
                
                st.markdown(f"""
                <div class="spec-row">
                    <h4>{phone_data[phone]['emoji']} {phone}</h4>
                    <p><strong>{value:,}</strong></p>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: {progress_percentage}%; background-color: {color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Tabela de comparação completa
    st.header("📋 Tabela de Comparação Detalhada")
    
    # Criar DataFrame
    comparison_data = []
    for phone in selected_phones:
        data = phone_data[phone]
        comparison_data.append({
            'Smartphone': f"{data['emoji']} {phone}",
            'Marca': data['brand'],
            'Tela': f"{data['screen_size']}\"",
            'Tipo Display': data['display_type'],
            'Resolução': data['resolution'],
            'Densidade (ppi)': f"{data['pixel_density']} ppi",
            'Taxa (Hz)': f"{data['refresh_rate']} Hz",
            'Brilho (nits)': f"{data['brightness']:,}",
            'Toque (Hz)': f"{data['touch_sampling']} Hz",
            'Tela Resistente': '✅ Sim' if data['durable_screen'] else '❌ Não',
            'HDR10': '✅ Sim' if data['hdr10'] else '❌ Não',
            'Preço': f"R$ {data['price']:,}"
        })
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)
    
    # Gráficos usando Streamlit nativo
    st.header("📈 Visualizações")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Comparação de Preços")
        chart_data = pd.DataFrame({
            'Smartphone': selected_phones,
            'Preço (R$)': [phone_data[phone]['price'] for phone in selected_phones]
        })
        st.bar_chart(chart_data.set_index('Smartphone')['Preço (R$)'])
        
    with col2:
        st.subheader("🔆 Brilho da Tela")
        brightness_data = pd.DataFrame({
            'Smartphone': selected_phones,
            'Brilho (nits)': [phone_data[phone]['brightness'] for phone in selected_phones]
        })
        st.bar_chart(brightness_data.set_index('Smartphone')['Brilho (nits)'])
    
    # Análise de custo-benefício
    st.header("💡 Análise Inteligente")
    
    # Calcular scores
    scores = {}
    for phone in selected_phones:
        data = phone_data[phone]
        # Score baseado em especificações técnicas
        tech_score = (
            (data['pixel_density'] / 500) * 20 +
            (data['brightness'] / 3000) * 20 +
            (data['touch_sampling'] / 1000) * 20 +
            (data['refresh_rate'] / 120) * 20 +
            (20 if data['durable_screen'] else 0) +
            (20 if data['hdr10'] else 0)
        )
        # Custo-benefício (score técnico / preço em milhares)
        cost_benefit = tech_score / (data['price'] / 1000)
        scores[phone] = {
            'tech_score': round(tech_score, 1),
            'cost_benefit': round(cost_benefit, 2)
        }
    
    # Rankings
    best_tech = max(scores.items(), key=lambda x: x[1]['tech_score'])
    best_value = max(scores.items(), key=lambda x: x[1]['cost_benefit'])
    most_expensive = max(selected_phones, key=lambda x: phone_data[x]['price'])
    cheapest = min(selected_phones, key=lambda x: phone_data[x]['price'])
    
    # Exibir recomendações
    st.subheader("🏆 Recomendações Personalizadas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="recommendation-card best-choice">
            <h4>🏆 Melhor Custo-Benefício</h4>
            <h3>{phone_data[best_value[0]]['emoji']} {best_value[0]}</h3>
            <p><strong>Score: {best_value[1]['cost_benefit']}</strong></p>
            <p>R$ {phone_data[best_value[0]]['price']:,}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="recommendation-card premium-choice">
            <h4>💎 Mais Avançado</h4>
            <h3>{phone_data[best_tech[0]]['emoji']} {best_tech[0]}</h3>
            <p><strong>Score Técnico: {best_tech[1]['tech_score']}</strong></p>
            <p>R$ {phone_data[best_tech[0]]['price']:,}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="recommendation-card budget-choice">
            <h4>💵 Mais Econômico</h4>
            <h3>{phone_data[cheapest]['emoji']} {cheapest}</h3>
            <p><strong>Entrada</strong></p>
            <p>R$ {phone_data[cheapest]['price']:,}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Ranking completo
    st.subheader("📊 Ranking Geral (Custo-Benefício)")
    
    sorted_phones = sorted(selected_phones, key=lambda x: scores[x]['cost_benefit'], reverse=True)
    
    for i, phone in enumerate(sorted_phones):
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        
        with col1:
            if i == 0:
                st.markdown("🥇")
            elif i == 1:
                st.markdown("🥈")
            elif i == 2:
                st.markdown("🥉")
            else:
                st.markdown(f"**#{i+1}**")
        
        with col2:
            st.markdown(f"**{phone_data[phone]['emoji']} {phone}**")
        
        with col3:
            st.markdown(f"Score: **{scores[phone]['cost_benefit']}**")
        
        with col4:
            st.markdown(f"R$ **{phone_data[phone]['price']:,}**")
    
    # Insights e conclusões
    st.header("🎯 Insights da Análise")
    
    insights = []
    
    if len(selected_phones) > 1:
        price_diff = max([phone_data[phone]['price'] for phone in selected_phones]) - min([phone_data[phone]['price'] for phone in selected_phones])
        insights.append(f"💰 A diferença de preço entre o mais caro e mais barato é de R$ {price_diff:,}")
        
        avg_brightness = np.mean([phone_data[phone]['brightness'] for phone in selected_phones])
        insights.append(f"🔆 O brilho médio das telas é de {avg_brightness:.0f} nits")
        
        hdr_phones = [phone for phone in selected_phones if phone_data[phone]['hdr10']]
        insights.append(f"📺 {len(hdr_phones)} de {len(selected_phones)} smartphones suportam HDR10")
    
    for insight in insights:
        st.info(insight)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>📱 <strong>Dashboard de Comparação de Smartphones</strong></p>
        <p>Desenvolvido com ❤️ usando Streamlit | Dados atualizados em 2024</p>
        <p>💡 <em>Dica: Use os filtros da barra lateral para personalizar sua análise</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
