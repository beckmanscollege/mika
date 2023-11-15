const receiverWindow = window.open('robot.html'); // Open the receiver page
document.addEventListener('keydown', function (event) {
    receiverWindow.postMessage(event.key, '*');
});
