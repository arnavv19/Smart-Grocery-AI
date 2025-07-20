function addToShoppingList(item) {
    fetch('/add_to_list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'item=' + item,
    }).then(response => {
        window.location.reload();
    });
}
