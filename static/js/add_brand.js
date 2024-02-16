$("#add-brand").validate({
    rules: {
        name: {
            required:true
        },
        image: {
            required:true
        }
    },
    messages: {
        name: {
            required: "Please enter brand name"
        },
        image: {
            required: "Please upload image"
        }
    },
});
