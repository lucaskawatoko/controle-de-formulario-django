console.log("home.js");

document.addEventListener("DOMContentLoaded", function () {
    const carousels = document.querySelectorAll(".carousel");
  
    carousels.forEach((carousel) => {
      // Inicializa o carrossel do Bootstrap com controle manual
      const carouselInstance = new bootstrap.Carousel(carousel, {
        interval: 500, // Define o tempo de troca das imagens (0,5 segundos)
        ride: "carousel"
      });
  
      // Função para iniciar o autoplay
      const startAutoplay = () => carouselInstance.cycle();
  
      // Função para parar o autoplay
      const stopAutoplay = () => carouselInstance.pause();
  
      // Evento para iniciar o autoplay ao focar
      carousel.addEventListener("mouseenter", startAutoplay);
  
      // Evento para parar o autoplay ao desfocar
      carousel.addEventListener("mouseleave", stopAutoplay);
    });
  });
  