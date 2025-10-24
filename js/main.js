// Espera o DOM carregar antes de executar
document.addEventListener("DOMContentLoaded", function() {

    // Lista de componentes para carregar [ID_do_placeholder, arquivo_html]
    const components = [
        ["header-placeholder", "_header.html"], // Assumindo que o _header tem o botão 'sidebarToggle'
        // ["header-cliente-placeholder", "_header_cliente.html"], // Se o cliente tiver um header diferente com 'sidebarContadorToggle'
        ["sidebar-placeholder", "_sidebar.html"],
        ["sidebar-contador-placeholder", "_sidebar_cont.html"] // Carrega a nova sidebar (Verifique se o nome do arquivo está correto)
    ];

    // Função para carregar um único componente (sem alterações)
    const loadHTML = (url, elementId) => {
        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    // Se o arquivo não for encontrado, não lança um erro, apenas avisa
                    // Isso permite que páginas que só usam um tipo de sidebar funcionem
                    if (response.status === 404) {
                         console.warn(`Arquivo ${url} não encontrado para o placeholder ${elementId}.`);
                         return null; // Retorna null para indicar que não carregou
                    }
                    throw new Error(`Não foi possível carregar ${url}: ${response.statusText}`);
                }
                return response.text();
            })
            .then(data => {
                const element = document.getElementById(elementId);
                if (element && data !== null) { // Verifica se data não é null
                    element.innerHTML = data;
                } else if (!element) {
                    // Não mostra aviso se o placeholder não existir,
                    // pois nem toda página terá todos os placeholders.
                    // console.warn(`Placeholder com ID '${elementId}' não encontrado.`);
                }
            });
    };

    // Carrega todos os componentes em paralelo
    Promise.all(
        components.map(comp => loadHTML(comp[1], comp[0]))
    ).then(() => {
        // ---- TUDO ESTÁ CARREGADO ----
        // Agora podemos inicializar AMBAS as sidebars

        // Inicializa a sidebar padrão (ID: 'sidebar', Botão: 'sidebarToggle')
        initializeSidebarToggle('sidebarToggle', 'sidebar');

        // Inicializa a sidebar do contador (ID: 'sidebarContador', Botão: 'sidebarContadorToggle')
        // Certifique-se de que os IDs '_sidebar_contador.html' e do botão no header correspondente estão corretos.
        initializeSidebarToggle('sidebarContadorToggle', 'sidebarContador'); 

        // Define o link ativo para AMBAS as sidebars
        setActiveNavLink('.sidebar'); // Para a sidebar padrão
        setActiveNavLink('.sidebar-contador'); // Para a sidebar do contador

    }).catch(error => {
        console.error("Erro ao carregar um ou mais componentes:", error);
    });

});


/**
 * Inicializa a lógica de abrir/fechar de um menu lateral específico.
 * @param {string} toggleButtonId - O ID do botão que controla o menu.
 * @param {string} sidebarId - O ID do elemento <aside> do menu.
 */
function initializeSidebarToggle(toggleButtonId, sidebarId) {
    const sidebarToggle = document.getElementById(toggleButtonId);
    const sidebar = document.getElementById(sidebarId);

    // Só adiciona o evento se AMBOS os elementos existirem na página atual
    if (sidebarToggle && sidebar) { 
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
        });
    } else {
        // Não mostra erro se não encontrar, pois nem toda página terá ambos os menus
        // console.warn(`Botão '${toggleButtonId}' ou Sidebar '${sidebarId}' não encontrado nesta página.`);
    }
}


/**
 * Adiciona a classe 'active' ao link de navegação correto dentro de uma sidebar específica.
 * @param {string} sidebarSelector - O seletor CSS para a sidebar (ex: '.sidebar', '.sidebar-contador').
 */
function setActiveNavLink(sidebarSelector) {
    // Pega o nome do arquivo da URL atual (ex: "dasmei.html")
    const currentPage = window.location.pathname.split("/").pop();

    if (currentPage && sidebarSelector) {
        // Verifica se a sidebar existe na página antes de procurar o link
        const sidebarElement = document.querySelector(sidebarSelector);
        if (sidebarElement) {
            // Procura um link DENTRO da sidebar especificada que corresponda
            const navLink = sidebarElement.querySelector(`.nav-link[href="${currentPage}"]`);
    
            if (navLink) {
                navLink.classList.add('active');
            }
        }
    }
}

