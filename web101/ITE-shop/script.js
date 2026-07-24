let cart = [];

function addItem(name, price) {
    cart.push({ name, price });
    showCart();
}

function removeItem(index) {
    cart.splice(index, 1);
    showCart();
}

function showCart() {

    let list = document.getElementById("cartList");
    list.innerHTML = "";

    let total = 0;

    cart.forEach((item, index) => {

        total += item.price;

        list.innerHTML += `
        <li>
            ${item.name} - $${item.price.toFixed(2)}
            <button class="remove" onclick="removeItem(${index})">X</button>
        </li>`;
    });

    document.getElementById("total").innerHTML = total.toFixed(2);
    document.getElementById("count").innerHTML = cart.length;
}