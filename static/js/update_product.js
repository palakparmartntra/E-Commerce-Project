$('#updateproduct').validate({
rules: {
    name:{
        required:true
    },
    description:{
        required:true
    },
    quantity:{
        required:true
    },
    price:{
        required:true
    },
    category:{
        required:true
    },
    brand:{
        required:true
    }
 },
 messages: {
    name:{
        required:'Please enter product name'
    },
    description:{
        required:'Please enter product description'
    },
    quantity:{
        required:'Please enter product quantity'
    },
    price:{
        required:'Please enter product price'
    },
    category:{
        required:'Please enter product category'
    },
    brand:{
        required:'Please enter product brand'
    }
 }
});
