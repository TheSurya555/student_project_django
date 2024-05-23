document.addEventListener('DOMContentLoaded', function () {
    const inboxLink = document.getElementById('inboxLink');
    const sentLink = document.getElementById('sentLink');
    const composeLink = document.getElementById('composeLink');

    const inboxSection = document.getElementById('inboxSection');
    const sentSection = document.getElementById('sentSection');
    const composeSection = document.getElementById('composeSection');

    inboxLink.addEventListener('click', function () {
        inboxLink.classList.add('active');
        sentLink.classList.remove('active');
        composeLink.classList.remove('active');

        inboxSection.classList.add('active');
        sentSection.classList.remove('active');
        composeSection.classList.remove('active');
    });

    sentLink.addEventListener('click', function () {
        inboxLink.classList.remove('active');
        sentLink.classList.add('active');
        composeLink.classList.remove('active');

        inboxSection.classList.remove('active');
        sentSection.classList.add('active');
        composeSection.classList.remove('active');
    });

    composeLink.addEventListener('click', function () {
        inboxLink.classList.remove('active');
        sentLink.classList.remove('active');
        composeLink.classList.add('active');

        inboxSection.classList.remove('active');
        sentSection.classList.remove('active');
        composeSection.classList.add('active');
    });
});
