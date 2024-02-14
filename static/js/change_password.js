$(document).ready(function ($) {
    $("#changepasswordform").validate({
        rules: {
            oldpassword: {
                required: true
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
            oldpassword: {
                required: "Please enter current password",
            },
            password1: {
                required: "Specify password",
                pwcheck: "The password does not match the criteria!",
                minlength: "The password does not meet the criteria!"
            },
            password2: {
                required: "Repeat password",
                equalTo: "The passwords do not match"
            }
        },
    });
});
