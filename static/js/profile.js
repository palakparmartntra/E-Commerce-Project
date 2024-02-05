$("#update_profile_form").validate({
    rules: {
        first_name: {
            required:true,
            minlength: 2,
            maxlength: 15
        },
        last_name: {
            required:true,
            minlength: 2
        },
        phone_no: {
            required:true,
            minlength: 10
        },
        email: {
            required:true,
            email: true
        }
    },
    messages: {
        first_name: {
            required: "Please enter first name",
            minlength: "Maximun length should be 2 characters",
            maxlength: "Maximun length should be 15 characters"
        },
        last_name: {
            required: "Please enter last name",
            maxlength: "Min length should be 2 characters"
        },
        phone_no: {
            required: "Please enter phone number",
            minlength: "Phone number must have 10 digits"
        },
        email: {
            required: "Please enter your email address",
            email: "Please enter correct email address"
        }
    },
});
