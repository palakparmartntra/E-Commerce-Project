$("#add-section").validate({
    rules: {
        name: {
            required:true
        },
        section_file: {
            required:true
        }
    },
    messages: {
        name: {
            required: "Please enter section name"
        },
        section_file: {
            required: "Please upload excel file for this section"
        }
    },
});
