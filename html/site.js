var selected_id = null;
var raw_data = null;

function InitializeHeightSlider(min_height, max_height) {
  $("#height-slider-range").slider({
    range: true,
    min: min_height,
    max: max_height,
    values: [min_height, max_height],
    slide: function(event, ui) {
      console.log(JSON.toString(event));
      var min_height_obj = InchesToHeightObj(parseInt(ui.values[0]));
      var max_height_obj = InchesToHeightObj(parseInt(ui.values[1]));
      $("#height").html(HeightStringFromInt(parseInt(ui.values[0])) +
          " - " + HeightStringFromInt(parseInt(ui.values[1])));
    },
    stop: function(event, ui) {
      console.log("Slider stopped.");
      // TODO: need to refresh the stuff at this time
    }
  });
  // TODO: set the initial values
  $("#height").html(HeightStringFromInt(parseInt($( "#height-slider-range").slider("values", 0))) +
    " - " + HeightStringFromInt(parseInt($("#height-slider-range").slider("values", 1))));
}

function InitializeWeightSlider(min_weight, max_weight) {
  $("#weight-slider-range").slider({
    range: true,
    min: min_weight,
    max: max_weight,
    values: [min_weight, max_weight],
    slide: function(event, ui) {
      $("#weight").val(ui.values[0] + " lbs to " + ui.values[1] + " lbs");
    }
  });
  $("#weight").val($( "#weight-slider-range").slider("values", 0) +
    " lbs to " + $("#weight-slider-range").slider("values", 1) + " lbs");
}

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

function InchesToHeightObj(height_in){
  var feet = Math.floor(height_in / 12);
  var inches = height_in % 12;
  return {'feet': feet, 'inches': inches};
}

function HeightStringFromInt(height_in){
  var height_obj = InchesToHeightObj(height_in);
  return height_obj.feet.toString() + '&#39;' + height_obj.inches.toString()
}

function GetStringTitle(current){
  // TODO: check to see the previous weight is valid
  var previous_weight = current.previous_weight_lbs;
  var current_weight = current.current_weight_lbs;

  return (HeightStringFromInt(current.height_in) + ' / ' +
      previous_weight.toString() + ' lbs &rarr; ' + current_weight.toString() + ' lbs');
}

$(document).ready(function(){

  $( "#image-list-group" ).empty();

  $('.btn-group').button();


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
    raw_data = data.result;
    // console.log(result);

    for (var i = 0; i < raw_data.length; i++) {
      // console.log(result[i].id);
      var current = raw_data[i];
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

    // Figure out the min and max heights and weights using cross filter

    var submissions = crossfilter(raw_data);
    var submissionsByHeight = submissions.dimension(function(d) { return d.height_in; });
    // TODO: assumption that there was a result (because we are dereferencing [0]
    var topHeight = submissionsByHeight.top(1)[0].height_in;
    var bottomHeight = submissionsByHeight.bottom(1)[0].height_in;
    console.log('top height: ' + topHeight + ' bottom height: ' + bottomHeight);

    // TODO: deal with case when there is no Previous weight...?
    var submissionsByPreviousWeight = submissions.dimension(function(d) { return d.previous_weight_lbs; });
    var submissionsByCurrentWeight = submissions.dimension(function(d) { return d.current_weight_lbs; });

    var topPreviousWeight = submissionsByPreviousWeight.top(1)[0].previous_weight_lbs;
    var topCurrentWeight = submissionsByCurrentWeight.top(1)[0].current_weight_lbs;

    var bottomPreviousWeight = submissionsByPreviousWeight.bottom(1)[0].previous_weight_lbs;
    var bottomCurrentWeight = submissionsByCurrentWeight.bottom(1)[0].current_weight_lbs;

    var topWeight = Math.max(topPreviousWeight, topCurrentWeight);
    var bottomWeight = Math.min(bottomPreviousWeight, bottomCurrentWeight);



    // var min_height = ;

    InitializeHeightSlider(bottomHeight, topHeight);
    InitializeWeightSlider(bottomWeight, topWeight);




  });


});