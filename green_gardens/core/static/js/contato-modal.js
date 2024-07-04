export default function initContatoModal() {
    const modalContact = document.getElementById('modal_contato');

    // Funcao de abrir o modal de contato
    const sendMessageBtn = document.getElementById('send_message');
    sendMessageBtn.addEventListener('click', () => {
        modalContact.classList.add('active_animation')
    })

    // Funcao de fechar o modal de contato
    const closeMessageBtn = document.getElementById('close_message_btn');
    closeMessageBtn.addEventListener('click', () => {
        modalContact.classList.remove('active_animation')
    })
}
