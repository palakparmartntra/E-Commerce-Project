$("#update_address_form").validate({
    rules: {
        receiver_name: {
            required:true
        },
        phone_no: {
            required:true,
            minlength: 10
        },
        house_no: {
            required:true
        },
        street: {
            required:true
        },
        landmark: {
            required:true
        },
        city: {
            required:true
        },
        state: {
            required:true
        },
        zipcode: {
            required:true,
            minlength: 6,
            maxlength: 6
        }
    },
    messages: {
        receiver_name: {
            required: "Please enter receiver name"
        },
        phone_no: {
            required: "Please enter phone number",
            minlength: "Phone number must have 10 digits",
            maxlength: "Phone number must have 10 digits"
        },
        house_no: {
            required: "Please enter house number"
        },
        street: {
            required: "Please enter street"
        },
        landmark: {
            required: "Please enter landmark"
        },
        city: {
            required: "Please enter city"
        },
        state: {
            required: "Please enter state"
        },
        zipcode: {
            required: "Please enter zipcode",
            minlength: "Zipcode must have 6 digits",
            maxlength: "Zipcode must have 6 digits"
        }
    },
});
