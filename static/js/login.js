$(document).ready(function () {
    $("#loginform").validate({
        rules: {
            login: {
                required: true
            },
            password:{
                required: true
            }
        },
        messages: {
            login: {
                required: "Please enter username"
            },
            password:{
                required: "Please enter password"
            }
        },
    });
});
