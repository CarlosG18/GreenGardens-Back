export default function initValoresCarrossel() {
  const carrosselValores = new Swiper('.carrossel_valores', {
    effect: "coverflow",
    grabCursor: true,
    centeredSlides: true,
    coverflowEffect: {
      rotate: 0,
      stretch: 0,
      depth: 0,
      modifier: 1,
      slideShadows: true,
    },
    loop: true, // Mantém o loop
    breakpoints: {
      1100: {
        slidesPerView: 3,
        spaceBetween: 30,
      },
      900: {
        slidesPerView: 2.5,
        spaceBetween: 30,
      },
      800: {
        slidesPerView: 1.5,
        spaceBetween: 30,
      },
      600: {
        slidesPerView: 1.3,
        spaceBetween: 10,
      },
      450: {
        slidesPerView: 1,
        spaceBetween: 10,
      },
      300: {
        slidesPerView: 1,
        spaceBetween: 10,
      },
    },
  });
}
