export default function initServicosCarrossel() {
    const carrosselServicos = new Swiper('.carrossel_servicos', {
        navigation: {
                    nextEl: '.swiper-button-next-servicos',
                    prevEl: '.swiper-button-prev-servicos',
                },
        
          direction: 'horizontal',
          loop: true,
          slidesPerView: 1,
        });
}