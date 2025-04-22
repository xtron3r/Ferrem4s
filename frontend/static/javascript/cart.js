var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var libroId = this.dataset.libro;
        var action = this.dataset.action;
        console.log('libroId:', libroId, 'action:', action);

        console.log('USER:', user);
        if (user === 'AnonymousUser') {
            console.log('User is not authenticated');
        } else {
            updateUserOrder(libroId, action);
        }
    });
}

function updateUserOrder(libroId, action) {
    console.log('User is authenticated, sending data...');

    var url = '/update_item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'libroId': libroId, 'action': action})
    })
    .then((response) => {
       return response.json();
    })
    .then((data) => {
        console.log('data:', data);
        location.reload();
    });
}
