document.addEventListener('DOMContentLoaded', function() {
    var socket = io("wss://" + document.domain + ":" + location.port);
    var chatForm = document.getElementById('chat-form');
    var chatInput = document.getElementById('chat-input');
    var chatContainer = document.getElementById('chat-container');
    var chatMessages = document.getElementById('chat-messages');
    var hiddenRoomId = document.getElementById('room_id');

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();
        sendMessage();
    });

    function sendMessage() {
        var message = chatInput.value;
        var username = document.getElementById('username-input').value || 'Anonymous';
        var room_id = document.getElementById('room_id').value;
        if (message) {
            console.log('Sending message:', message, 'from user:', username, 'to room:', room_id);
            socket.emit('send_message', {username: username, message: message, room_id: room_id});
            chatInput.value = '';
        }
    }

    function addMessageToChat(username, message) {
        const chatMessages = document.getElementById('chat-messages');
        const chatMessage = document.createElement('p');
        chatMessage.classList.add('chat-message');

        const usernameSpan = document.createElement('span');
        usernameSpan.classList.add('username');
        usernameSpan.textContent = username + ': ';

        const messageSpan = document.createElement('span');
        messageSpan.textContent = message;

        chatMessage.appendChild(usernameSpan);
        chatMessage.appendChild(messageSpan);
        chatMessages.appendChild(chatMessage);

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    socket.on('receive_message', function(data) {
        console.log("Message event received on client side");
        console.log("Received message:", data.message, "from user:", data.username, "in room:", data.room_id);
        
        // Call the addMessageToChat function here
        addMessageToChat(data.username, data.message);
    });

    // Video synchronization
    socket.on('play_video', function() {
        console.log("Play video event received on client side");

        const videoPlayer = document.getElementById('video_url');
        videoPlayer.play();
    });

    socket.on('pause_video', function() {
        const videoPlayer = document.getElementById('video_url');
        videoPlayer.pause();
    });

    socket.on('seek_video', function(time) {
        const videoPlayer = document.getElementById('video_url');
        videoPlayer.currentTime = time;
    });

    const videoPlayer = document.getElementById('video_url');
    videoPlayer.addEventListener('play', function() {
        socket.emit('play_video');
    });

    videoPlayer.addEventListener('pause', function() {
        socket.emit('pause_video');
    });

    videoPlayer.addEventListener('seeked', function() {
        socket.emit('seek_video', videoPlayer.currentTime);
    });
});
