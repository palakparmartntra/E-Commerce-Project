$('#banner').validate({
rules: {
    banner_name:{
        required:true
    },
    banner_image:{
        required:true
    }
 },
 messages: {
    banner_name:{
    required:'Please enter banner name'
    },
     banner_image:{
    required:'Please attach banner image'
    },

 }
});
$('#updatebanner').validate({
rules: {
    banner_name:{
        required:true
    },

 },
 messages: {
    banner_name:{
    required:'Please enter banner name'
    },


 }
});
