export default function initScrollSection() {

 //Funcao para dar o scroll ate a secao
 function scrollToSetion(event) {
    event.preventDefault()

    //Pega o href do botao apertado
    const href = event.currentTarget.getAttribute('href')
    const section = document.querySelector(href);
 
    //Pega o header e seu height
    const header = document.querySelector('header');
    const headerHeight = parseFloat(window.getComputedStyle(header).height); //Pega p height pos css e tranforma em number


    const sectionTop = section.offsetTop - headerHeight; //Subtrai o top secao com o height do header

    //Metodo de scroll do window
    window.scrollTo({
        top: sectionTop,
        behavior: "smooth",
    })
}

//Pega os botoes de link para secao e adiciona um event listener de clique
const linkButtons = document.querySelectorAll('[href^="#"]')
linkButtons.forEach(btn => {
    btn.addEventListener('click', scrollToSetion);
})

}
