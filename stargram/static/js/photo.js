
const photoJson = () => {
    $.ajax({
        url: 'http://127.0.0.1:8000/photo_json',
        type: 'GET',
        async: false,
        success: function(data) {
            console.log(data)
            }
      });
}

window.onload = () => {
    console.log("ggg")
    photoJson();
};