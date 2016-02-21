var listView = null;
// var compiled = _.template('<span><img class="lazy-img" data-original="${image_url}" height="400" width="400" /></span><br/>');
var columns = null;
var nextIndexForPhoto = 0;
var raw_data = null;
var filtered_submissions = null;

var imageWidth = 400;
var columnBorderWidth = 20;  // border on each side of a column

var compiledImageEntryTemplate =  _.template($('#image-entry-template').html());

var global_gender_is_female = null;
var global_units_imperial = true;

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

function HeightStringFromInt(height_in){
    if (global_units_imperial) {
        var height_obj = InchesToHeightObj(height_in);
        return height_obj.feet.toString() + '&#39;' + height_obj.inches.toString();
    } else {
        return InchesToCm(height_in).toFixed(1).toString() + ' cm';
    }
}

function WeightStringFromWeight(weight_lbs){
    if (global_units_imperial) {
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
    console.log('$a: ' + $a.prop('outerHTML'));
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
    console.log('openLightBox called with index = ' + index);
    destroyLightBox();

    // Build lightbox
    $lg = $("#lightgallery");
    // var $first_image = $("<img>", {id: 'first_image', src: ''});
    // var html = '<a href="http://imgur.com/old22m.jpg" id="first_image"> <img src=" /> </a> <a href="http://imgur.com/W0BpBm.jpg"> <img src="http://imgur.com/W0BpBm.jpg" /> </a>';

    var current = raw_data[index];
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
        if (nextIndexForPhoto > raw_data.length) {
            // TODO - I need to handle this case better so it doesn't get here.
            // Best I can do for now.
            return;
        }

        // console.log(JSON.stringify(raw_data[i]));
        var current = raw_data[nextIndexForPhoto];

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
        //var previous_weight = WeightStringFromWeight(current.previous_weight);
        //var current_weight = WeightStringFromWeight(current.current_weight);
        var html = compiledImageEntryTemplate({'title': title, 'index': nextIndexForPhoto, 'image_url': image_url_medium, 'image_height': image_height, 'image_width': imageWidth});
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


function resetBoxes(){
    // Function that is called when any of the filtering or options are set.
    // Set the slider min and max

    var submissions = crossfilter(raw_data);

    // Filter by gender
    var submissionsByGender = submissions.dimension(function(s) { return s.gender; });
    submissionsByGender.filter(global_gender_is_female);

    // Filter by sfw / nsfw
    /*
     var submissionsByNSFW = submissions.dimension(function(s) { return s.adult_content; });
     if (global_nsfw_checked == false){
     // Only one is set (not both or none)
     // we only filter if one of the variables is not true
     submissionsByNSFW.filter(false);
     }
     */

    /*
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
    */

}

function drawMoreBoxes(){
    var LIMIT = 10;  // Just for testing. Number of rows to draw
    for (var i = 0; i < LIMIT; i ++ ) {
        row();
    }
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

            resetBoxes();
            drawMoreBoxes();


            // Now that everything is added, NOW call the layout method
            // layoutGrid()

        }
    });
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
    console.log('hello!');
    // var $el = $('#my-infinite-container');

    // TODO - set gender and english radio
    //$('input:radio[name="gender_radio"]').filter('[value="female"]').attr('checked', true);
    //$('input:radio[name="units_radio"]').filter('[value="english"]').attr('checked', true);
    global_gender_is_female = true;
    $('input:radio[name=gender_radio]')[1].checked = true;  // select Female by default
    $('input:radio[name=units_radio]')[0].checked = true;  // select english by default

    $("input[name='gender_radio']").change(function() {
        console.log("gender_radio changed");
    });

    $("input[name='units_radio']").change(function() {
        console.log("units_radio changed");
    });

    // TODO - set up Slider
    rangeSliderWeight = document.getElementById('slider-range-weight');

    noUiSlider.create(rangeSliderWeight, {
        start: [ 100],
        step: 1,
        range: {
            'min': [  100 ],
            'max': [ 550 ],
        }
    });
    rangeSliderWeight.noUiSlider.on('update', function( values, handle ) {
        // console.log('values: ' + values);
        // $('#selected_weight').val(values[0]);
        var rangeSliderValueElement = document.getElementById('selected_weight');
        rangeSliderValueElement.innerHTML = values[handle];
        // rangeSliderValueElement.innerHTML = values[handle];
    });


    // Height
    rangeSliderHeight = document.getElementById('slider-range-height');

    noUiSlider.create(rangeSliderHeight, {
        start: [ 48,  96],
        step: 1,
        connect: true,
        range: {
            'min': [  48 ],
            'max': [ 96 ]
        }
    });
    rangeSliderHeight.noUiSlider.on('update', function( values, handle ) {
        // console.log('values: ' + values);
        // $('#selected_weight').val(values[0]);
        var rangeSliderValueElement = document.getElementById('selected_height');
        rangeSliderValueElement.innerHTML = values[handle];
        // rangeSliderValueElement.innerHTML = values[handle];
    });

    rangeSliderWeight.noUiSlider.updateOptions({
        range: {
            'min': 50,
            'max': 200
        }
    });


    // TODO - assert
    console.log('windowWidth: ' + $( window ).width());
    // console.log('documentWidth: ' + $( document ).width());

    var num_columns = Math.max(1, Math.floor($(window).width() / (imageWidth + 2 * columnBorderWidth)));
    // var num_columns = 2;
    console.log('num_columns: ' + num_columns);
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
    // var spinner = $('#spinner-div');


    var spinnerTemplate = _.template($('#spinner-template').html());
    var spinner = $(spinnerTemplate());
    spinner.insertAfter($('#container'));
    // spinner.insertAfter($('#demo').closest('.row'));



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






