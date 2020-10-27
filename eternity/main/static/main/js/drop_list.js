function showMenu{{detail_post.id}}(){
    document.getElementById('droplist{{ detail_post.id }}').classList.toggle("show");
}
window.onclick = function(event) {
    if (!event.target.matches('.drop-icon')) {
        var droplist = document.getElementsByClassName('drop-list');
        var i;
        for (i = 0; i < droplist.length; i++) {
            var opendroplist = droplist[i];
            if (opendroplist.classList.contains('show')) {
                opendroplist.classList.remove('show');
            }
        }
    }
}
