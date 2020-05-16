const   btnGetUsers = document.getElementById("btnGetUsers"),
        btnEnviarForm2 = document.getElementById("btnEnviar"),
        username = document.getElementById("username"),
        pass = document.getElementById("pass"),
        email = document.getElementById("email");

btnEnviarForm2.addEventListener("click", () => {
    var dataSend=new FormData();
    dataSend.append('username',username.value);
    dataSend.append('password',pass.value);
    dataSend.append('email',email.value);

    fetch('http://localhost:5000/registro', {
        method: 'POST',
        body: dataSend
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        console.log(data);
    })
    .catch(function(err) {
        console.error(err);
    });
});

btnGetUsers.addEventListener("click", () => {
    fetch('http://localhost:5000/users')
        .then(response=> {
            return response.json();
        })
        .then(data=> {
            console.log(data);
        })
        .catch(err=> {
            console.error(err);
        });
});
