var listView = null;
// var compiled = _.template('<span><img class="lazy-img" data-original="${image_url}" height="400" width="400" /></span><br/>');
var columns = null;
var nextIndexForPhoto = 0;
var raw_data = null;  // never use raw_data for results. use filtered_submissions
var filtered_submissions = null;

var imageWidth = 400;
var columnBorderWidth = 20;  // border on each side of a column

var compiledImageEntryTemplate =  _.template($('#image-entry-template').html());

// var global_units_imperial = true;

var global_min_weight = null;
var global_max_weight = null;
var global_min_height = null;
var global_max_height = null;

var last_selected_weight = null;
var last_selected_height = null;

var rangeSliderWeight = null;
var rangeSliderHeight = null;

function InchesToHeightObj(height_in){
    var feet = Math.floor(height_in / 12);
    var inches = height_in % 12;
    return {'feet': feet, 'inches': inches};
}

function InchesToCm(height_in) {
    return height_in * 2.54;
}

function UnitsAreImperial() {
    return $("input[name=units_radio]:checked").val() == 'imperial';
}

function HeightStringFromInt(height_in){
    if (UnitsAreImperial()) {
        var height_obj = InchesToHeightObj(height_in);
        return height_obj.feet.toString() + '&#39;' + height_obj.inches.toString();
    } else {
        return InchesToCm(height_in).toFixed(1).toString() + ' cm';
    }
}

function WeightStringFromWeight(weight_lbs){
    if (UnitsAreImperial()) {
        return weight_lbs.toString() + ' lbs';
    } else {
        return (weight_lbs / 2.2).toFixed(1).toString() + ' kg';
    }
}

function GetStringTitle(current){
    // TODO: check to see the previous weight is valid
    var previous_weight = current.previous_weight_lbs;
    var current_weight = current.current_weight_lbs;

    return (HeightStringFromInt(current.height_in) + ' / ' +
    WeightStringFromWeight(previous_weight) + ' &rarr; ' + WeightStringFromWeight(current_weight));
}

function destroyLightBox() {
    $lg = $("#lightgallery");
    if ($lg.data('lightGallery') === undefined) {
        return;
    }
    $lg.data('lightGallery').destroy(true);
    $lg.empty();  // clear html
}

function lightboxImage(image_id, first_image) {
    var image_url = imageUrlForImageID(image_id, 'l');
    var image_url_thumb = imageUrlForImageID(image_id, 's');
    var $a = $("<a>", {href: image_url});
    $a.attr('data-exThumbImage', image_url_thumb);
    // console.log('$a: ' + $a.prop('outerHTML'));
    if (first_image == true) {
        $a.attr('id', 'first_image');
    }
    var $image = $("<img>", {src: image_url});
    $a.append($image);
    return $a;
}

function openLightBox(index) {
    // index is the index in raw_data (TODO - need to rename raw_data)
    // alert('images: ' + JSON.stringify(raw_data[index].photos));

    // Just in case:
    // console.log('openLightBox called with index = ' + index);
    destroyLightBox();

    // Build lightbox
    $lg = $("#lightgallery");
    // var $first_image = $("<img>", {id: 'first_image', src: ''});
    // var html = '<a href="http://imgur.com/old22m.jpg" id="first_image"> <img src=" /> </a> <a href="http://imgur.com/W0BpBm.jpg"> <img src="http://imgur.com/W0BpBm.jpg" /> </a>';

    var current = filtered_submissions[index];
    // var image_id = current.photos[0];
    for (var i = 0; i < current.photos.length; i++) {
        var image_id = current.photos[i];
        var lightBox = lightboxImage(image_id, i == 0);  // so we mark the first image as first_image
        $lg.append(lightBox);
    }
    // $lg.html(html);
    $("#lightgallery").lightGallery({
        'download': false,
        'exThumbImage': 'data-exThumbImage'
    });

    // Launch Lightbox
    $('#first_image').click();

    // We destroy Lightbox on close
    // Hopefully this thing doesn't have memory leaks
    $lg.on('onCloseAfter.lg',function(event){
        // onCloseAfter.lg;
        destroyLightBox();
    });

}

function imageUrlForImageID(image_id, size) {
    // size has to be 's', 'm', or 'l'
    var image_url = 'http://imgur.com/' + image_id + size + '.jpg';
    return image_url;
}

function resetSpinner(){
    $('#spinner-div').html("<img src='spinner.gif' class=spinner alt='Loading...'>");
}

function row() {
    var colIndex, length, $minCol, $currCol;
    for (var i = 0, length = columns.length; i < length; i++) {// for(index = 0, length = columns.length; index < length; index++) {


        // Determine the min column (column with the minimum length)
        // We do this so each column is the same length
        var $minCol = null;
        for(colIndex = 0; colIndex < length; colIndex++) {
            $currCol = $(columns[colIndex]);
            if(!$minCol) $minCol = $currCol;

            // The bug is that the CSS in the HTML makes each column think it's the same height
            if ($currCol.height() < $minCol.height()) {
                $minCol = $currCol;
            }
            //  else $minCol = $minCol.height() > $currCol.height() ? $currCol : $minCol;
        }
        /*
        for(colIndex = 0; colIndex < length; colIndex++) {
            $currCol = $(columns[colIndex]);

            if(!$minCol) $minCol = $currCol;
            else $minCol = $minCol.height() > $currCol.height() ? $currCol : $minCol;
        }
        */

        // If we don't have any more results to show
        if (nextIndexForPhoto >= filtered_submissions.length) {
            // TODO - I need to handle this case better so it doesn't get here.
            // Best I can do for now.
            // TODO - I should display something to tell users there are no more submissions
            $('#spinner-div').html("No more results.");
            return;
        } else {
            // Show spinner
            resetSpinner();


        }

        // console.log(JSON.stringify(raw_data[i]));
        var current = filtered_submissions[nextIndexForPhoto];

        var image_id = current.photos[0];  // we take the first image
        // var image_url = 'http://imgur.com/' + image_id;

        // image_url = image_url.substr(0, image_url.length-4);
        // var image_url_large = image_url + "l.jpg";
        var image_url_medium = imageUrlForImageID(image_id, 'm');
        var image_url_small = imageUrlForImageID(image_id, 's');

        // TODO - use something cleaner like strcat
        var gender_string = "";
        if (current.gender == true) {
            gender_string = 'female';
        } else {
            gender_string = 'male';
        }




        // all_grid_element_html.push(grid_elemen);
        // all_grid_element_html = all_grid_element_html + grid_element_html;
        // var html = compiled({'image_url': image_url_medium});
        var image_height = Math.round(imageWidth / current.first_image_aspect_ratio);
        // var height = 400;
        var title = GetStringTitle(current);
        var previous_weight_str = WeightStringFromWeight(current.previous_weight_lbs);
        var current_weight_str = WeightStringFromWeight(current.current_weight_lbs);
        // console.log('previous_weight_str: ' + previous_weight_str);
        var height_str = HeightStringFromInt(current.height_in);
        // console.log(JSON.stringify(current));
        var html = compiledImageEntryTemplate({'submission_id': current.id, 'height_str': height_str, 'previous_weight_str': previous_weight_str, 'current_weight_str': current_weight_str, 'index': nextIndexForPhoto, 'image_url': image_url_medium, 'image_height': image_height, 'image_width': imageWidth});
        // var html = '<div><img onclick="openLightBox('+ nextIndexForPhoto +')" class="lazy-img" data-original="' + image_url_medium + '" height="'+ height +'" width="' + imageWidth + '" /></div>';

        // Append it to the column with the lowest height
        $minCol.data('listView').append(html);
        nextIndexForPhoto++;
        // listView.append(html);
        // console.log('appending: ' + c);
        // alert(result[i]);
        //Do something
    }
}

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

function isGenderFemale(){
    // Return value of radio == female
    return $("input[name=gender_radio]:checked").val() == 'female';
}

function resetBoxes(){
    // Function that is called when any of the filtering or options are set.
    resetSpinner();

    //console.log('resetBoxes called!');
    // Reset Columns Views
    // columns = $('.infinite');

    if (columns !== null) {
        console.log('resetting ' + columns.length  +'columns');
        columns.each(function() {
            // remove
            $(this).data('listView').remove();
        });
    }


    //console.log('windowWidth: ' + $( window ).width());
    // console.log('documentWidth: ' + $( document ).width());

    var num_columns = Math.max(1, Math.floor($(window).width() / (imageWidth + 2 * columnBorderWidth)));
    // var num_columns = 2;
    //console.log('num_columns: ' + num_columns);
    $('#float-wrap').html('');  // Clear the container for the infinite columns
    for (var i = 0; i < num_columns; i++) {
        var $div = $("<div>", {class: "infinite infinite-scroll-column"});
        $div.css('border-left-width', columnBorderWidth);
        $div.css('border-right-width', columnBorderWidth);
        // var html = '<div class="infinite infinite-scroll-column"></div>';
        $('#float-wrap').append($div);
    }


    columns = $('.infinite');
    console.assert(columns.length > 0, "No columns present!");

    columns.each(function() {
        listView = new infinity.ListView($(this), {
            lazy: function(){
                $(this).find('.lazy-img').each(function() {
                    var $ref = $(this);
                    $ref.attr('src', $ref.attr('data-original'));
                });
                // console.log('elem data: ' + getMethods(elem));
                // console.log('elem attr: ' + elem.getAttribute('data-original'));
                // $(elem).attr('src', $(elem).attr('data-original'));}
            }
        });
        $(this).data('listView', listView);
    });

    // We reset the index since we're resetting the boxes
    nextIndexForPhoto = 0;







    console.assert(raw_data !== null, "No data present!");
    var submissions = crossfilter(raw_data);

    // Filter by gender
    var submissionsByGender = submissions.dimension(function(s) { return s.gender; });
    submissionsByGender.filter(isGenderFemale());

    // Filter by sfw / nsfw
    /*
     var submissionsByNSFW = submissions.dimension(function(s) { return s.adult_content; });
     if (global_nsfw_checked == false){
     // Only one is set (not both or none)
     // we only filter if one of the variables is not true
     submissionsByNSFW.filter(false);
     }
     */
    // filtered_submissions = submissionsByGender.top(Infinity);




    // Filter by height
    // TODO - height filtering isn't working.
    // See what I did in the other code

    // var submissionByHeight = submissions.dimension(function(s) {return s.height_in;});
    var submissionsByHeight = submissions.dimension(function(d) { return d.height_in; });


    var currentSelectedHeight = rangeSliderHeight.noUiSlider.get();
    var heightApproxRatio = 0.01;
    var minHeight = Math.floor(currentSelectedHeight * (1 - heightApproxRatio));
    var maxHeight = Math.round(currentSelectedHeight * (1 + heightApproxRatio));

    submissionsByHeight.filter([minHeight, maxHeight]); // TODO: add + Math.MIN_VALUE

    //console.log('submissionsByHeight: ' + JSON.stringify(submissionsByHeight.top(20)));

    //console.log('for filtering -- min height= ' + minHeight);
    //console.log('for filtering -- max height= ' + maxHeight);




    // Filter by weight
    // var approxRatio = 0.03;
    var submissionByCurrentWeight = submissions.dimension(function(s) {return s.current_weight_lbs;});
    var submissionByPreviousWeight = submissions.dimension(function(s) {return s.previous_weight_lbs;});


    var weightMargin = 5;
    var selectedWeight = rangeSliderWeight.noUiSlider.get();
    var selectedTopWeight = Math.round(selectedWeight + weightMargin);
    var selectedBottomWeight = Math.round(selectedWeight - weightMargin);

    submissionByCurrentWeight.filter([selectedBottomWeight, selectedTopWeight + 1]);

    var unsorted_results = submissionByCurrentWeight.top(Infinity);

    submissionByCurrentWeight.filterAll(); // Need to clear that filter

    submissionByPreviousWeight.filter([selectedBottomWeight, selectedTopWeight + 1]);

    var secondary_results = submissionByPreviousWeight.top(Infinity);

    MergeSecondArrayIntoFirst(unsorted_results, secondary_results);

    // Create another crossfilter for this data to sort it by the score
    var cf2 = crossfilter(unsorted_results);
    var submissionByScore = cf2.dimension(function(s) {return s.score;});
    filtered_submissions = submissionByScore.top(Infinity);



}

function drawMoreBoxes(){
    var LIMIT = 10;  // Just for testing. Number of rows to draw
    for (var i = 0; i < LIMIT; i ++ ) {
        row();
    }
}

function round5(x)
{
    return Math.round(x/5)*5;
}

function downloadContent(){
    Papa.parse("csv_dump.csv", {
        download: true,
        dynamicTyping: true,
        header:true,
        skipEmptyLines:true,
        complete: function(results) {
            raw_data = results.data;




            // Using JSON
            // raw_data = data.result;
            // var limit = 100;
            // Parse the imgur urls:

            // console.log(raw_data);
            for (var i = 0; i < raw_data.length; i++){
                // console.log(raw_data[i]);
                //console.log(typeof raw_data[i].current_weight_lbs)
                //assert(typeof raw_data[i].current_weight_lbs === 'number', 'Error: Weight is not a number');
                raw_data[i]['photos'] = raw_data[i].photos.split(',');
            }

            var submissions = crossfilter(raw_data);
            var submissionByCurrentWeight = submissions.dimension(function(s) {return s.current_weight_lbs;});
            var submissionByPreviousWeight = submissions.dimension(function(s) {return s.previous_weight_lbs;});
            // Get the top weight
            var topPreviousWeight = submissionByPreviousWeight.top(1)[0].previous_weight_lbs;
            var topCurrentWeight = submissionByCurrentWeight.top(1)[0].current_weight_lbs;

            var bottomPreviousWeight = submissionByPreviousWeight.bottom(1)[0].previous_weight_lbs;
            var bottomCurrentWeight = submissionByCurrentWeight.bottom(1)[0].current_weight_lbs;

            var submissionsByHeight = submissions.dimension(function(d) { return d.height_in; });
            // TODO: assumption that there was a result (because we are dereferencing [0]

            global_max_height = submissionsByHeight.top(1)[0].height_in;
            global_min_height = submissionsByHeight.bottom(1)[0].height_in;

            global_max_weight = Math.max(topPreviousWeight, topCurrentWeight);
            global_min_weight = Math.min(bottomPreviousWeight, bottomCurrentWeight);
            //console.log('global_min_weight: ' + global_min_weight);
            //console.log('global_max_weight: ' + global_max_weight);


            // TODO - set up Slider
            rangeSliderWeight = document.getElementById('slider-range-weight');

            noUiSlider.create(rangeSliderWeight, {
                start: [135],  // TODO - currently arbitrary default weight
                step: 5,
                range: {
                    'min': [ round5(global_min_weight)  ],
                    'max': [ round5(global_max_weight) ],
                    '70%': [250], // Hack for now
                    '90%': [400]
                }
            });


            rangeSliderWeight.noUiSlider.on('update', function( values, handle ) {
                // console.log('values: ' + values);
                // $('#selected_weight').val(values[0]);
                updateWeightDiv(Math.floor(values[handle]))
                // rangeSliderValueElement.innerHTML = values[handle];

            });


            rangeSliderWeight.noUiSlider.on('set', function( values, handle ) {
                var selectedWeight = values[handle];
                // console.log('selectedWeight: ' + selectedWeight);
                if (selectedWeight != last_selected_weight) {
                    last_selected_weight = selectedWeight;
                    resetBoxes();
                    drawMoreBoxes();
                }

            });



            // Height
            rangeSliderHeight = document.getElementById('slider-range-height');

            // TODO - set the real height
            noUiSlider.create(rangeSliderHeight, {
                start: [ 64],  // TODO -currently arbitrarily default height
                step: 1,
                range: {
                    'min': [  global_min_height ],
                    'max': [ global_max_height ],
                }
            });
            rangeSliderHeight.noUiSlider.on('update', function( values, handle ) {
                // console.log('values: ' + values);
                // $('#selected_weight').val(values[0]);
                updateHeightDiv(values[handle]);
                // rangeSliderValueElement.innerHTML = values[handle];

            });

            rangeSliderHeight.noUiSlider.on('set', function( values, handle ) {
                var selectedHeight = values[handle];
                // console.log('selectedHeight: ' + selectedHeight);
                if (selectedHeight != last_selected_height) {
                    last_selected_height = selectedHeight;
                    resetBoxes();
                    drawMoreBoxes();
                }
            });

            // Now that everything is added, NOW call the layout method
            resetBoxes();
            drawMoreBoxes();
            // layoutGrid()

        }
    });
}

function updateHeightDiv(height_in) {
    var rangeSliderValueElement = document.getElementById('selected_height');
    rangeSliderValueElement.innerHTML = HeightStringFromInt(height_in);
}

function updateWeightDiv(weight_lbs) {
    var rangeSliderValueElement = document.getElementById('selected_weight');
    rangeSliderValueElement.innerHTML = WeightStringFromWeight(weight_lbs);
}

function onscreen($el) {
    var viewportBottom = $(window).scrollTop() + $(window).height();
    return $el.offset().top <= viewportBottom;
}

function getMethods(obj) {
    var result = [];
    for (var id in obj) {
        try {
            if (typeof(obj[id]) == "function") {
                result.push(id + ": " + obj[id].toString());
            }
        } catch (err) {
            result.push(id + ": inaccessible");
        }
    }
    return result;
}

$(document).ready(function() {
    // console.log('hello!');
    // var $el = $('#my-infinite-container');

    // TODO - set gender and english radio
    //$('input:radio[name="gender_radio"]').filter('[value="female"]').attr('checked', true);
    //$('input:radio[name="units_radio"]').filter('[value="english"]').attr('checked', true);
    $('input:radio[name=gender_radio]')[1].checked = true;  // select Female by default
    $('input:radio[name=units_radio]')[0].checked = true;  // select english by default

    $("input[name='gender_radio']").change(function() {
        // console.log("gender_radio changed");
        resetBoxes();
        drawMoreBoxes();
        // rangeSliderHeight.noUiSlider.fireEvent('update');
        // rangeSliderHeight.noUiSlider.set(l;
        // rangeSliderHeight.noUiSlider.set(last_selected_height);
    });

    $("input[name='units_radio']").change(function() {
        // console.log("units_radio changed");
        updateHeightDiv(Math.floor(rangeSliderHeight.noUiSlider.get()));
        updateWeightDiv(Math.floor(rangeSliderWeight.noUiSlider.get()));
        resetBoxes();
        drawMoreBoxes();
        // TODO - need to refresh the whole table to support this
         // rangeSliderHeight.noUiSlider.dispatchEvent('update');
        // rangeSliderHeight.no
        // rangeSliderHeight.noUiSlider.set(last_selected_height);
    });








    /*
    columns.each(function() {
        var listView = new ListView($(this), {
            lazy: function() {
                $(this).find('.pug').each(function() {
                    var $ref = $(this);
                    $ref.attr('src', $ref.attr('data-original'));
                });
            }
        });
        $(this).data('listView', listView);
    });
    */

    // var spinner = $(spinnerTemplate());
    downloadContent();


    var updateScheduled = false;
    var spinner = $('#spinner-div');


    /*
    var spinnerTemplate = _.template($('#spinner-template').html());
    var spinner = $(spinnerTemplate());
    spinner.insertAfter($('#container'));
    // spinner.insertAfter($('#demo').closest('.row'));
    */


    $(window).on('scroll', function() {
        if(!updateScheduled) {
            setTimeout(function() {
                if(onscreen(spinner)) drawMoreBoxes();
                updateScheduled = false;
            }, 500);
            updateScheduled = true;
        }
    });


    // Lazy load images
    // downloadContent();
    // ... When adding new content:



    // var $newContent = $('<p>Hello World</p>');
    // listView.append($newContent);



});






