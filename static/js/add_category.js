$('#addcategory').validate({
rules: {
        name:{
        required:true
        }
 },
 messgaes: {
    name:{
    required:'Please enter category name'
    }
 }
});
