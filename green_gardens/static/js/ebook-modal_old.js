export default function initEbookModal() {
    const modalBox = document.querySelector('.modal_box');
    const modalForms = document.getElementById('modalForm')
    
    //Abrir o modal
    
    const openModalBtns = document.querySelectorAll('[data-buttonModal]');
    openModalBtns.forEach((btn) => {
        btn.addEventListener('click', () => {
            modalBox.classList.add('active_animation');
            modalForms.style.display = 'block';
        })
    })
    
    
    //Fechar o modal
    
    function closeModal(modal) { 
        modal.classList.remove('active_animation')
    }
    
    const closeModalBtn = document.getElementById('backModalBtn');
    closeModalBtn.addEventListener('click', (event) => {
        event.preventDefault();
        closeModal(modalBox);
    });
    
    //Fechar modal com outise click
    
    modalBox.addEventListener('click', (event) => {
        if(event.target === modalBox) {
            closeModal(modalBox)
        }
    })
    
    
    // Verifica os input e abre modal download com sucesso
    
    const modalInputName = document.getElementById('modalName');
    addInputListener(modalInputName);
    const modalInputPhone = document.getElementById('modalTelefone');
    addInputListener(modalInputPhone);
    const modalInputEmail = document.getElementById('modalEmail');
    addInputListener(modalInputEmail)
    
    function addInputListener(input) {  
        input.addEventListener('input', (event) => {   // Adicionar um Listener pra cada input, sem precisar repetir
            let inputValue = event.target.value;
    
        })
    }

    function validateForm() {
        return modalInputName.value.length > 3 && modalInputPhone.value.length > 8 && modalInputEmail.value.length > 7;
    }
    
    const downloadFinished = document.getElementById('downloadFinished');

    modalForms.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData(modalForms);

        try {
            const response = await fetch(modalForms.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
                }
            });

            // Verifique o status da resposta e se é um JSON válido
            if (response.ok) {
                const data = await response.json();
                modalForms.style.display = 'none';
                downloadFinished.classList.add('active_animation')

                //closeModal(modalBox);
                //downloadFinished.classList.add("active_animation");

                Toastify({
                    text: "Sucesso!",
                    duration: 3000,
                    close: true,
                    gravity: "top",
                    position: "right",
                    stopOnFocus: false,
                    style: { background: "white", color: "#242C12" },
                }).showToast();

                modalInputName.value = "";
                modalInputPhone.value = "";
                modalInputEmail.value = "";

                window.location.href = data.url_download;

            } else {
                Toastify({
                    text: "Erro ao processar o formulário!",
                    duration: 3000,
                    close: true,
                    gravity: "top",
                    position: "right",
                    stopOnFocus: true,
                    style: { background: "red" },
                }).showToast();
                console.error('Erro na requisição:', response.statusText);  // Mostra erros na requisição
            }
        } catch (error) {
            console.error('Erro na operação fetch:', error);  // Mostra erros na operação fetch
            Toastify({ //Lib de alert 
                text: "Preencha os campos corretamente!",
                duration: 3000,
                close: true,
                gravity: "top", 
                position: "right",
                stopOnFocus: true, 
                style: {
                  background: "red",
                },
                
              }).showToast();
        }
        });
    
    // Fechar o a tela de dowload com sucesso
    
    const closeDowloadBtn = document.getElementById('CloseDowloadBtn');
    closeDowloadBtn.addEventListener('click', (event) => {
        event.preventDefault();
        closeModal(modalBox); // Fechar o modal inteiro
        closeModal(downloadFinished); // Fechar a tela de download
    })
}