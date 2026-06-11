document.addEventListener("DOMContentLoaded", () => {

    const menuItems =
    document.querySelectorAll(".sidebar nav a");

    menuItems.forEach(item => {

        item.addEventListener("click", () => {

            menuItems.forEach(i =>
                i.classList.remove("active")
            );

            item.classList.add("active");

        });

    });

});
async function searchUser() {

    const query =
    document.getElementById(
        "userSearch"
    ).value;

    const response =
    await fetch(
        `/search_user?query=${query}`
    );

    const users =
    await response.json();

    const results =
    document.getElementById(
        "searchResults"
    );

    results.innerHTML = "";

    users.forEach(user => {

        results.innerHTML += `

            <div class="user-card">

                <h4>${user.username}</h4>

                <button
                onclick="sendRequest(${user.id})">

                    Send Request

                </button>

            </div>

        `;

    });

}
async function sendRequest(receiverId){

    const response =
    await fetch(
        "/send_chat_request",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({

                receiver_id:
                receiverId

            })
        }
    );

    const data =
    await response.json();

    alert(data.message || "Request Sent");
}
async function loadRequests(){

    const response =
    await fetch("/chat_requests");

    const requests =
    await response.json();

    const requestBox =
    document.getElementById(
        "requestList"
    );

    if(!requestBox) return;

    requestBox.innerHTML = "";

    requests.forEach(req => {

        requestBox.innerHTML += `

        <div class="request-card">

            <p>
            ${req.sender_username}
            wants to chat
            </p>

            <button
            onclick="acceptRequest(
            ${req.request_id})">

            Accept

            </button>

            <button
            onclick="rejectRequest(
            ${req.request_id})">

            Reject

            </button>

        </div>

        `;

    });

}
async function acceptRequest(id){

    await fetch(
        "/accept_request",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({

                request_id:id

            })
        }
    );

    loadRequests();

    if(typeof loadUsers === "function"){
        loadUsers();
    }
}
async function rejectRequest(id){

    await fetch(
        "/reject_request",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({

                request_id:id

            })
        }
    );

    loadRequests();
}
document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadRequests();

    }
);
async function searchPeople(){

    const query =
    document.getElementById(
        "networkSearch"
    ).value;

    const response =
    await fetch(
        `/search_people?query=${query}`
    );

    const users =
    await response.json();

    const results =
    document.getElementById(
        "networkResults"
    );

    results.innerHTML = "";

    users.forEach(user => {

    results.innerHTML += `

    <div class="search-user-card">

        <div class="search-user-left">

            <div class="search-user-avatar">
                ${user.username[0].toUpperCase()}
            </div>

            <div class="search-user-info">

                <h4>${user.username}</h4>

                <p>${user.email}</p>

            </div>

        </div>

        <div style="display:flex;gap:10px;">

            <a
                href="/profile/${user.id}"
                class="profile-btn">

                Profile

            </a>

            <button
                class="connect-btn"
                onclick="sendConnection(${user.id})">

                Connect

            </button>

        </div>

    </div>

    `;

});

}
async function sendConnection(id){

    const response =
    await fetch(
        "/send_connection",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({

                receiver_id:id

            })

        }
    );

    const data =
    await response.json();

    alert(
        data.message ||
        "Connection Request Sent"
    );

}
async function loadConnectionRequests(){

    const response =
    await fetch(
        "/connection_requests"
    );

    const requests =
    await response.json();

    const container =
    document.getElementById(
        "connectionRequests"
    );

    if(!container) return;

    container.innerHTML = "";

    requests.forEach(req => {

        container.innerHTML += `

        <div class="request-card">

            <p>${req.username}</p>

            <button
            onclick="acceptConnection(
            ${req.request_id})">

                Accept

            </button>

        </div>

        `;

    });

}
async function acceptConnection(id){

    await fetch(
        "/accept_connection",
        {
            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({

                request_id:id

            })

        }
    );

    loadConnectionRequests();

}
loadConnectionRequests();

/* ===========================
   POST MODAL
=========================== */

function openPostModal(){

    document
    .getElementById("postModal")
    .classList.add("show");
}

function closePostModal(){

    document
    .getElementById("postModal")
    .classList.remove("show");
}
document.addEventListener("change",(e)=>{

    if(e.target.id !== "postMedia") return;

    const file = e.target.files[0];

    const preview =
    document.getElementById(
        "mediaPreview"
    );

    preview.innerHTML = "";

    if(!file) return;

    const url =
    URL.createObjectURL(file);

    if(file.type.startsWith("image")){

        preview.innerHTML = `
            <img
                src="${url}"
                class="preview-image">
        `;
    }
    else{

        preview.innerHTML = `
            <video
                src="${url}"
                controls
                class="preview-video">
            </video>
        `;
    }

});
async function createPost(){

    const caption =
    document.getElementById(
        "postCaption"
    ).value;

    const file =
    document.getElementById(
        "postMedia"
    ).files[0];

    const formData =
    new FormData();

    formData.append(
        "caption",
        caption
    );

    if(file){
        formData.append(
            "media",
            file
        );
    }

    const response =
    await fetch(
        "/create_post",
        {
            method:"POST",
            body:formData
        }
    );

    const data =
    await response.json();

    if(data.success){

        closePostModal();

        document
        .getElementById(
            "postCaption"
        ).value="";

        document
        .getElementById(
            "postMedia"
        ).value="";

        loadPosts();
    }
}

async function loadPosts(){

    const response =
    await fetch("/posts");

    const posts =
    await response.json();

    const feed =
    document.getElementById(
        "feedContainer"
    );

    feed.innerHTML = "";

    posts.forEach(post => {

        let mediaHTML = "";

        if(post.media_url){

            if(
                post.media_type
                .startsWith("image")
            ){

                mediaHTML = `
                    <img
                    src="${post.media_url}"
                    class="feed-image">
                `;
            }
            else{

                mediaHTML = `
                    <video
                    src="${post.media_url}"
                    controls
                    class="feed-video">
                    </video>
                `;
            }
        }

        feed.innerHTML += `

        <div class="post">

            <div class="post-header">

                <div class="user">

                    <div class="avatar">
                        ${post.username[0].toUpperCase()}
                    </div>

                    <div>

                        <h3>
                            ${post.username}
                        </h3>

                        <span>
                            ${post.created_at}
                        </span>

                    </div>

                </div>

            </div>

            <div class="post-content">
                ${post.caption || ""}
            </div>

            ${mediaHTML}

            <div class="post-actions">

                <span>❤️ Like</span>

                <span>💬 Comment</span>

                <span>🔁 Share</span>

            </div>

        </div>

        `;
    });
}

document.addEventListener(
    "DOMContentLoaded",
    loadPosts
);