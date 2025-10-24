// Aguarda o DOM carregar completamente antes de adicionar os eventos
document.addEventListener('DOMContentLoaded', function () {

    // 1. LÓGICA PARA OS BADGES DE STATUS DE 3 ESTADOS (Pago/Pendente/Vencido)
    // Seleciona TODOS os badges de 3 estados (ex: pela classe .status-badge-pagamento)
    const badgesPagamento = document.querySelectorAll('.status-badge-pagamento'); // Use uma classe específica!

    badgesPagamento.forEach(badge => {
        badge.addEventListener('click', function () {
            const currentState = this.textContent.trim();
            this.classList.remove('status-pago', 'status-pendente', 'status-vencido');

            if (currentState === 'Pago') {
                this.textContent = 'Pendente';
                this.classList.add('status-pendente');
            } else if (currentState === 'Pendente') {
                this.textContent = 'Vencido';
                this.classList.add('status-vencido');
            } else {
                this.textContent = 'Pago';
                this.classList.add('status-pago');
            }
        });
    });

    // 2. LÓGICA PARA OS BADGES DE STATUS DE 2 ESTADOS (Adimplente/Inadimplente)
    // Seleciona TODOS os badges de 2 estados (ex: pela classe .status-badge-cliente)
    const badgesCliente = document.querySelectorAll('.status-badge-cliente'); // Use outra classe específica!

    badgesCliente.forEach(badge => {
        badge.addEventListener('click', function () {
            const isAdimplente = this.textContent === 'Adimplente';

            if (isAdimplente) {
                this.textContent = 'Inadimplente';
                this.classList.remove('status-adimplente');
                this.classList.add('status-inadimplente');
            } else {
                this.textContent = 'Adimplente';
                this.classList.remove('status-inadimplente');
                this.classList.add('status-adimplente');
            }
        });
    });

    // 3. ADICIONE OUTRAS LÓGICAS DESTA PÁGINA AQUI...
    // Por exemplo, a lógica para o filtro ou para a busca.

});