// Espera o DOM carregar antes de executar
document.addEventListener("DOMContentLoaded", function() {

    // Lista de componentes para a ÁREA DO CLIENTE
    const components = [
        ["header-placeholder", "_header.html"],         // Cabeçalho padrão com botão 'sidebarToggle'
        ["sidebar-placeholder", "_sidebar.html"]          // Sidebar padrão com id 'sidebar'
    ];

    // Função para carregar um único componente (sem alterações)
    const loadHTML = (url, elementId) => {
        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    if (response.status === 404) {
                         console.warn(`Arquivo ${url} não encontrado para o placeholder ${elementId}.`);
                         return null;
                    }
                    throw new Error(`Não foi possível carregar ${url}: ${response.statusText}`);
                }
                return response.text();
            })
            .then(data => {
                const element = document.getElementById(elementId);
                if (element && data !== null) {
                    element.innerHTML = data;
                } else if (!element) {
                    // console.warn(`Placeholder com ID '${elementId}' não encontrado.`);
                }
            });
    };

    // Carrega os componentes definidos acima
    Promise.all(
        components.map(comp => loadHTML(comp[1], comp[0]))
    ).then(() => {
        // ---- COMPONENTES DA ÁREA DO CLIENTE CARREGADOS ----
        
        // Inicializa APENAS a sidebar padrão (ID: 'sidebar', Botão: 'sidebarToggle')
        initializeSidebarToggle('sidebarToggle', 'sidebar');

        // Define o link ativo APENAS na sidebar padrão
        setActiveNavLink('.sidebar'); 

    }).catch(error => {
        console.error("Erro ao carregar um ou mais componentes:", error);
    });

});


/**
 * Inicializa a lógica de abrir/fechar de um menu lateral específico.
 */
function initializeSidebarToggle(toggleButtonId, sidebarId) {
    const sidebarToggle = document.getElementById(toggleButtonId);
    const sidebar = document.getElementById(sidebarId);

    if (sidebarToggle && sidebar) { 
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
        });
    } else {
        // console.warn(`Botão '${toggleButtonId}' ou Sidebar '${sidebarId}' não encontrado nesta página.`);
    }
}

/**
 * Adiciona a classe 'active' ao link de navegação correto dentro de uma sidebar específica.
 */
function setActiveNavLink(sidebarSelector) {
    const currentPage = window.location.pathname.split("/").pop();

    if (currentPage && sidebarSelector) {
        const sidebarElement = document.querySelector(sidebarSelector);
        if (sidebarElement) {
            const navLink = sidebarElement.querySelector(`.nav-link[href="${currentPage}"]`);
            if (navLink) {
                navLink.classList.add('active');
            }
        }
    }
}

