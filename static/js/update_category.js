$('#updatecategory').validate({
rules: {
        name:{
        required:true
        },
        parent:{
        required:true
        },

 },
 messages: {
    name:{
    required:'Please enter category name'
    },
    parent:{
    required:'Please enter Parent category'
    },

 }
});
