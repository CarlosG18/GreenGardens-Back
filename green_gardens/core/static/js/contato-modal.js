export default function initContatoModal(){const e=document.getElementById("modal_contato");document.getElementById("send_message").addEventListener("click",(()=>{e.classList.add("active_animation")}));document.getElementById("close_message_btn").addEventListener("click",(()=>{e.classList.remove("active_animation")}))}