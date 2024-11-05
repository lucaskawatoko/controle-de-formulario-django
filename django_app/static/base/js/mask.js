document.addEventListener('DOMContentLoaded', function() {
    // Verificação periódica para aplicar a máscara de número de celular brasileiro
    const intervalId = setInterval(() => {
        const phoneFields = document.querySelectorAll('[name="telefone"]');
  
        if (phoneFields.length > 0) {
            console.clear(); // Limpa o console ao encontrar os campos de telefone
  
            // Aplica a máscara a cada campo encontrado
            phoneFields.forEach(field => {
                // Aplica a máscara ao carregar o campo
                applyPhoneMask(field);
  
                // Adiciona evento de input para atualizar a máscara
                field.addEventListener("input", function () {
                    applyPhoneMask(field);
                });
            });
  
            // Limpa o intervalo para que o código execute apenas uma vez e evita logs repetidos
            clearInterval(intervalId);
        }
    }, 500); // Verifica a cada 500ms
  
    function applyPhoneMask(field) {
        // Remove qualquer caractere não numérico
        let value = field.value.replace(/\D/g, "");
  
        // Verifica se o valor está vazio, se sim, limpa o campo
        if (value === "") {
            field.value = "";
            return; // Sai da função para não aplicar máscara
        }
  
        // Limita o número a 11 dígitos (DDD + número)
        if (value.length > 11) {
            value = value.substring(0, 11);
        }
        
        // Formata o valor com a máscara de telefone
        if (value.length === 11) {
            value = value.replace(/^(\d{2})(\d{5})(\d{4})$/, "($1) $2-$3");
        } else if (value.length > 6) {
            value = value.replace(/^(\d{2})(\d{4})(\d{0,4})$/, "($1) $2-$3");
        } else if (value.length > 2) {
            value = value.replace(/^(\d{2})(\d{0,5})$/, "($1) $2");
        } else {
            value = value.replace(/^(\d*)$/, "($1");
        }
  
        // Atualiza o valor do campo
        field.value = value;
    }
});
