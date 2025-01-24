API_URL = '/api/';



function generateChatId() {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < 12; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

function addChatLoader() {
    var cId = generateChatId();
    var time = getTime();
    $(".chat-box").append(`
        <div class="assistant-chat" id="${cId}">
            <img class="loading" src="./img/loading.gif">
        </div>
        <p class="assistant-chat-time">${time}</p>
    `);
    return cId
}


function getTime() {
    var date = new Date();
    var hours = date.getHours();
    var minutes = date.getMinutes();
    if (hours > 11) {
        if (hours == 12) {
            return `${hours}:${minutes} PM`;
        } else {
            return `${hours - 12}:${minutes} PM`;
        }
    } else {
        return `${hours}:${minutes} AM`;
    }
}

function initializeChat() {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const today = new Date();
    const day = String(today.getDate()).padStart(2, '0');
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const year = today.getFullYear();

    const formattedDate = `${day} ${months[parseInt(month) - 1]} ${year}`;
    const time = getTime();

    $(".chat-box").append(`
        <div class="chat-date">
            <p class="chat-date-text">
                ${formattedDate}
            </p>
        </div>
        <div class="assistant-chat">
            <p class="assistant-chat-text">Welcome, how can I help you today?</p>
        </div>
        <p class="assistant-chat-time">${time}</p>
    `);
}

function addMessage(text, type, cId) {
    var time = getTime();
    if (type == 'u') {
        $(".chat-box").append(`
            <div class="user-chat">
                <p class="user-chat-text">${text}</p>
            </div>
            <p class="user-chat-time">${time}</p>
        `);
    } else if (type == 'a') {
        $(`#${cId}`).html(`<p class="assistant-chat-text">${text}</p>`);
    }
}

function sendPostRequest(url, data) {
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            success: function (response) {
                resolve(response);
            },
            error: function (xhr, status, error) {
                reject(xhr.responseText);
            }
        });
    });
}



$('#send-button').click(function () {
    time = Date.now();
    ctext = $('#chat-text').val().trim()
    if (ctext != "") {
        addMessage(ctext, 'u')
        $('#chat-text').val('')
        var cId = addChatLoader();
        sendPostRequest(API_URL, { text: ctext }).then(function (response) {
            addMessage(response['answer'], 'a', cId);
        });
    }
});


initializeChat();