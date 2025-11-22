document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('dasStatusChart');
    let dasChart; // Variável para guardar a instância do gráfico

    // Dados iniciais (exemplo)
    let chartData = {
        pago: 9,
        pendente: 21,
        vencido: 4
    };

    // Cores correspondentes às classes CSS dos badges
    const chartColors = {
        pago: '#8BA883',      // Cor da classe .status-pago
        pendente: '#F7D358',  // Cor da classe .status-pendente
        vencido: '#BB8B7E'    // Cor da classe .status-vencido
    };

    /**
     * Função para criar ou atualizar o gráfico de rosca
     */
    function renderChart() {
        const dataValues = [chartData.pago, chartData.pendente, chartData.vencido];
        const backgroundColors = [chartColors.pago, chartColors.pendente, chartColors.vencido];

        // Atualiza os contadores na legenda HTML
        document.getElementById('count-pago').textContent = chartData.pago;
        document.getElementById('count-pendente').textContent = chartData.pendente;
        document.getElementById('count-vencido').textContent = chartData.vencido;

        if (ctx) {
             if (dasChart) {
                // Se o gráfico já existe, atualiza os dados
                dasChart.data.datasets[0].data = dataValues;
                dasChart.data.datasets[0].backgroundColor = backgroundColors;
                dasChart.update();
            } else {
                 // Se não existe, cria o gráfico
                 dasChart = new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Em dia', 'Pendente', 'Vencido'],
                        datasets: [{
                            label: 'Status DAS',
                            data: dataValues,
                            backgroundColor: backgroundColors,
                            borderColor: '#fff', // Borda branca entre as fatias
                            borderWidth: 2,
                            hoverOffset: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: '70%', // Controla o tamanho do "buraco" no meio
                        plugins: {
                            legend: {
                                display: false // Esconde a legenda padrão do Chart.js
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        let label = context.label || '';
                                        if (label) {
                                            label += ': ';
                                        }
                                        if (context.parsed !== null) {
                                            label += context.parsed;
                                        }
                                        return label;
                                    }
                                }
                            }
                        }
                    }
                });
            }
        } else {
            console.error("Elemento canvas 'dasStatusChart' não encontrado.");
        }
    }

    /**
     * Função para recalcular os dados do gráfico (SIMULAÇÃO)
     * No projeto real, esta função leria os badges de outras páginas
     * ou faria uma chamada API para obter os totais atualizados.
     */
    function updateChartData() {
        // --- INÍCIO DA SIMULAÇÃO ---
        // Simula a contagem de badges em outras páginas (exemplo)
        // No seu projeto real, você precisaria buscar esses dados
        
        // Exemplo: Imagine que pegamos todos os badges de pagamento da aplicação
        const allPaymentBadges = document.querySelectorAll('.status-badge-pagamento'); // Seleciona badges DE OUTRAS PÁGINAS (se carregadas) OU DADOS DO BACKEND

         // Resetamos a contagem
         chartData = { pago: 0, pendente: 0, vencido: 0 };

        // Simulamos a contagem baseada no texto (idealmente seria pela classe)
        // Isso é apenas um EXEMPLO, a lógica real dependerá de como você busca os dados
        if (allPaymentBadges.length > 0) { // Se encontrasse badges em outras páginas
            allPaymentBadges.forEach(badge => {
                 const status = badge.textContent.trim().toLowerCase();
                 if (status === 'pago' || status === 'finalizado') { // Assumindo que 'Finalizado' = 'Pago'
                     chartData.pago++;
                 } else if (status === 'pendente') {
                     chartData.pendente++;
                 } else if (status === 'vencido') {
                     chartData.vencido++;
                 }
            });
        } else {
            // Se não encontrar badges (ex: só o dashboard está aberto),
            // usa os dados iniciais ou busca do backend
             chartData = { pago: 9, pendente: 21, vencido: 4 }; // Mantém dados de exemplo
             console.warn("Nenhum badge de pagamento encontrado para contagem dinâmica. Usando dados estáticos.");
        }
        
        // --- FIM DA SIMULAÇÃO ---

        // Re-renderiza o gráfico com os novos dados
        renderChart();
    }

    // --- INICIALIZAÇÃO E EVENTOS ---

    // Renderiza o gráfico inicial quando a página carrega
    renderChart();

    // ADICIONA EVENT LISTENERS AOS BADGES (SE EXISTIREM NA PÁGINA ATUAL)
    // Se você tiver badges nesta página que devam atualizar o gráfico ao clicar:
    const badgesNestaPagina = document.querySelectorAll('.status-badge-pagamento'); // Adapte o seletor se necessário
    
    if (badgesNestaPagina.length > 0) {
        badgesNestaPagina.forEach(badge => {
            badge.addEventListener('click', function() {
                // Lógica para mudar o estado do badge clicado (do dashboard-gestao.js)
                const currentState = this.textContent.trim();
                this.classList.remove('status-pago', 'status-pendente', 'status-vencido');

                let newStateClass = '';
                if (currentState === 'Pago' || currentState === 'Finalizado') {
                    this.textContent = 'Pendente';
                    newStateClass = 'status-pendente';
                } else if (currentState === 'Pendente') {
                    this.textContent = 'Vencido';
                     newStateClass = 'status-vencido';
                } else { // Era Vencido
                    this.textContent = 'Pago';
                     newStateClass = 'status-pago';
                }
                 this.classList.add(newStateClass);

                // DEPOIS de mudar o estado do badge, ATUALIZA O GRÁFICO
                // A função updateChartData() precisa recontar TODOS os badges relevantes
                updateChartData(); 
            });
        });
    }

    // Opcional: Adicionar um listener para eventos personalizados
    // Se outras páginas dispararem um evento quando um badge mudar,
    // o dashboard pode "ouvir" e atualizar o gráfico.
    // Exemplo: document.addEventListener('statusBadgeChanged', updateChartData);

});
