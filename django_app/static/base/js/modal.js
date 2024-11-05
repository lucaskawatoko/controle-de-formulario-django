console.log("modal carregado");

document.addEventListener("DOMContentLoaded", function() {
    // Configuração: Defina o tempo para reexibir o modal (em segundos)
    const modalDisplayInterval = {
        value: 1, // Tempo padrão: 30 segundos
        unit: 'days' // Unidade de tempo: 'seconds', 'minutes', 'hours', 'days'
    };

    // Função para converter o tempo de exibição baseado na unidade escolhida
    function convertTimeToSeconds(value, unit) {
        switch (unit) {
            case 'minutes':
                return value * 60; // Minutos para segundos
            case 'hours':
                return value * 60 * 60; // Horas para segundos
            case 'days':
                return value * 60 * 60 * 24; // Dias para segundos
            default:
                return value; // Já está em segundos
        }
    }

    // Função para mostrar o modal de boas-vindas
    function showWelcomeModal() {
        let modal = new bootstrap.Modal(document.getElementById('welcomeModal'));
        modal.show();
    }

    // Função para calcular a diferença em segundos entre duas datas
    function timeDifferenceInSeconds(date1, date2) {
        const diffInMs = Math.abs(date2 - date1);
        return Math.floor(diffInMs / 1000); // Converte milissegundos em segundos
    }

    // Verifica o localStorage
    const lastVisit = localStorage.getItem('lastVisit');
    const now = new Date();
    const timeLimitInSeconds = convertTimeToSeconds(modalDisplayInterval.value, modalDisplayInterval.unit);

    if (!lastVisit) {
        // Se é a primeira visita ou o dado não existe no localStorage
        showWelcomeModal();
        localStorage.setItem('lastVisit', now); // Armazena a hora atual
    } else {
        // Calcula a diferença de tempo entre agora e a última visita em segundos
        const lastVisitDate = new Date(lastVisit);
        const timeDifference = timeDifferenceInSeconds(lastVisitDate, now);

        // Exibe o modal se a diferença for maior que o tempo configurado
        if (timeDifference > timeLimitInSeconds) {
            showWelcomeModal();
        }

        // Atualiza a última visita no localStorage
        localStorage.setItem('lastVisit', now);
    }
});
