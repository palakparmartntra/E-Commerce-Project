$("#update-brand").validate({
    rules: {
        name: {
            required:true
        }
    },
    messages: {
        name: {
            required: "Please enter brand name"
        }
    },
});
