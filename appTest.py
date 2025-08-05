import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Configuração da página
st.set_page_config(
    page_title="Comparador de Produtos",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para um design mais limpo
st.markdown("""
<style>
/* Reset e base */
.main > div {
    padding-top: 2rem;
}

/* Header */
.header-container {
    background: white;
    padding: 2rem 0 1rem 0;
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 2rem;
}

.header-title {
    font-size: 2rem;
    font-weight: 700;
    color: #1a1a1a;
    margin: 0;
    text-align: center;
}

.header-subtitle {
    font-size: 1rem;
    color: #666;
    text-align: center;
    margin-top: 0.5rem;
}

/* Sidebar styling */
.sidebar-header {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border-left: 4px solid #007bff;
}

/* Product cards */
.product-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}

.product-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transform: translateY(-2px);
}

.product-image {
    width: 60px;
    height: 60px;
    background: #f8f9fa;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    margin-bottom: 1rem;
}

.product-name {
    font-size: 1.1rem;
    font-weight: 600;
    color: #1a1a1a;
    margin: 0.5rem 0;
}

.product-price {
    font-size: 1.5rem;
    font-weight: 700;
    color: #007bff;
    margin: 0.8rem 0;
}

.product-year {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 1rem;
}

.add-button {
    background: #007bff;
    color: white;
    border: none;
    padding: 0.7rem 1rem;
    border-radius: 6px;
    width: 100%;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.3s ease;
}

.add-button:hover {
    background: #0056b3;
}

.remove-button {
    background: #dc3545;
    color: white;
    border: none;
    padding: 0.7rem 1rem;
    border-radius: 6px;
    width: 100%;
    font-weight: 600;
    cursor: pointer;
}

/* Comparison section */
.comparison-header {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    margin-bottom: 2rem;
    text-align: center;
}

.comparison-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1a1a1a;
    margin: 0;
}

.spec-table {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.spec-row {
    border-bottom: 1px solid #f0f0f0;
    padding: 1rem;
}

.spec-row:last-child {
    border-bottom: none;
}

.spec-label {
    font-weight: 600;
    color: #333;
    padding: 0.5rem 0;
}

.best-price {
    background: #d4edda;
    color: #155724;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-weight: 600;
}

.most-recent {
    background: #cce7ff;
    color: #004085;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-weight: 600;
}

.premium {
    background: #fff3cd;
    color: #856404;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-weight: 600;
}

/* Clear button */
.clear-button {
    background: #6c757d;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-size: 0.9rem;
    cursor: pointer;
    margin-top: 1rem;
}

/* Price history charts */
.chart-container {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}

.chart-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1rem;
    text-align: center;
}

.current-price {
    font-size: 1.2rem;
    font-weight: 700;
    color: #007bff;
    text-align: center;
    margin-bottom: 0.5rem;
}

.price-trend {
    font-size: 0.9rem;
    text-align: center;
    margin-bottom: 1rem;
}

.price-down {
    color: #28a745;
}

.price-up {
    color: #dc3545;
}

/* Recommendation cards */
.recommendation-card {
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
    margin-bottom: 1rem;
}

.rec-success {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
}

.rec-info {
    background-color: #d1ecf1;
    border: 1px solid #bee5eb;
    color: #0c5460;
}

.rec-warning {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    color: #856404;
}
</style>
""", unsafe_allow_html=True)

# Base de dados dos produtos
@st.cache_data
def load_product_data():
    return {
        'iPhone 15 Pro Max': {
            'brand': 'Apple',
            'category': 'Celulares',
            'price': 11199,
            'year': 2023,
            'launch_date': '2023-09-15',
            'specifications': {
                'Ano de Lançamento': 2023,
                'Memória RAM': '8GB',
                'Armazenamento': '256GB',
                'Processador': 'A17 Pro',
                'Tela': '6.7" Super Retina XDR',
                'Bateria': '4441 mAh',
                'Câmera': '48MP + 12MP + 12MP',
                'Sistema Operacional': 'iOS 17',
                'Peso': '221g'
            },
            'icon': '📱'
        },
        'Galaxy S24 Ultra': {
            'brand': 'Samsung',
            'category': 'Celulares',
            'price': 12299,
            'year': 2024,
            'launch_date': '2024-01-17',
            'specifications': {
                'Ano de Lançamento': 2024,
                'Memória RAM': '12GB',
                'Armazenamento': '512GB',
                'Processador': 'Snapdragon 8 Gen 3',
                'Tela': '6.8" Dynamic AMOLED 2X',
                'Bateria': '5000 mAh',
                'Câmera': '200MP + 50MP + 10MP + 12MP',
                'Sistema Operacional': 'Android 14',
                'Peso': '232g'
            },
            'icon': '📱'
        },
        'Pixel 8 Pro': {
            'brand': 'Google',
            'category': 'Celulares',
            'price': 9999,
            'year': 2023,
            'launch_date': '2023-10-04',
            'specifications': {
                'Ano de Lançamento': 2023,
                'Memória RAM': '12GB',
                'Armazenamento': '128GB',
                'Processador': 'Google Tensor G3',
                'Tela': '6.7" LTPO OLED',
                'Bateria': '5050 mAh',
                'Câmera': '50MP + 48MP + 48MP',
                'Sistema Operacional': 'Android 14',
                'Peso': '213g'
            },
            'icon': '📱'
        },
        'Xiaomi 14 Ultra': {
            'brand': 'Xiaomi',
            'category': 'Celulares',
            'price': 8999,
            'year': 2024,
            'launch_date': '2024-02-25',
            'specifications': {
                'Ano de Lançamento': 2024,
                'Memória RAM': '16GB',
                'Armazenamento': '512GB',
                'Processador': 'Snapdragon 8 Gen 3',
                'Tela': '6.73" AMOLED',
                'Bateria': '5300 mAh',
                'Câmera': '50MP + 50MP + 50MP + 50MP',
                'Sistema Operacional': 'MIUI 15',
                'Peso': '229g'
            },
            'icon': '📱'
        },
        'OnePlus 12': {
            'brand': 'OnePlus',
            'category': 'Celulares',
            'price': 7499,
            'year': 2024,
            'launch_date': '2024-01-23',
            'specifications': {
                'Ano de Lançamento': 2024,
                'Memória RAM': '12GB',
                'Armazenamento': '256GB',
                'Processador': 'Snapdragon 8 Gen 3',
                'Tela': '6.82" LTPO AMOLED',
                'Bateria': '5400 mAh',
                'Câmera': '50MP + 64MP + 48MP',
                'Sistema Operacional': 'OxygenOS 14',
                'Peso': '220g'
            },
            'icon': '📱'
        },
        'Vivo X100 Pro': {
            'brand': 'Vivo',
            'category': 'Celulares',
            'price': 6999,
            'year': 2024,
            'launch_date': '2024-01-08',
            'specifications': {
                'Ano de Lançamento': 2024,
                'Memória RAM': '12GB',
                'Armazenamento': '256GB',
                'Processador': 'Dimensity 9300',
                'Tela': '6.78" LTPO AMOLED',
                'Bateria': '5400 mAh',
                'Câmera': '50MP + 50MP + 50MP',
                'Sistema Operacional': 'Funtouch OS 14',
                'Peso': '225g'
            },
            'icon': '📱'
        }
    }

def generate_price_history(current_price, months=6):
    """Gera histórico de preços simulado"""
    dates = []
    prices = []
    
    start_date = datetime.now() - timedelta(days=months*30)
    
    # Começar com um preço um pouco mais alto
    base_price = current_price * 1.15
    
    for i in range(months * 4):  # 4 pontos por mês
        date = start_date + timedelta(days=i*7)  # A cada semana
        
        # Simular flutuação de preços com tendência de queda
        variation = random.uniform(-0.08, 0.03)  # Mais chance de cair
        base_price = base_price * (1 + variation)
        
        # Garantir que não fique muito abaixo do preço atual
        if base_price < current_price * 0.85:
            base_price = current_price * random.uniform(0.9, 1.1)
            
        dates.append(date.strftime('%d/%m'))
        prices.append(max(base_price, current_price * 0.8))
    
    # Garantir que o último preço seja próximo ao atual
    prices[-1] = current_price
    
    return dates, prices

def create_price_chart_data(product_name, current_price):
    """Cria dados para gráfico de histórico de preços usando Streamlit nativo"""
    dates, prices = generate_price_history(current_price)
    
    # Calcular tendência
    price_change = (prices[-1] - prices[0]) / prices[0] * 100
    trend_text = f"↓ R$ {abs(prices[0] - prices[-1]):.0f}" if price_change < 0 else f"↑ R$ {abs(prices[-1] - prices[0]):.0f}"
    trend_class = "price-down" if price_change < 0 else "price-up"
    
    # Criar DataFrame para o gráfico
    chart_data = pd.DataFrame({
        'Data': dates,
        'Preço': prices
    })
    
    return chart_data, trend_text, trend_class

def main():
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Comparador de Produtos</h1>
        <p class="header-subtitle">Compare celulares e computadores lado a lado</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    product_data = load_product_data()
    
    # Inicializar session state
    if 'selected_products' not in st.session_state:
        st.session_state.selected_products = []
    
    # Layout principal
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Seção de seleção de produtos
        st.markdown("""
        <div class="sidebar-header">
            <h3>Produtos Selecionados</h3>
            <p>Até 4 produtos selecionados</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar produtos selecionados
        if st.session_state.selected_products:
            for product in st.session_state.selected_products:
                data = product_data[product]
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 0.5rem; background: #f8f9fa; border-radius: 6px; margin-bottom: 0.5rem;">
                    <span style="margin-right: 0.5rem;">{data['icon']}</span>
                    <span style="flex: 1; font-weight: 500;">{product}</span>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🗑️ Limpar", key="clear_all", help="Remove todos os produtos"):
                st.session_state.selected_products = []
                st.rerun()
        else:
            st.info("Nenhum produto selecionado")
        
        st.markdown("---")
        
        # Seção de seleção de produtos
        st.markdown("""
        <h4>Selecionar Produtos</h4>
        <p>Escolha até 4 produtos para comparar</p>
        """, unsafe_allow_html=True)
        
        # Filtros
        categories = ['Todos'] + list(set([data['category'] for data in product_data.values()]))
        selected_category = st.selectbox("Categoria", categories)
        
        brands = ['Todas'] + list(set([data['brand'] for data in product_data.values()]))
        selected_brand = st.selectbox("Marca", brands)
        
        # Filtrar produtos
        filtered_products = {}
        for name, data in product_data.items():
            if selected_category != 'Todos' and data['category'] != selected_category:
                continue
            if selected_brand != 'Todas' and data['brand'] != selected_brand:
                continue
            filtered_products[name] = data
        
        # Exibir produtos disponíveis
        for product_name, data in filtered_products.items():
            is_selected = product_name in st.session_state.selected_products
            can_add = len(st.session_state.selected_products) < 4
            
            st.markdown(f"""
            <div class="product-card">
                <div class="product-image">{data['icon']}</div>
                <div class="product-name">{product_name}</div>
                <div class="product-price">R$ {data['price']:,}</div>
                <div class="product-year">{data['year']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if is_selected:
                if st.button("❌ Remover da Comparação", key=f"remove_{product_name}"):
                    st.session_state.selected_products.remove(product_name)
                    st.rerun()
            else:
                if can_add:
                    if st.button("➕ Adicionar à Comparação", key=f"add_{product_name}"):
                        st.session_state.selected_products.append(product_name)
                        st.rerun()
                else:
                    st.button("Limite atingido (4 produtos)", disabled=True, key=f"disabled_{product_name}")
    
    with col2:
        if not st.session_state.selected_products:
            st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem; color: #666;">
                <h3>👈 Selecione produtos para comparar</h3>
                <p>Escolha até 4 produtos na barra lateral para ver a comparação detalhada</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Header da comparação
            st.markdown("""
            <div class="comparison-header">
                <h2 class="comparison-title">Comparação de Produtos</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Tabela de especificações
            st.markdown("### 📋 Especificações")
            
            # Criar tabela de comparação
            all_specs = set()
            for product in st.session_state.selected_products:
                all_specs.update(product_data[product]['specifications'].keys())
            
            # Cabeçalho da tabela
            cols = st.columns([2] + [1] * len(st.session_state.selected_products))
            with cols[0]:
                st.markdown("**Especificação**")
            
            for i, product in enumerate(st.session_state.selected_products):
                with cols[i + 1]:
                    data = product_data[product]
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{data['icon']}</div>
                        <div style="font-weight: 600; font-size: 0.9rem;">{product}</div>
                        <div style="color: #666; font-size: 0.8rem;">{data['brand']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Preço (linha especial)
            cols = st.columns([2] + [1] * len(st.session_state.selected_products))
            with cols[0]:
                st.markdown("**Preço**")
            
            prices = [product_data[product]['price'] for product in st.session_state.selected_products]
            min_price = min(prices)
            max_price = max(prices)
            
            for i, product in enumerate(st.session_state.selected_products):
                with cols[i + 1]:
                    price = product_data[product]['price']
                    if price == min_price and len(st.session_state.selected_products) > 1:
                        st.markdown(f'<div class="best-price">R$ {price:,}</div>', unsafe_allow_html=True)
                    elif price == max_price and len(st.session_state.selected_products) > 1:
                        st.markdown(f'<div class="premium">R$ {price:,}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"**R$ {price:,}**")
            
            # Outras especificações
            for spec in sorted(all_specs):
                cols = st.columns([2] + [1] * len(st.session_state.selected_products))
                with cols[0]:
                    st.markdown(f"**{spec}**")
                
                # Para ano de lançamento, destacar o mais recente
                if spec == "Ano de Lançamento":
                    years = []
                    for product in st.session_state.selected_products:
                        specs = product_data[product]['specifications']
                        if spec in specs:
                            years.append(specs[spec])
                    
                    max_year = max(years) if years else 0
                    
                    for i, product in enumerate(st.session_state.selected_products):
                        with cols[i + 1]:
                            specs = product_data[product]['specifications']
                            if spec in specs:
                                value = specs[spec]
                                if value == max_year and len(st.session_state.selected_products) > 1:
                                    st.markdown(f'<div class="most-recent">{value}</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(f"{value}")
                            else:
                                st.markdown("-")
                else:
                    for i, product in enumerate(st.session_state.selected_products):
                        with cols[i + 1]:
                            specs = product_data[product]['specifications']
                            if spec in specs:
                                st.markdown(f"{specs[spec]}")
                            else:
                                st.markdown("-")
            
            # Histórico de preços usando gráficos nativos do Streamlit
            if len(st.session_state.selected_products) <= 2:
                st.markdown("### 📈 Histórico de Preços")
                
                chart_cols = st.columns(len(st.session_state.selected_products))
                
                for i, product in enumerate(st.session_state.selected_products):
                    with chart_cols[i]:
                        data = product_data[product]
                        chart_data, trend_text, trend_class = create_price_chart_data(product, data['price'])
                        
                        st.markdown(f"""
                        <div class="chart-title">{product}</div>
                        <div class="current-price">R$ {data['price']:,}</div>
                        <div class="price-trend {trend_class}">{trend_text}</div>
                        """, unsafe_allow_html=True)
                        
                        # Usar line_chart nativo do Streamlit
                        st.line_chart(chart_data.set_index('Data')['Preço'], height=200)
            
            # Gráfico de comparação de preços
            st.markdown("### 💰 Comparação de Preços")
            
            price_comparison = pd.DataFrame({
                'Produto': st.session_state.selected_products,
                'Preço (R$)': [product_data[product]['price'] for product in st.session_state.selected_products]
            })
            
            st.bar_chart(price_comparison.set_index('Produto')['Preço (R$)'])
            
            # Recomendações
            st.markdown("### 💡 Recomendações")
            
            # Melhor custo-benefício (mais recente com menor preço)
            best_value = None
            best_score = 0
            
            for product in st.session_state.selected_products:
                data = product_data[product]
                # Score baseado em ano/preço
                score = data['year'] / (data['price'] / 1000)
                if score > best_score:
                    best_score = score
                    best_value = product
            
            rec_cols = st.columns(3)
            
            with rec_cols[0]:
                if best_value:
                    st.markdown(f"""
                    <div class="recommendation-card rec-success">
                        <h4>🏆 Melhor Custo-Benefício</h4>
                        <h3>{best_value}</h3>
                        <p>R$ {product_data[best_value]['price']:,}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with rec_cols[1]:
                # Mais recente
                newest = max(st.session_state.selected_products, 
                           key=lambda x: product_data[x]['year'])
                st.markdown(f"""
                <div class="recommendation-card rec-info">
                    <h4>🆕 Mais Recente</h4>
                    <h3>{newest}</h3>
                    <p>{product_data[newest]['year']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with rec_cols[2]:
                # Mais barato
                cheapest = min(st.session_state.selected_products, 
                             key=lambda x: product_data[x]['price'])
                st.markdown(f"""
                <div class="recommendation-card rec-warning">
                    <h4>💰 Mais Econômico</h4>
                    <h3>{cheapest}</h3>
                    <p>R$ {product_data[cheapest]['price']:,}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Análise adicional
            if len(st.session_state.selected_products) > 1:
                st.markdown("### 📊 Análise Comparativa")
                
                # Criar métricas comparativas
                avg_price = sum(prices) / len(prices)
                price_range = max_price - min_price
                
                metric_cols = st.columns(3)
                
                with metric_cols[0]:
                    st.metric("Preço Médio", f"R$ {avg_price:,.0f}")
                
                with metric_cols[1]:
                    st.metric("Diferença de Preço", f"R$ {price_range:,.0f}")
                
                with metric_cols[2]:
                    newest_year = max([product_data[p]['year'] for p in st.session_state.selected_products])
                    st.metric("Ano Mais Recente", f"{newest_year}")

if __name__ == "__main__":
    main()
