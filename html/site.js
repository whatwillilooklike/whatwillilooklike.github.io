var selected_id = null;

function HTMLIdFromHTML(id){
  return "list_" + id;
}

function IdFromHTMLId(html_id){
  return html_id.substr(5);
}

function SelectListElement(html_id){
  // Also unselects the previous element
  if (selected_id) {
    $("#list_" + selected_id).removeClass("active");
  }

  $("#" + html_id).addClass("active");
  selected_id = IdFromHTMLId(html_id);
}

function GetStringTitle(current){
  var feet = Math.floor(current.height_in / 12);
  var inches = current.height_in % 12;
  // TODO: check to see the previous weight is valid
  var previous_weight = current.previous_weight_lbs;
  var current_weight = current.current_weight_lbs;

  return (feet.toString() + '&#39;' + inches.toString() + ' / ' +
      previous_weight.toString() + ' lbs &rarr; ' + current_weight.toString() + ' lbs');
}

$(document).ready(function(){

  $( "#image-list-group" ).empty();

  /*
  $("#image-list-group a").click(function(){
  // $(document).on('click', '.list-group a', function () {
    console.log("selected something.");
    console.log("Selected Option Yaz:"+$(this).text());
  });
  */

  // Keep track of which elements are clicked
  $(document).on('click', '#image-list-group a', function () {
  // $("#image-list-group a").on('click', 'p.test', function() {
    // alert('you clicked a p.test element');
    // console.log("Selected Option Maz:"+$(this).text());
    // console.log("Selected Option Maz:" + $(this).attr('id'));
    SelectListElement($(this).attr('id'))
    // TODO: also change shit
  });

  // alert("Atleast this is working.");
  $.getJSON( "json_dump.json", function( data ) {
    // alert(data);
    var items = [];
    var result = data.result;
    // console.log(result);

    for (var i = 0; i < result.length; i++) {
      // console.log(result[i].id);
      var current = result[i];
      $( "#image-list-group" ).append(
        '<a href="#" class="list-group-item" id="'+ 'list_' + current.id + '">' +
        '<h5 class="list-group-item-heading">' + GetStringTitle(current) + '</h5>'+
        '<p class="list-group-item-text">'+ current.title + '</p>' +
        '</a>');

      // alert(result[i]);
      //Do something
    }

    selected_id = IdFromHTMLId($("#image-list-group a:first-child").attr('id'));
    // The first element

    // $("#image-list-group a:first-child").addClass("active");
    var first_html_id = $("#image-list-group a:first-child").attr('id');
    SelectListElement(first_html_id);
    // selected_id
    // $( "p" ).addClass( "myClass yourClass" );

    /*
    $.each(result, function(obj) {
      console.log(obj['id']);
      // items.push( "<li id='" + key + "'>" + val + "</li>" );
    });
    */


    /*
    $( "<ul/>", {
      "class": "my-new-list",
      html: items.join( "" )
    }).appendTo( "body" );
    */

  });


});