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
            required: "Please enter brand name"
        },
        section_file: {
            required: "Please upload excel file for this section"
        }
    },
});
