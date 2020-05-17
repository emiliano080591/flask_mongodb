const   btnGetUsers = document.getElementById("btnGetUsers"),
        btnEnviarForm = document.getElementById("btnEnviarFile"),
        file = document.querySelector('input[type="file"]'),
        btnEnviarForm2 = document.getElementById("btnEnviar"),
        username = document.getElementById("username"),
        pass = document.getElementById("pass"),
        email = document.getElementById("email");

        
/*
*****************
PETICIONES GET  *
*****************
*/
 //obtiene todos los usuarios
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
}); //fin de btnGetUsers

/*
****************
PETICIONES POST*
****************
*/

btnEnviarForm.addEventListener("click", () => {
    var data = new FormData();
    data.append('file', file.files[0]);
    fetch('http://localhost:5000/upload', {
        headers:{
            'Access-Control-Allow-Origin':'*'
        },
        method: 'POST',
        body: data
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

//registra un usuario
btnEnviarForm2.addEventListener("click", () => {
    var dataSend=new FormData();
    dataSend.append('username',username.value);
    dataSend.append('password',pass.value);
    dataSend.append('email',email.value);

    fetch('http://localhost:8000/users', {
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
});//fin de btnEnviarForm2


