$("#update_address_form").validate({
    rules: {
        purchase_quantity: {
            minlength: 1,
            maxlength: 6
        }
    },
    messages: {
        purchase_quantity: {
            minlength: "minimum 1 quantity is required",
            maxlength: "maximum 6 is allowed"
        }
    },
});
