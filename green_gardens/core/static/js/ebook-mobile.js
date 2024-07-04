export default function initShowMoreText() {

    const text = document.getElementById('read_more_text');

    // Funcao de mostrar o resto do texto ao clique
    const buttonShowText = document.getElementById('show_more_text');
    buttonShowText.addEventListener('click', () => {
        text.style.display = 'inline';
        buttonShowText.style.display = 'none'
    })
}

