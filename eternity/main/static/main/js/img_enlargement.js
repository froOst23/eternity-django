var modal = document.getElementById('myModal');
var img = document.getElementById('detailImg');
var modalImg = document.getElementById('targetImg');

img.onclick = function() {
    modal.style.display = "block";
    modalImg.src = this.src;
}

var span = document.getElementsByClassName("close")[0];
span.onclick = function(e) {
    modal.style.display = "none";
}
