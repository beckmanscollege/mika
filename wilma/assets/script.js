document.addEventListener('keydown', function (event) {
    const elId = event.key.toLowerCase();
    const el = document.getElementById(elId);
    if (el) {
        const parent = el.parentNode;
        parent.querySelectorAll('.show').forEach((el) => {
            el.classList.remove('show');
            el.querySelectorAll('video, audio').forEach((media) => {
                media.currentTime = 0;
                //media.pause()
            });
        });
        el.classList.add('show');
        el.querySelectorAll('video, audio').forEach((media) => {
            if (media.readyState >= 3) {
                media.play();
            }
        });
    }
});
