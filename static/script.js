async function sendMessage(){

let input = document.getElementById("user-input")

let chatBox = document.getElementById("chat-box")

let message = input.value

chatBox.innerHTML += `<div class="message user">${message}</div>`

input.value = ""

let response = await fetch("/chatbot",{

method:"POST",

headers:{"Content-Type":"application/json"},

body:JSON.stringify({message:message})

})

let data = await response.json()

chatBox.innerHTML += `<div class="message bot">${data.reply}</div>`

chatBox.scrollTop = chatBox.scrollHeight

}