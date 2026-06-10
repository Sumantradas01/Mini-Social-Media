function sendConnection(userId){

    fetch("/send_connection",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            receiver_id:userId
        })

    })

    .then(r=>r.json())

    .then(data=>{

        alert("Friend Request Sent");

    });

}


function sendChatRequest(userId){

    fetch("/send_chat_request",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            receiver_id:userId
        })

    })

    .then(r=>r.json())

    .then(data=>{

        alert("Chat Request Sent");

    });

}