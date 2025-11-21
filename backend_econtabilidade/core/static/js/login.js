// Arquivo: js/login.js

document.getElementById('loginForm').addEventListener('submit', function(event) {
    // 1. Previne o envio padrão do formulário (evita o recarregamento da página)
    event.preventDefault();

    // 2. Obtém o valor do e-mail digitado
    const email = document.getElementById('email').value.trim();
    // Você pode ignorar a senha na simulação por enquanto

    let destino = '';

    // --- LÓGICA DE SIMULAÇÃO DE PERMISSÃO ---
    // Simula o login do Contador (Usuário Master)
    // Use um e-mail específico para acesso Master
    if (email === 'fabio@contabilidade.com') { 
        destino = 'dashboard_cont.html';
    } 
    // Simula o login do Cliente
    // Qualquer outro e-mail com '@' será tratado como Cliente
    else if (email.includes('@')) { 
        destino = 'dashboard_cliente.html';
    } 
    // Caso contrário, mostra um erro
    else {
        alert('E-mail inválido. Por favor, insira um endereço correto para login.');
        return; // Sai da função
    }

    // 3. Redireciona a página para o Dashboard correto
    window.location.href = destino;
});