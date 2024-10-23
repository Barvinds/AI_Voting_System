$(document).ready(function(){
  $('#submitBtn').click(function(e){
    e.preventDefault(); 


    var name = $('#name').val().trim();
    var phone = $('#pnum').val().trim();


    if(name !== "" && phone !== "") {

      if(name === "barvin" && phone === "8870666787") {

        window.location.href = 'dashboard.html';
      } else {

        showError("Details are wrong");
      }
    } else {

      showError("Please fill in all details");
    }
  });


  function showError(message) {
    $('#error_container').html('<p class="error_message">' + message + '</p>');
  }
});
