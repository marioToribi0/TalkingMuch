$("#file-upload").css("opacity", "0");

$("#file-browser").click(function(e) {
  e.preventDefault();
  $("#file-upload").trigger("click");
});

var el = document.getElementById('id_file');
el.onchange = function(){
  document.getElementById('text-loading').innerHTML = 'Ready 😉';
  document.getElementById('send').style.display = 'inline';
};