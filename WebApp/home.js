// /pair
// /logout
$('form').submit(function(event){
    event.preventDefault();
    let post_endpoint = $(this).attr("action")
    let id_number = $(this).serialize();

    $.ajax({
        url: post_endpoint,
        type: "POST",
        data: id_number,
        success: function(data) {
            json = toJSON(data);
        },
        error: function(ts){
            alert(ts.responseText);
        }
    }).done(function(response){
        json = toJSON(response);
        status = json['status'];
        if (choose_dir(status)){
            location.href = 'settings.html';
        } else{
            console.log('here')
            $('#idnum').html('Incorrect ID number, please try again!')
        }
    })
})