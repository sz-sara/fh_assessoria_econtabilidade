document.addEventListener('DOMContentLoaded', function () {
    const monthlyCtx = document.getElementById('monthlyDasChart');
    const yearlyCtx = document.getElementById('yearlyDasChart');

    // Cores (devem corresponder às classes CSS .status-*)
    const colorPago = '#8BA883';
    const colorPendente = '#F7D358';
    const colorVencido = '#BB8B7E';

    // --- Gráfico de Barras Mensal ---
    if (monthlyCtx) {
        new Chart(monthlyCtx, {
            type: 'bar',
            data: {
                labels: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'], // Meses
                datasets: [{
                    label: 'Status DAS Mensal',
                    data: [1, 1, 1, 1, 1, 1, 1, 3, 2, 2, 2, 2], // 1:Pago, 2:Pendente, 3:Vencido (Exemplo)
                    backgroundColor: (context) => {
                        // Define a cor de cada barra baseado no valor (exemplo)
                        const value = context.raw;
                        if (value === 3) return colorVencido;
                        if (value === 2) return colorPendente;
                        return colorPago; // Padrão é pago
                    },
                    borderWidth: 0,
                    borderRadius: 4, // Barras levemente arredondadas
                    barPercentage: 0.6, // Largura das barras
                    categoryPercentage: 0.7 // Espaçamento entre grupos de barras (meses)
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        display: false, // Esconde o eixo Y
                        max: 3.5 // Um pouco acima do valor máximo para dar espaço
                    },
                    x: {
                        grid: {
                            display: false // Esconde as linhas de grade verticais
                        },
                        ticks: {
                             font: {
                                size: 10 // Tamanho menor para os meses
                             }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false // Esconde a legenda padrão
                    },
                    tooltip: {
                         enabled: false // Desabilita tooltips neste gráfico simples
                    }
                }
            }
        });
    } else {
         console.error("Elemento canvas 'monthlyDasChart' não encontrado.");
    }

    // --- Gráfico de Rosca Anual ---
    if (yearlyCtx) {
        // Dados de exemplo
        const pagoPercent = 40;
        const pendentePercent = 32;
        const vencidoPercent = 28;

        // Atualiza os percentuais na legenda HTML
        document.getElementById('percent-pago').textContent = pagoPercent;
        document.getElementById('percent-pendente').textContent = pendentePercent;
        document.getElementById('percent-vencido').textContent = vencidoPercent;


        new Chart(yearlyCtx, {
            type: 'doughnut',
            data: {
                labels: ['Pago', 'Pendente', 'Vencido'],
                datasets: [{
                    label: 'Status DAS Anual (%)',
                    data: [pagoPercent, pendentePercent, vencidoPercent],
                    backgroundColor: [
                        colorPago,
                        colorPendente,
                        colorVencido
                    ],
                    borderColor: '#fff',
                    borderWidth: 3, // Borda branca maior
                    hoverOffset: 6 // Efeito de destaque maior ao passar o mouse
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%', // Buraco central maior
                plugins: {
                    legend: {
                        display: false // Esconde a legenda padrão
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed !== null) {
                                    label += context.parsed + '%'; // Adiciona % ao tooltip
                                }
                                return label;
                            }
                        }
                    }
                }
            }
        });
    } else {
        console.error("Elemento canvas 'yearlyDasChart' não encontrado.");
    }

});
