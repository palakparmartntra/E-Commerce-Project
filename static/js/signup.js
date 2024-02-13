$(document).ready(function () {
    $("#signupform").validate({
        rules: {
            email: {
                 required: true,
                 email: true
            },
            username: {
                required: true,
                minlength: 3,
                maxlength: 10
            },
            password1: {
                 required: true,
                 pwcheck: true,
                 minlength: 8
            },
            password2: {
                required: true,
                equalTo: "#id_password1"
            }
        },
        messages: {
            email: {
                required: "Specify email address",
                email: "invalid email format"
            },
            username: {
                required: "Please enter username",
            },
            password1: {
                required: "Specify password",
                pwcheck: "The password does not match the criteria!",
                minlength: "The password does not meet the criteria!"
            },
            password2: {
                required: "Repeat password",
                equalTo: "The passwords do not match"
            },
        },
    });
});
