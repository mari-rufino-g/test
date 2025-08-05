import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Configuração da página
st.set_page_config(
    page_title="Comparador de Agentes LLM",
    page_icon="🤖",
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

.best-performance {
    background: #d1ecf1;
    color: #0c5460;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-weight: 600;
}

.worst-performance {
    background: #f8d7da;
    color: #721c24;
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

# Base de dados dos agentes LLM
@st.cache_data
def load_agent_data():
    return {
        'Agente Alpha': {
            'provider': 'TechCorp',
            'category': 'Atendimento',
            'cost': 2500,
            'deployment_year': 2024,
            'deployment_date': '2024-01-15',
            'specifications': {
                'Ano de Implantação': 2024,
                'Quantidade de Atendimentos': '15,000/mês',
                'Custo Total': 'R$ 2,500/mês',
                'Total de Erros': '45/mês',
                'Total de Bugs': '8/mês',
                'Tempo Médio de Atendimento': '2.3 min'
            },
            'icon': '🤖'
        },
        'Agente Beta': {
            'provider': 'AIFlow',
            'category': 'Suporte',
            'cost': 3200,
            'deployment_year': 2023,
            'deployment_date': '2023-11-20',
            'specifications': {
                'Ano de Implantação': 2023,
                'Quantidade de Atendimentos': '22,000/mês',
                'Custo Total': 'R$ 3,200/mês',
                'Total de Erros': '38/mês',
                'Total de Bugs': '12/mês',
                'Tempo Médio de Atendimento': '1.8 min'
            },
            'icon': '🤖'
        },
        'Agente Gamma': {
            'provider': 'SmartBot',
            'category': 'Vendas',
            'cost': 4100,
            'deployment_year': 2024,
            'deployment_date': '2024-03-10',
            'specifications': {
                'Ano de Implantação': 2024,
                'Quantidade de Atendimentos': '28,500/mês',
                'Custo Total': 'R$ 4,100/mês',
                'Total de Erros': '52/mês',
                'Total de Bugs': '6/mês',
                'Tempo Médio de Atendimento': '3.1 min'
            },
            'icon': '🤖'
        },
        'Agente Delta': {
            'provider': 'NeuralSys',
            'category': 'Atendimento',
            'cost': 1850,
            'deployment_year': 2023,
            'deployment_date': '2023-08-05',
            'specifications': {
                'Ano de Implantação': 2023,
                'Quantidade de Atendimentos': '12,800/mês',
                'Custo Total': 'R$ 1,850/mês',
                'Total de Erros': '63/mês',
                'Total de Bugs': '15/mês',
                'Tempo Médio de Atendimento': '4.2 min'
            },
            'icon': '🤖'
        },
        'Agente Epsilon': {
            'provider': 'CogniBot',
            'category': 'Suporte',
            'cost': 2900,
            'deployment_year': 2024,
            'deployment_date': '2024-02-28',
            'specifications': {
                'Ano de Implantação': 2024,
                'Quantidade de Atendimentos': '19,200/mês',
                'Custo Total': 'R$ 2,900/mês',
                'Total de Erros': '41/mês',
                'Total de Bugs': '9/mês',
                'Tempo Médio de Atendimento': '2.7 min'
            },
            'icon': '🤖'
        },
        'Agente Zeta': {
            'provider': 'AutoChat',
            'category': 'Vendas',
            'cost': 3750,
            'deployment_year': 2023,
            'deployment_date': '2023-12-12',
            'specifications': {
                'Ano de Implantação': 2023,
                'Quantidade de Atendimentos': '25,600/mês',
                'Custo Total': 'R$ 3,750/mês',
                'Total de Erros': '35/mês',
                'Total de Bugs': '7/mês',
                'Tempo Médio de Atendimento': '2.1 min'
            },
            'icon': '🤖'
        }
    }

def generate_cost_history(current_cost, months=6):
    """Gera histórico de custos simulado"""
    dates = []
    costs = []
    
    start_date = datetime.now() - timedelta(days=months*30)
    
    # Começar com um custo um pouco diferente
    base_cost = current_cost * 1.05
    
    for i in range(months * 4):  # 4 pontos por mês
        date = start_date + timedelta(days=i*7)  # A cada semana
        
        # Simular flutuação de custos
        variation = random.uniform(-0.05, 0.08)  # Variação nos custos
        base_cost = base_cost * (1 + variation)
        
        # Garantir que não fique muito diferente do custo atual
        if base_cost < current_cost * 0.7:
            base_cost = current_cost * random.uniform(0.85, 1.15)
        elif base_cost > current_cost * 1.3:
            base_cost = current_cost * random.uniform(0.85, 1.15)
            
        dates.append(date.strftime('%d/%m'))
        costs.append(max(base_cost, current_cost * 0.5))
    
    # Garantir que o último custo seja próximo ao atual
    costs[-1] = current_cost
    
    return dates, costs

def create_cost_chart_data(agent_name, current_cost):
    """Cria dados para gráfico de histórico de custos usando Streamlit nativo"""
    dates, costs = generate_cost_history(current_cost)
    
    # Calcular tendência
    cost_change = (costs[-1] - costs[0]) / costs[0] * 100
    trend_text = f"↓ R$ {abs(costs[0] - costs[-1]):.0f}" if cost_change < 0 else f"↑ R$ {abs(costs[-1] - costs[0]):.0f}"
    trend_class = "price-down" if cost_change < 0 else "price-up"
    
    # Criar DataFrame para o gráfico
    chart_data = pd.DataFrame({
        'Data': dates,
        'Custo': costs
    })
    
    return chart_data, trend_text, trend_class

def main():
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Comparador de Agentes LLM</h1>
        <p class="header-subtitle">Compare agentes de IA e suas métricas de performance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    agent_data = load_agent_data()
    
    # Inicializar session state
    if 'selected_agents' not in st.session_state:
        st.session_state.selected_agents = []
    
    # Layout principal
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Seção de seleção de agentes
        st.markdown("""
        <div class="sidebar-header">
            <h3>Agentes Selecionados</h3>
            <p>Até 4 agentes selecionados</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar agentes selecionados
        if st.session_state.selected_agents:
            for agent in st.session_state.selected_agents:
                data = agent_data[agent]
                
                st.markdown(f"""
                <div style="display: flex; align-items: center; padding: 0.5rem; background: #f8f9fa; border-radius: 6px; margin-bottom: 0.5rem;">
                    <span style="margin-right: 0.5rem;">{data['icon']}</span>
                    <span style="flex: 1; font-weight: 500;">{agent}</span>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🗑️ Limpar", key="clear_all", help="Remove todos os agentes"):
                st.session_state.selected_agents = []
                st.rerun()
        else:
            st.info("Nenhum agente selecionado")
        
        st.markdown("---")
        
        # Seção de seleção de agentes
        st.markdown("""
        <h4>Selecionar Agentes</h4>
        <p>Escolha até 4 agentes para comparar</p>
        """, unsafe_allow_html=True)
        
        # Filtros
        categories = ['Todos'] + list(set([data['category'] for data in agent_data.values()]))
        selected_category = st.selectbox("Categoria", categories)
        
        providers = ['Todos'] + list(set([data['provider'] for data in agent_data.values()]))
        selected_provider = st.selectbox("Provedor", providers)
        
        # Filtrar agentes
        filtered_agents = {}
        for name, data in agent_data.items():
            if selected_category != 'Todos' and data['category'] != selected_category:
                continue
            if selected_provider != 'Todos' and data['provider'] != selected_provider:
                continue
            filtered_agents[name] = data
        
        # Exibir agentes disponíveis
        for agent_name, data in filtered_agents.items():
            is_selected = agent_name in st.session_state.selected_agents
            can_add = len(st.session_state.selected_agents) < 4
            
            st.markdown(f"""
            <div class="product-card">
                <div class="product-image">{data['icon']}</div>
                <div class="product-name">{agent_name}</div>
                <div class="product-price">R$ {data['cost']:,}/mês</div>
                <div class="product-year">{data['provider']} - {data['deployment_year']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if is_selected:
                if st.button("❌ Remover da Comparação", key=f"remove_{agent_name}"):
                    st.session_state.selected_agents.remove(agent_name)
                    st.rerun()
            else:
                if can_add:
                    if st.button("➕ Adicionar à Comparação", key=f"add_{agent_name}"):
                        st.session_state.selected_agents.append(agent_name)
                        st.rerun()
                else:
                    st.button("Limite atingido (4 agentes)", disabled=True, key=f"disabled_{agent_name}")
    
    with col2:
        if not st.session_state.selected_agents:
            st.markdown("""
            <div style="text-align: center; padding: 4rem 2rem; color: #666;">
                <h3>👈 Selecione agentes para comparar</h3>
                <p>Escolha até 4 agentes na barra lateral para ver a comparação detalhada</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Header da comparação
            st.markdown("""
            <div class="comparison-header">
                <h2 class="comparison-title">Comparação de Agentes LLM</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Tabela de especificações
            st.markdown("### 📊 Métricas de Performance")
            
            # Criar tabela de comparação
            all_specs = set()
            for agent in st.session_state.selected_agents:
                all_specs.update(agent_data[agent]['specifications'].keys())
            
            # Cabeçalho da tabela
            cols = st.columns([2] + [1] * len(st.session_state.selected_agents))
            with cols[0]:
                st.markdown("**Métrica**")
            
            for i, agent in enumerate(st.session_state.selected_agents):
                with cols[i + 1]:
                    data = agent_data[agent]
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{data['icon']}</div>
                        <div style="font-weight: 600; font-size: 0.9rem;">{agent}</div>
                        <div style="color: #666; font-size: 0.8rem;">{data['provider']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Custo (linha especial)
            cols = st.columns([2] + [1] * len(st.session_state.selected_agents))
            with cols[0]:
                st.markdown("**Custo Mensal**")
            
            costs = [agent_data[agent]['cost'] for agent in st.session_state.selected_agents]
            min_cost = min(costs)
            max_cost = max(costs)
            
            for i, agent in enumerate(st.session_state.selected_agents):
                with cols[i + 1]:
                    cost = agent_data[agent]['cost']
                    if cost == min_cost and len(st.session_state.selected_agents) > 1:
                        st.markdown(f'<div class="best-price">R$ {cost:,}/mês</div>', unsafe_allow_html=True)
                    elif cost == max_cost and len(st.session_state.selected_agents) > 1:
                        st.markdown(f'<div class="premium">R$ {cost:,}/mês</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f"**R$ {cost:,}/mês**")
            
            # Outras especificações com destaque para melhores/piores valores
            for spec in sorted(all_specs):
                cols = st.columns([2] + [1] * len(st.session_state.selected_agents))
                with cols[0]:
                    st.markdown(f"**{spec}**")
                
                # Para ano de implantação, destacar o mais recente
                if spec == "Ano de Implantação":
                    years = []
                    for agent in st.session_state.selected_agents:
                        specs = agent_data[agent]['specifications']
                        if spec in specs:
                            years.append(specs[spec])
                    
                    max_year = max(years) if years else 0
                    
                    for i, agent in enumerate(st.session_state.selected_agents):
                        with cols[i + 1]:
                            specs = agent_data[agent]['specifications']
                            if spec in specs:
                                value = specs[spec]
                                if value == max_year and len(st.session_state.selected_agents) > 1:
                                    st.markdown(f'<div class="most-recent">{value}</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(f"{value}")
                            else:
                                st.markdown("-")
                
                # Para erros e bugs, destacar menor valor (melhor performance)
                elif "Erros" in spec or "Bugs" in spec:
                    values = []
                    for agent in st.session_state.selected_agents:
                        specs = agent_data[agent]['specifications']
                        if spec in specs:
                            # Extrair número da string "45/mês"
                            num_value = int(specs[spec].split('/')[0])
                            values.append(num_value)
                    
                    if values:
                        min_value = min(values)
                        max_value = max(values)
                        
                        for i, agent in enumerate(st.session_state.selected_agents):
                            with cols[i + 1]:
                                specs = agent_data[agent]['specifications']
                                if spec in specs:
                                    value = specs[spec]
                                    num_value = int(value.split('/')[0])
                                    if num_value == min_value and len(st.session_state.selected_agents) > 1:
                                        st.markdown(f'<div class="best-performance">{value}</div>', unsafe_allow_html=True)
                                    elif num_value == max_value and len(st.session_state.selected_agents) > 1:
                                        st.markdown(f'<div class="worst-performance">{value}</div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"{value}")
                                else:
                                    st.markdown("-")
                
                # Para tempo de atendimento, destacar menor valor (melhor performance)
                elif "Tempo Médio" in spec:
                    values = []
                    for agent in st.session_state.selected_agents:
                        specs = agent_data[agent]['specifications']
                        if spec in specs:
                            # Extrair número da string "2.3 min"
                            num_value = float(specs[spec].split(' ')[0])
                            values.append(num_value)
                    
                    if values:
                        min_value = min(values)
                        max_value = max(values)
                        
                        for i, agent in enumerate(st.session_state.selected_agents):
                            with cols[i + 1]:
                                specs = agent_data[agent]['specifications']
                                if spec in specs:
                                    value = specs[spec]
                                    num_value = float(value.split(' ')[0])
                                    if num_value == min_value and len(st.session_state.selected_agents) > 1:
                                        st.markdown(f'<div class="best-performance">{value}</div>', unsafe_allow_html=True)
                                    elif num_value == max_value and len(st.session_state.selected_agents) > 1:
                                        st.markdown(f'<div class="worst-performance">{value}</div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"{value}")
                                else:
                                    st.markdown("-")
                
                # Para quantidade de atendimentos, destacar maior valor (melhor performance)
                elif "Quantidade de Atendimentos" in spec:
                    values = []
                    for agent in st.session_state.selected_agents:
                        specs = agent_data[agent]['specifications']
                        if spec in specs:
                            # Extrair número da string "15,000/mês"
                            num_value = int(specs[spec].replace(',', '').split('/')[0])
                            values.append(num_value)
                    
                    if values:
                        min_value = min(values)
                        max_value = max(values)
                        
                        for i, agent in enumerate(st.session_state.selected_agents):
                            with cols[i + 1]:
                                specs = agent_data[agent]['specifications']
                                if spec in specs:
                                    value = specs[spec]
                                    num_value = int(value.replace(',', '').split('/')[0])
                                    if num_value == max_value and len(st.session_state.selected_agents) > 1:
                                        st.markdown(f'<div class="best-performance">{value}</div>', unsafe_allow_html=True)
                                    elif num_value == min_value and len(st.session_state.selected_agents) > 1:
                                        st.markdown(f'<div class="worst-performance">{value}</div>', unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"{value}")
                                else:
                                    st.markdown("-")
                
                else:
                    for i, agent in enumerate(st.session_state.selected_agents):
                        with cols[i + 1]:
                            specs = agent_data[agent]['specifications']
                            if spec in specs:
                                st.markdown(f"{specs[spec]}")
                            else:
                                st.markdown("-")
            
            # Histórico de custos usando gráficos nativos do Streamlit
            if len(st.session_state.selected_agents) <= 2:
                st.markdown("### 📈 Histórico de Custos")
                
                chart_cols = st.columns(len(st.session_state.selected_agents))
                
                for i, agent in enumerate(st.session_state.selected_agents):
                    with chart_cols[i]:
                        data = agent_data[agent]
                        chart_data, trend_text, trend_class = create_cost_chart_data(agent, data['cost'])
                        
                        st.markdown(f"""
                        <div class="chart-title">{agent}</div>
                        <div class="current-price">R$ {data['cost']:,}/mês</div>
                        <div class="price-trend {trend_class}">{trend_text}</div>
                        """, unsafe_allow_html=True)
                        
                        # Usar line_chart nativo do Streamlit
                        st.line_chart(chart_data.set_index('Data')['Custo'], height=200)
            
            # Gráfico de comparação de custos
            st.markdown("### 💰 Comparação de Custos")
            
            cost_comparison = pd.DataFrame({
                'Agente': st.session_state.selected_agents,
                'Custo Mensal (R$)': [agent_data[agent]['cost'] for agent in st.session_state.selected_agents]
            })
            
            st.bar_chart(cost_comparison.set_index('Agente')['Custo Mensal (R$)'])
            
            # Recomendações
            st.markdown("### 💡 Recomendações")
            
            # Melhor custo-benefício (baseado em atendimentos/custo)
            best_value = None
            best_score = 0
            
            for agent in st.session_state.selected_agents:
                data = agent_data[agent]
                # Extrair número de atendimentos
                atendimentos = int(data['specifications']['Quantidade de Atendimentos'].replace(',', '').split('/')[0])
                # Score baseado em atendimentos/custo
                score = atendimentos / data['cost']
                if score > best_score:
                    best_score = score
                    best_value = agent
            
            rec_cols = st.columns(3)
            
            with rec_cols[0]:
                if best_value:
                    st.markdown(f"""
                    <div class="recommendation-card rec-success">
                        <h4>🏆 Melhor Custo-Benefício</h4>
                        <h3>{best_value}</h3>
                        <p>R$ {agent_data[best_value]['cost']:,}/mês</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with rec_cols[1]:
                # Mais recente
                newest = max(st.session_state.selected_agents, 
                           key=lambda x: agent_data[x]['deployment_year'])
                st.markdown(f"""
                <div class="recommendation-card rec-info">
                    <h4>🆕 Mais Recente</h4>
                    <h3>{newest}</h3>
                    <p>{agent_data[newest]['deployment_year']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with rec_cols[2]:
                # Mais econômico
                cheapest = min(st.session_state.selected_agents, 
                             key=lambda x: agent_data[x]['cost'])
                st.markdown(f"""
                <div class="recommendation-card rec-warning">
                    <h4>💰 Mais Econômico</h4>
                    <h3>{cheapest}</h3>
                    <p>R$ {agent_data[cheapest]['cost']:,}/mês</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Análise adicional
            if len(st.session_state.selected_agents) > 1:
                st.markdown("### 📊 Análise Comparativa")
                
                # Criar métricas comparativas
                avg_cost = sum(costs) / len(costs)
                cost_range = max_cost - min_cost
                
                # Calcular total de atendimentos
                total_atendimentos = 0
                for agent in st.session_state.selected_agents:
                    atendimentos_str = agent_data[agent]['specifications']['Quantidade de Atendimentos']
                    atendimentos = int(atendimentos_str.replace(',', '').split('/')[0])
                    total_atendimentos += atendimentos
                
                # Calcular média de erros
                total_erros = 0
                for agent in st.session_state.selected_agents:
                    erros_str = agent_data[agent]['specifications']['Total de Erros']
                    erros = int(erros_str.split('/')[0])
                    total_erros += erros
                avg_erros = total_erros / len(st.session_state.selected_agents)
                
                metric_cols = st.columns(4)
                
                with metric_cols[0]:
                    st.metric("Custo Médio", f"R$ {avg_cost:,.0f}/mês")
                
                with metric_cols[1]:
                    st.metric("Diferença de Custo", f"R$ {cost_range:,.0f}/mês")
                
                with metric_cols[2]:
                    st.metric("Total Atendimentos", f"{total_atendimentos:,}/mês")
                
                with metric_cols[3]:
                    st.metric("Média de Erros", f"{avg_erros:.0f}/mês")
                
                # Performance Score
                st.markdown("### 🎯 Score de Performance")
                
                performance_data = []
                for agent in st.session_state.selected_agents:
                    data = agent_data[agent]
                    specs = data['specifications']
                    
                    # Extrair métricas
                    atendimentos = int(specs['Quantidade de Atendimentos'].replace(',', '').split('/')[0])
                    erros = int(specs['Total de Erros'].split('/')[0])
                    bugs = int(specs['Total de Bugs'].split('/')[0])
                    tempo = float(specs['Tempo Médio de Atendimento'].split(' ')[0])
                    
                    # Calcular score (maior é melhor)
                    # Fórmula: (atendimentos * 100) / (custo + erros*10 + bugs*15 + tempo*100)
                    score = (atendimentos * 100) / (data['cost'] + erros*10 + bugs*15 + tempo*100)
                    
                    performance_data.append({
                        'Agente': agent,
                        'Score': score,
                        'Atendimentos': atendimentos,
                        'Custo': data['cost'],
                        'Erros': erros,
                        'Bugs': bugs,
                        'Tempo (min)': tempo
                    })
                
                # Ordenar por score
                performance_data.sort(key=lambda x: x['Score'], reverse=True)
                
                # Mostrar ranking
                for i, perf in enumerate(performance_data):
                    color = "#d4edda" if i == 0 else "#f8f9fa"
                    border_color = "#c3e6cb" if i == 0 else "#dee2e6"
                    icon = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🔹"
                    
                    st.markdown(f"""
                    <div style="background: {color}; border: 1px solid {border_color}; padding: 1rem; margin: 0.5rem 0; border-radius: 8px;">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <div style="display: flex; align-items: center;">
                                <span style="font-size: 1.2rem; margin-right: 0.5rem;">{icon}</span>
                                <strong>{perf['Agente']}</strong>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 1.1rem; font-weight: 600; color: #007bff;">
                                    Score: {perf['Score']:.2f}
                                </div>
                                <div style="font-size: 0.9rem; color: #666;">
                                    {perf['Atendimentos']:,} atend. | R$ {perf['Custo']:,} | {perf['Erros']} erros
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
