window.addEventListener('message', (event) => {
    const keyCommand = event.data;
    const keyEvent = new KeyboardEvent('keydown', {
        key: keyCommand,
        code: `Key${keyCommand}`,
        keyCode: keyCommand.charCodeAt(0),
    });

    document.dispatchEvent(keyEvent);
    console.log(`Received and interpreted key command: ${keyCommand}`);
});
