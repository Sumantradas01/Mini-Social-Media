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

async function uploadProfilePicture(){

    const file =
    document.getElementById(
        "profilePicInput"
    ).files[0];

    if(!file){

        alert("Select an image");

        return;
    }

    const formData =
    new FormData();

    formData.append(
        "profile_picture",
        file
    );

    const response =
    await fetch(
        "/upload_profile_picture",
        {
            method:"POST",
            body:formData
        }
    );

    const data =
    await response.json();

    if(data.success){

        location.reload();

    }else{

        alert(data.message);
    }
}

async function updateBio(){

    const bio =
    document.getElementById(
        "bioText"
    ).value;

    const response =
    await fetch(
        "/update_bio",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({
                bio:bio
            })
        }
    );

    const data =
    await response.json();

    if(data.success){

        alert("Bio Updated");

        location.reload();

    }else{

        alert(data.message);
    }
}

async function updateBio(){

    const bio =
    document.getElementById(
        "bioText"
    ).value;

    const response =
    await fetch(
        "/update_bio",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({
                bio:bio
            })
        }
    );

    const data =
    await response.json();

    if(data.success){

        alert("Bio Updated");

        location.reload();

    }else{

        alert(data.message);
    }
}