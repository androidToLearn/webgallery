let allUsersDivs = document.getElementsByClassName('other_chat');
let allPNameUsers = document.getElementsByClassName('b');

for (let i = 0; i < allUsersDivs.length; i++) {
    allUsersDivs[i].addEventListener('click', (event) => {
        console.log('clicked');
        fetch('/add_user', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 'contact': allPNameUsers[i].innerText + '' }) }).then((response) => {
            window.location.reload();
        });
    });
}