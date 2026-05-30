/* =========================================
   SELECTED USER
========================================= */

let selectedUser = null;

/* =========================================
   LOAD USERS
========================================= */

async function loadUsers(){

    const response =
        await fetch("/get_users");

    const users =
        await response.json();

    const chatList =
        document.getElementById(
            "chatList"
        );

    chatList.innerHTML = "";

    users.forEach(user => {

        const div =
            document.createElement("div");

        div.classList.add(
            "chat-item"
        );

        div.innerHTML = `

            <div class="chat-avatar">
                ${user.username
                    .charAt(0)
                    .toUpperCase()}
            </div>

            <div class="chat-info">
                <h4>${user.username}</h4>
                <p>${user.email}</p>
            </div>

        `;

        div.onclick = () => {

            selectedUser = user;

            document.getElementById(
                "chatUser"
            ).innerText =
                user.username;

            loadMessages(user.id);

        };

        chatList.appendChild(div);

    });

}

/* =========================================
   LOAD MESSAGES
========================================= */

async function loadMessages(userId){

    const response =
        await fetch(
            `/get_messages/${userId}`
        );

    const messages =
        await response.json();

    const msgBox =
        document.getElementById(
            "messages"
        );

    msgBox.innerHTML = "";

    messages.forEach(msg => {

        const div =
            document.createElement("div");

        div.classList.add(
            "message"
        );

        div.classList.add(

            msg.sender_username ===
            CURRENT_USERNAME

            ? "sent"

            : "received"

        );

        div.innerText =
            msg.message;

        msgBox.appendChild(div);

    });

}

/* =========================================
   SEND MESSAGE
========================================= */

async function sendMessage(){

    if(!selectedUser)
        return;

    const input =
        document.getElementById(
            "messageInput"
        );

    const message =
        input.value;

    if(message.trim() === "")
        return;

    await fetch("/send_message",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            receiver_id:
                selectedUser.id,

            message:
                message

        })

    });

    input.value = "";

    loadMessages(
        selectedUser.id
    );

}

/* =========================================
   AUTO LOAD
========================================= */

loadUsers();