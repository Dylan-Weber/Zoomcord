// Animate slide bars
var slider = document.getElementById('min_speed_slider');
var reading = slider.value;
console.log(slider, reading)

slider.oninput = () => {
    document.getElementById('min_speed').innerHTML = `Minimum Movement Spped: ${this.value}`;
}


//Post req for max and min_speed
$('form').submit(function(event){
    event.preventDefault();
    let post_endpoint = $(this).attr("action")
    let min_speed = $('#min_speed').value;

    $.ajax({
        url: post_endpoint,
        type: "POST",
        data: `min_speed=${min_speed}`,
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
            location.href = 'main.html';
            localStorage.setItem('min_speed', min_speed);
        } else{
            console.log('here')
            //$('#idnum').html('Incorrect ID number, please try again!')
        }
    })
})