$('#updatecategory').validate({
rules: {
        name:{
        required:true
        }
 },
 messgaes: {
    name:{
    required:'please enter category name'
    }
 }
});




//Function To Display Popup
function div_show() {
document.getElementById('abc').style.display = "block";
}
//Function to Hide Popup
function div_hide(){
document.getElementById('abc').style.display = "none";
}

