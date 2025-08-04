import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
.comparison-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 0.5rem;
    text-align: center;
    margin-bottom: 1rem;
}
.spec-row {
    padding: 0.5rem;
    margin: 0.25rem 0;
    border-left: 4px solid #667eea;
    background-color: #f8f9fa;
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
            'launch_year': 2023
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
            'launch_year': 2024
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
            'launch_year': 2024
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
            'launch_year': 2024
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
            'launch_year': 2024
        },
        'OnePlus Open': {
            'brand': 'OnePlus',
            'display_type': 'OLED',
            'screen_size': 7.82,
            'resolution': '1440 x 2268',
            'pixel_density': 426,
            'refresh_rate': 120,
            'brightness': 2800,
            'touch_sampling': 1000,
            'durable_screen': True,
            'hdr10': True,
            'price': 8999,
            'launch_year': 2023
        }
    }

# Função para criar gráfico de barras
def create_bar_chart(data, metric, title, color='#667eea'):
    fig = px.bar(
        x=list(data.keys()),
        y=[data[phone][metric] for phone in data.keys()],
        title=title,
        color_discrete_sequence=[color]
    )
    fig.update_layout(
        xaxis_title="Smartphones",
        yaxis_title=title,
        showlegend=False,
        height=400
    )
    return fig

# Função para criar gráfico radar
def create_radar_chart(selected_phones, phone_data):
    categories = ['Densidade de Pixels', 'Brilho', 'Taxa de Toque', 'Tamanho da Tela', 'Taxa de Atualização']
    
    fig = go.Figure()
    
    for phone in selected_phones:
        data = phone_data[phone]
        values = [
            data['pixel_density'] / 500 * 100,  # Normalizado para 0-100
            data['brightness'] / 3000 * 100,
            data['touch_sampling'] / 1000 * 100,
            data['screen_size'] / 8 * 100,
            data['refresh_rate'] / 120 * 100
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=phone
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Comparação Radar das Especificações"
    )
    
    return fig

# Interface principal
def main():
    # Header
    st.markdown("""
    <div class="comparison-header">
        <h1>📱 Dashboard de Comparação de Smartphones</h1>
        <p>Compare as especificações dos principais smartphones do mercado</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    phone_data = load_phone_data()
    
    # Sidebar para seleção de smartphones
    st.sidebar.header("🔧 Configurações")
    
    # Seleção múltipla de smartphones
    selected_phones = st.sidebar.multiselect(
        "Selecione os smartphones para comparar:",
        options=list(phone_data.keys()),
        default=['iPhone 15 Pro', 'Galaxy S24', 'Vivo Y400 4G'],
        help="Você pode selecionar até 6 smartphones"
    )
    
    if not selected_phones:
        st.warning("⚠️ Selecione pelo menos um smartphone para comparar!")
        return
    
    # Filtros adicionais
    st.sidebar.subheader("📊 Filtros")
    
    show_price_filter = st.sidebar.checkbox("Filtrar por preço")
    if show_price_filter:
        price_range = st.sidebar.slider(
            "Faixa de preço (R$)",
            min_value=0,
            max_value=10000,
            value=(1000, 8000),
            step=500
        )
        selected_phones = [
            phone for phone in selected_phones 
            if price_range[0] <= phone_data[phone]['price'] <= price_range[1]
        ]
    
    if not selected_phones:
        st.warning("⚠️ Nenhum smartphone na faixa de preço selecionada!")
        return
    
    # Exibir dados selecionados
    filtered_data = {phone: phone_data[phone] for phone in selected_phones}
    
    # Seção de resumo
    st.header("📋 Resumo dos Dispositivos Selecionados")
    
    cols = st.columns(len(selected_phones))
    for i, phone in enumerate(selected_phones):
        with cols[i]:
            data = phone_data[phone]
            st.markdown(f"""
            <div class="metric-card">
                <h3>📱 {phone}</h3>
                <p><strong>Marca:</strong> {data['brand']}</p>
                <p><strong>Tela:</strong> {data['screen_size']}" {data['display_type']}</p>
                <p><strong>Preço:</strong> R$ {data['price']:,}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Tabela de comparação detalhada
    st.header("📊 Comparação Detalhada")
    
    # Criar DataFrame para exibição
    comparison_data = []
    for phone in selected_phones:
        data = phone_data[phone]
        comparison_data.append({
            'Smartphone': phone,
            'Marca': data['brand'],
            'Tela (pol)': data['screen_size'],
            'Resolução': data['resolution'],
            'Densidade (ppi)': data['pixel_density'],
            'Taxa Atualização (Hz)': data['refresh_rate'],
            'Brilho (nits)': data['brightness'],
            'Taxa Toque (Hz)': data['touch_sampling'],
            'Tela Resistente': '✅' if data['durable_screen'] else '❌',
            'HDR10': '✅' if data['hdr10'] else '❌',
            'Preço (R$)': f"R$ {data['price']:,}"
        })
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True)
    
    # Gráficos comparativos
    st.header("📈 Análises Visuais")
    
    # Três colunas para gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de densidade de pixels
        fig_density = create_bar_chart(
            filtered_data, 
            'pixel_density', 
            'Densidade de Pixels (PPI)',
            '#FF6B6B'
        )
        st.plotly_chart(fig_density, use_container_width=True)
        
        # Gráfico de brilho
        fig_brightness = create_bar_chart(
            filtered_data, 
            'brightness', 
            'Brilho Máximo (nits)',
            '#4ECDC4'
        )
        st.plotly_chart(fig_brightness, use_container_width=True)
    
    with col2:
        # Gráfico de preço
        fig_price = create_bar_chart(
            filtered_data, 
            'price', 
            'Preço (R$)',
            '#45B7D1'
        )
        st.plotly_chart(fig_price, use_container_width=True)
        
        # Gráfico de taxa de toque
        fig_touch = create_bar_chart(
            filtered_data, 
            'touch_sampling', 
            'Taxa de Amostragem de Toque (Hz)',
            '#96CEB4'
        )
        st.plotly_chart(fig_touch, use_container_width=True)
    
    # Gráfico radar
    if len(selected_phones) >= 2:
        st.subheader("🎯 Análise Radar Comparativa")
        fig_radar = create_radar_chart(selected_phones, phone_data)
        st.plotly_chart(fig_radar, use_container_width=True)
    
    # Análise de custo-benefício
    st.header("💰 Análise Custo-Benefício")
    
    # Calcular score de custo-benefício
    scores = {}
    for phone in selected_phones:
        data = phone_data[phone]
        # Score baseado em especificações normalizadas vs preço
        tech_score = (
            data['pixel_density'] / 500 * 25 +
            data['brightness'] / 3000 * 25 +
            data['touch_sampling'] / 1000 * 25 +
            data['refresh_rate'] / 120 * 25
        )
        cost_benefit = tech_score / (data['price'] / 1000)  # Score por mil reais
        scores[phone] = round(cost_benefit, 2)
    
    # Exibir ranking
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    st.subheader("🏆 Ranking Custo-Benefício")
    for i, (phone, score) in enumerate(sorted_scores):
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.markdown(f"**#{i+1}**")
        with col2:
            st.markdown(f"**{phone}**")
        with col3:
            st.markdown(f"Score: **{score}**")
    
    # Recomendações
    st.header("💡 Recomendações")
    
    if len(selected_phones) > 1:
        best_overall = max(scores.items(), key=lambda x: x[1])[0]
        most_expensive = max(selected_phones, key=lambda x: phone_data[x]['price'])
        cheapest = min(selected_phones, key=lambda x: phone_data[x]['price'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success(f"🏆 **Melhor Custo-Benefício**\n\n{best_overall}")
        
        with col2:
            st.info(f"💎 **Premium**\n\n{most_expensive}")
        
        with col3:
            st.warning(f"💵 **Mais Econômico**\n\n{cheapest}")
    
    # Footer com informações
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>📱 Dashboard desenvolvido com Streamlit | Dados atualizados em 2024</p>
        <p>💡 Use os filtros na barra lateral para personalizar sua análise</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
