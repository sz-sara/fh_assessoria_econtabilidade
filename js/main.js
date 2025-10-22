// Espera o DOM carregar antes de executar
document.addEventListener("DOMContentLoaded", function() {
    
    // Lista de componentes para carregar [ID_do_placeholder, arquivo_html]
    const components = [
        ["header-placeholder", "_header.html"],
        ["sidebar-placeholder", "_sidebar.html"]
    ];

    // Função para carregar um único componente
    const loadHTML = (url, elementId) => {
        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Não foi possível carregar ${url}: ${response.statusText}`);
                }
                return response.text();
            })
            .then(data => {
                const element = document.getElementById(elementId);
                if (element) {
                    element.innerHTML = data;
                } else {
                    console.warn(`Placeholder com ID '${elementId}' não encontrado.`);
                }
            });
    };

    // Carrega todos os componentes em paralelo
    Promise.all(
        components.map(comp => loadHTML(comp[1], comp[0]))
    ).then(() => {
        // ---- TUDO ESTÁ CARREGADO ----
        // Agora podemos executar os scripts que dependem desses componentes
        
        initializeSidebarToggle();
        setActiveNavLink();

    }).catch(error => {
        console.error("Erro ao carregar um ou mais componentes:", error);
    });

});


/**
 * Inicializa a lógica de abrir/fechar do menu lateral.
 * Esta função SÓ é chamada DEPOIS que o header e o sidebar foram carregados.
 */
function initializeSidebarToggle() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
        });
    } else {
        console.error("Botão 'sidebarToggle' ou 'sidebar' não encontrado após o carregamento.");
    }
}


/**
 * Adiciona a classe 'active' ao link de navegação correto,
 * com base na página que está aberta.
 */
function setActiveNavLink() {
    // Pega o nome do arquivo da URL atual (ex: "dasmei.html")
    const currentPage = window.location.pathname.split("/").pop();

    if (currentPage) {
        // Procura um link no sidebar que corresponda exatamente ao nome do arquivo
        const navLink = document.querySelector(`.sidebar .nav-link[href="${currentPage}"]`);
        
        if (navLink) {
            navLink.classList.add('active');
        }
    }
}
