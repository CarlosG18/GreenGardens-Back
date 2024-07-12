export default function initSliderHome() {
    const slider = new Swiper('.swiper', {
        autoplay: {
          delay: 5000,
        },

        direction: 'horizontal',
        loop: true,
      
        // If we need pagination
        pagination: {
          el: '.swiper-pagination',
          clickable: true,
        },

      
        // Navigation arrows
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        }
      });
}
