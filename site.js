var selected_id = null;
var raw_data = null;

var slider = null;
var slider_settings = {
    pagerCustom: '#bx-pager'
  };

var global_gender_is_female = null;
var global_nsfw_checked = null;
// var global_sfw_checked = null;
var global_min_height = null;
var global_max_height = null;
var global_min_weight = null;
var global_max_weight = null;

var global_current_submission_id = null;

var global_units_imperial = true;

function MergeSecondArrayIntoFirst(first, second){
  // Helper function which adds the submission entries which appear in second
  // but not in first, into first
  var used_ids = {};
  for (var i = 0; i < first.length; i++){
    var obj = first[i];
    used_ids[obj.id] = true;
  }

  for (var i = 0; i < second.length; i++){
    var obj = second[i];
    if (!(obj.id in used_ids)){
      first.push(obj);
    }
  }
  return;
}

function GetSubmissionWithId(submission_id){
  // iterate through raw_data and return submission with id
  // this function is EXTREMELY ineffecient. Need to use a
  // hash_map like datastructure of look-up based on id op's
  for (var i = 0; i < raw_data.length; i++){
    var submission = raw_data[i];
    if (submission.id == submission_id){
      return submission;
    }
  }
  // This should never ever happen
  return null;
}

function LoadSubmission(submission_id){
  var submission = GetSubmissionWithId(submission_id);

  if (!submission){
    // Incase an invalid tag was supplied
    return;
  }


  // alert("Loaded submission with title: " + submission.title);
  var html_content = "<b>" + submission.title + "</b> <sup><a href='"+ submission.permalink +"' target='_blank'>[LINK]</a></sup><br/><br/>";

  /*
  if (submission.url) {
    html_content += '<a href="' + submission.url + '">' + submission.url + "</a><br/><br/>" ;
  }
  */

  $("#submission_content").html(html_content);

  if (submission.media_json){
    // submission_image_content
    var image_content_html = "";

    // TODO: I just need to fetch all the images from an Imgur album and use on standard
    // image viewer
    /*
    if ('imgur_albums' in submission.media_json && submission.media_json.imgur_albums){
      // TODO: only using the first album url....
      var album_url = submission.media_json.imgur_albums[0];
      // TODO: I think there shouldn't be a trailing slash for albums because the regex will not match a trailing
      // slash
      image_content_html += '<iframe class="imgur-album" width="100%" height="550" frameborder="0" src="'+album_url+'/embed"></iframe> <br/><br/>';


    }
    */

    var image_thumbnails_html = "";

    if ('imgur_images' in submission.media_json && submission.media_json.imgur_images) {

      for (var i = 0; i < submission.media_json.imgur_images.length; i++) {

        // get the large thumbnail
        var image_url = submission.media_json.imgur_images[i];
        // image_url = image_url.substr(0, image_url.length-4);
        var image_url_large = image_url + "l.jpg"
        var image_url_small = image_url + "s.jpg"
        // <li><img src="http://i.imgur.com/J7NnmFB.jpg" /></li>
        console.log("large image: " + image_url_large);

        // image_content_html += '<img src="'+ image_url + '"> <br/><br/>';
        image_content_html += '<li><img src="' + image_url_large + '" /></li>';
        // <a data-slide-index="0" href=""><img src="http://i.imgur.com/J7NnmFBs.jpg" /></a>
        image_thumbnails_html += '<a data-slide-index="' + i.toString() + '" href=""><img src="' + image_url_small + '" /></a>&nbsp;';

      }
      console.log("Image content html: " + image_content_html);
    }

    /*
    if (!($("#bx-image-slider").length)) {
      console.log('#bx-image-slider exists');
      $("#bx-image").append( $( "h2" ) );
    }
    if (!($("#bx-pager").length)) {
      console.log('#bx-pager exists');
    }
    */

    $("#bx-image-slider-container").html('<ul id="bx-image-slider" class="bxslider"></ul>');
    $("#bx-pager-container").html('<div id="bx-pager"></div>');

    // bx-image-slider-container

    $("#bx-image-slider").html(image_content_html);
    // console.log("#bx-image-slider value: " + $("#bx-image-slider").val());

    if (submission.media_json.imgur_images.length <= 1) {
      // Don't show thumbnails if there are none to show
      image_thumbnails_html = "";
    }

    $("#bx-pager").html(image_thumbnails_html);
    // console.log("#bx-pager value: " + $("#bx-pager").val());

    // slider.reloadSlider(slider_settings);
    slider = $('.bxslider').bxSlider(slider_settings);


  }

  // Set the window hash now that we know the submission_id is valid
  global_current_submission_id = submission_id;
  window.location.hash = submission_id;
  
  /*
  if (submission.media_embed_json){
    // html_content += "MEDIA_EMBED_JSON: " + submission.media_embed_json;
    var decoded = $('<div/>').html(submission.media_embed_json.content).text();
    // console.log('DECODED' + decoded);
    html_content += "MEDIA_EMBED" + decoded;
    // console.log('embed:' + JSON.stringify(submission.media_embed_json));
  }
  if (submission.media_json){
    html_content += "MEDIA_JSON: " + JSON.toString(submission.media_json);
    // console.log('media:' + JSON.stringify(submission.media_json));
  }
  */

  // if submission.media


}

function InitializeHeightSlider() {
  $("#height-slider-range").slider({
    range: true,
    min: global_min_height,
    max: global_max_height,
    values: [global_min_height, global_max_height],
    slide: function(event, ui) {
      // console.log(JSON.toString(event));
      var min_height_obj = InchesToHeightObj(parseInt(ui.values[0]));
      var max_height_obj = InchesToHeightObj(parseInt(ui.values[1]));
      $("#height").html(HeightStringFromInt(parseInt(ui.values[0])) +
          " - " + HeightStringFromInt(parseInt(ui.values[1])));
    },
    stop: function(event, ui) {
      // console.log("Slider stopped.");
      global_min_height = parseInt(ui.values[0]);
      global_max_height = parseInt(ui.values[1]);
      UpdateTable();
      // TODO: need to refresh the stuff at this time
    }
  });
  // TODO: set the initial values
  $("#height").html(HeightStringFromInt(parseInt($( "#height-slider-range").slider("values", 0))) +
    " - " + HeightStringFromInt(parseInt($("#height-slider-range").slider("values", 1))));
}

function InitializeWeightSlider() {
  $("#weight-slider-range").slider({
    range: true,
    min: global_min_weight,
    max: global_max_weight,
    values: [global_min_weight, global_max_weight],
    slide: function(event, ui) {
      $("#weight").val(ui.values[0] + " lbs to " + ui.values[1] + " lbs");
    },
    stop: function(event, ui) {
      // console.log("Slider stopped.");
      global_min_weight = parseInt(ui.values[0]);
      global_max_weight = parseInt(ui.values[1]);
      UpdateTable();
      // TODO: need to refresh the stuff at this time
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

  LoadSubmission(selected_id);

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

function UpdateTable(){
  $( "#image-list-group" ).empty();
  // alert("Update Table Called!");

  // $( "input:radio[name=bar]:checked" ).val();
  // TODO: Filter by the global variables here

  var submissions = crossfilter(raw_data);

  // Filter by gender
  var submissionsByGender = submissions.dimension(function(s) { return s.gender; });
  submissionsByGender.filter(global_gender_is_female);



  // Filter by sfw / nsfw
  var submissionsByNSFW = submissions.dimension(function(s) { return s.adult_content; });
  if (global_nsfw_checked == false){
    // Only one is set (not both or none)
    // we only filter if one of the variables is not true
    submissionsByNSFW.filter(false);
  }


  // Filter by height
  var submissionByHeight = submissions.dimension(function(s) {return s.height_in;});
  submissionByHeight.filter([global_min_height, global_max_height + 1]); // TODO: add + Math.MIN_VALUE

  console.log('global min height= ' + global_min_height);
  console.log('global max height= ' + global_max_height);

  // Filter by weight
  var submissionByCurrentWeight = submissions.dimension(function(s) {return s.current_weight_lbs;});
  submissionByCurrentWeight.filter([global_min_weight, global_max_weight + 1]);

  var unsorted_results = submissionByCurrentWeight.top(Infinity);

  submissionByCurrentWeight.filterAll(); // Need to clear that filter

  var submissionByPreviousWeight = submissions.dimension(function(s) {return s.previous_weight_lbs;});
  submissionByPreviousWeight.filter([global_min_weight, global_max_weight + 1]);

  var secondary_results = submissionByPreviousWeight.top(Infinity);

  MergeSecondArrayIntoFirst(unsorted_results, secondary_results);

  // Create another crossfilter for this data to sort it by the score
  var cf2 = crossfilter(unsorted_results);
  var submissionByScore = cf2.dimension(function(s) {return s.score;});
  var results = submissionByScore.top(Infinity);


  // var results = secondary_results;
  // Score dimension
  //

  //


  for (var i = 0; i < results.length; i++) {
    // console.log(result[i].id);
    var current = results[i];
    $( "#image-list-group" ).append(
      '<a href="#" class="list-group-item" id="'+ 'list_' + current.id + '">' +
      '<h5 class="list-group-item-heading">' + GetStringTitle(current) + '</h5>'+
      '<p class="list-group-item-text">'+ current.title + '</p>' +
      '</a>');

    // alert(result[i]);
    //Do something
  }

  $ ( "#number_of_results").html(results.length.toString());
}

function updateResultsSize(){
  console.log("updateResultsSize");
  // TODO: change the height of the DIV
  var other_content_height = 300;  // height of other content on page
  var minimum_results_height = 400;
  var results_height = Math.max(minimum_results_height, $(window).height() - other_content_height);
  $("#image-list-group").height(results_height);
}

function setGender(gender_str) {
  if (gender_str == "male") {
    $("#gender_logo_span").html('<i class="fa fa-male" style="color:#2B6BF6;"></i>');
  } else if (gender_str == "female") {
    $("#gender_logo_span").html('<i class="fa fa-female" style="color:#FE2EC8;"></i>');
    // $("#height-slider-range").children("div").css("background","#FE2EC8");
  }

}

function setUnits() {
  console.log("Setting units to: " + global_units_imperial);
  InitializeHeightSlider(2,10);
}

$(document).ready(function(){

  setGender("female");  // default gender selection

  global_units_imperial = true;

  updateResultsSize();
  $(window).resize(function() {
      updateResultsSize();
  });

  $(window).on('hashchange', function() {
    console.log("hashchange!");
    if (global_current_submission_id){
      window.location.hash = global_current_submission_id;
    }
    // .. work ..
  });

  // Default Global variables:
  global_gender_is_female = true; // because that is selected by default
  global_nsfw_checked = false; // same as above and below
  //  global_sfw_checked = true; // because that is selected by default

  // $( "#image-list-group" ).empty();

  $('.btn-group').button();

  // slider = $('.bxslider').bxSlider(slider_settings);

  $("input[name=gender_radio]:radio").change(function () {
    // TODO: optimization - even if the same option is selected again, this
    // function gets called
    // alert("Radio button changed.");

    var gender_str = $("input:radio[name=gender_radio]:checked").val();
    if (gender_str == "male"){
      console.log("Male is checked.");
      global_gender_is_female = false;
      setGender("male");
    } else {
      console.log("Female is checked.");
      global_gender_is_female = true;
      setGender("female");
    }

    UpdateTable();
  });

  $("input[name=units_radio]:radio").change(function () {
    // TODO: optimization - even if the same option is selected again, this
    // function gets called
    // alert("Radio button changed.");

    var units_str = $("input:radio[name=units_radio]:checked").val();
    if (units_str == "imperial"){
      console.log("Imperial is checked.");
      global_units_imperial = true;
      // setGender("male");
    } else {
      console.log("Metric is checked.");
      global_units_imperial = false;
      // setGender("female");
    }
    setUnits();

    // UpdateTable();
  });


  $("#nsfw_checkbox").change(function(){
    // alert("NSFW checkboxes changed.");
    if ($('#nsfw_checkbox').prop('checked')){
      global_nsfw_checked = true;
      // alert("Clothed is checked");
    } else {
      global_nsfw_checked = false;
    }
    UpdateTable();
  });


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

    // If there is a hashtag, load the appropriate submission:
    //
    var hash = window.location.hash;
    if (hash) {
      hash = hash.substr(1);
      if (hash != "") {
        global_current_submission_id = hash;
        LoadSubmission(hash);
        console.log("If hash is true, hash = " + hash);
      }
    }


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

    global_min_height = bottomHeight;
    global_max_height = topHeight;
    InitializeHeightSlider();

    global_min_weight = bottomWeight;
    global_max_weight = topWeight;
    InitializeWeightSlider();

    UpdateTable();



    // selected_id = IdFromHTMLId($("#image-list-group a:first-child").attr('id'));
    // The first element

    // $("#image-list-group a:first-child").addClass("active");
    // Select the first element in the table
    var first_html_id = $("#image-list-group a:first-child").attr('id');
    // TODO: uncomment the line below
    // TODO: only execute the line below if there are results to begin with...?(but should be the case)
    // SelectListElement(first_html_id);


  });


});
