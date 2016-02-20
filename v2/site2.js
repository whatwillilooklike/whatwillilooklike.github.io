var listView = null;
// var compiled = _.template('<span><img class="lazy-img" data-original="${image_url}" height="400" width="400" /></span><br/>');
var columns = null;
var nextIndexForPhoto = 0;
var raw_data = null;

var imageWidth = 400;
var columnBorderWidth = 20;  // border on each side of a column

function destroyLightBox() {
    $lg = $("#lightgallery");
    if ($lg.data('lightGallery') === undefined) {
        return;
    }
    $lg.data('lightGallery').destroy(true);
    $lg.html('');  // clear html
}

function lightboxImage(image_id, first_image) {
    var image_url = imageUrlForImageID(image_id, 'l');
    var $a = $("<a>", {href: image_url});
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
    destroyLightBox();

    // Build lightbox
    $lg = $("#lightgallery");
    // var $first_image = $("<img>", {id: 'first_image', src: ''});
    // var html = '<a href="http://imgur.com/old22m.jpg" id="first_image"> <img src=" /> </a> <a href="http://imgur.com/W0BpBm.jpg"> <img src="http://imgur.com/W0BpBm.jpg" /> </a>';
    var a = lightboxImage('old22', true);
    var b = lightboxImage('W0BpB', false);
    $lg.append(a);
    $lg.append(b);
    // $lg.html(html);
    $("#lightgallery").lightGallery();

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
            if ($currCol.height() <= $minCol.height()) {
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
        var html = '<div><img onclick="openLightBox('+ nextIndexForPhoto +')" class="lazy-img" data-original="' + image_url_medium + '" height="400" width="400" /></div>';

        // Append it to the column with the lowest height
        $minCol.data('listView').append(html);
        nextIndexForPhoto++;
        // listView.append(html);
        // console.log('appending: ' + c);
        // alert(result[i]);
        //Do something
    }
}

function downloadContent(){
    Papa.parse("csv_dump.csv", {
        download: true,
        dynamicTyping: true,
        header:true,
        skipEmptyLines:true,
        complete: function(results) {

            var LIMIT = 100;  // Just for testing


            // Using JSON
            // raw_data = data.result;
            // var limit = 100;
            // Parse the imgur urls:
            raw_data = results.data;
            // console.log(raw_data);
            for (var i = 0; i < raw_data.length; i++){
                // console.log(raw_data[i]);
                //console.log(typeof raw_data[i].current_weight_lbs)
                //assert(typeof raw_data[i].current_weight_lbs === 'number', 'Error: Weight is not a number');
                raw_data[i]['photos'] = raw_data[i].photos.split(',');
            }


            //
            var all_grid_element_html = [];


            for (var i = 0; i < LIMIT; i ++ ) {
                row();
            }

            // Now that everything is added, NOW call the layout method
            // layoutGrid()

        }
    });
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

    // Lazy load images
    downloadContent();
    // ... When adding new content:



    // var $newContent = $('<p>Hello World</p>');
    // listView.append($newContent);



});
