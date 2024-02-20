$('#updatecategory').validate({
rules: {
        name:{
        required:true
        }
 },
 messages: {
    name:{
    required:'Please enter category name'
    }
 }
});
