var socket = new WebSocket("ws://localhost:9000/ws");
socket.onopen = function (event) { socket.send("Here is some text that the server is urgently awaiting!");};
var selected_r = -1;
var selected_c = -1;

var rack = ["R","S","T","L","N","E","X"];

var current_squares = [];
var current_letters = [];

function update_selection(r,c) {
  if (selected_r != -1) $("#row-"+selected_r+"-col-"+selected_c).removeClass("selected");
  selected_r = r;
  selected_c = c;
  if (selected_r != -1) $("#row-"+selected_r+"-col-"+selected_c).addClass("selected");
}

function play_tile(event) {
  if (selected_r == -1) return;
  var l = String.fromCharCode(event.keyCode || event.which).toUpperCase();
  i = current_squares.indexOf(""+selected_r+","+selected_c);
  if (i > -1) {
      current_squares.splice(i,1);
      ll = current_letters[i];
      current_letters.splice(i,1);
      add_to_rack(ll);
      $("#row-"+selected_r+"-col-"+selected_c + " div.tile").text("");
      $("#row-"+selected_r+"-col-"+selected_c).removeClass("current-play");
  }
  if (l != ' ') {
    if (rack.indexOf(l) > -1) {
      take_from_rack(l);
      $("#row-"+selected_r+"-col-"+selected_c + " div.tile").text(l);
      $("#row-"+selected_r+"-col-"+selected_c).addClass("current-play");
      current_squares.push(""+selected_r+","+selected_c);
      update_selection(-1,-1);
      current_letters.push(l);
    }
  }
}

function take_from_rack(l) {
  rack.splice(rack.indexOf(l),1);
  $("#scrabble-rack .rack-letter-" + l).first().remove();
}

function add_to_rack(l) {
  rack.push(l);
  $("#scrabble-rack tr").append("<td class='rack-letter-" + l + "'><div class='tile'>"+l+"</div></td>");
}

function do_play() {
  socket.send(JSON.stringify({'squares':current_squares,'letters':current_letters}));
}

document.addEventListener('keypress',play_tile);
