export default function initAnimationScroll() {
    const sections = document.querySelectorAll('[data-anima="scroll"]');
    const windowHeight = window.innerHeight * 0.8; //80% da altura da janela

    if(sections.length > 0) { //Verica se existe seções para adicionar a animação
        function scrollAnimation() {
            sections.forEach(section => {
        
                const sectionTop = section.getBoundingClientRect().top;
                const isSectionVisible = (sectionTop - windowHeight) < 0  // Verifica se o topo da seção - 60% da janela é maior que 0
        
                if(isSectionVisible) { 
                    section.classList.add("active_animation_scroll"); // Animação na descida da página
                }  
                
            })
        }
        scrollAnimation()
        
        window.addEventListener('scroll', scrollAnimation);
    }

}


