(function() {

    // Create and connect sockert
    var socket = io.connect('/chat');

    // Grab some references
    var $status = $('#status');
    var $login_form = $('#login');
    var $logout_form = $('#logout');
    var $chat_form = $('#chat');
    var $users = $('#users');
    var $chat = $('#chat-data');

    // Bind the login form
    $login_form.bind('submit', function() {
        var $input = $(this).find('input');
        socket.emit('login', $input.val());
        $login_form.toggleClass('hidden');
        $logout_form.toggleClass('hidden');
        $input.val('');
        return false;
    });

    $logout_form.bind('submit', function() {
        socket.emit('logout');
        $login_form.toggleClass('hidden');
        $logout_form.toggleClass('hidden');
        return false;
    });

    // Bind the chat form
    $chat_form.bind('submit', function() {
        var $input = $(this).find('input');
        scroll_chat();
        socket.emit('chat', $input.val());
        $input.val('');
        return false;
    });

    // List of currently logged-in users
    var users = [];

    // Bind events to the socket
    socket.on('connect', function() {
        $status.html('<b>Connected: ' + socket.socket.transport.name + '</b>');
    });
    socket.on('error', function() {
        $status.html('<b>Error</b>');
    });
    socket.on('disconnect', function() {
        $status.html('<b>Closed</b>');
    });
    socket.on('enter', function(msg) {
        users.push(msg);
        render_users();
        append_chat($('<em>' + msg + '</em> has entered the game.<br/>'));
    });
    socket.on('exit', function(msg) {
        users = $.grep(users, function(value, index) {
            return value != msg });
        render_users();
        append_chat($('<em>' + msg + '</em> has left the game.<br/>'));
    });
    socket.on('users', function(msg) {
        users = msg;
        render_users();
    });
    socket.on('chat', function(msg) {
        append_chat($('<li>' + msg.m + '</li>'));
    });

    // Some helper functions
    function render_users() {
        var result = $.map(users, function(value, index) {
            return '<li>' + value + '</li>';
        });
        $users.html(result.join('\n'));
    }
    function scroll_chat() {
        var new_scrolltop = $chat.prop('scrollHeight') - $chat.height();
        $chat.prop({ scrollTop: new_scrolltop});
    }
    function append_chat(msg) {
        var old_scrolltop = $chat.prop('scrollTop');
        var new_scrolltop = $chat.prop('scrollHeight') - $chat.height();
        var scroll = old_scrolltop == new_scrolltop;
        $chat.append(msg);
        if(scroll) {
            scroll_chat();
        }
    }
})();
