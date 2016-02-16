var listView = null;
// var compiled = _.template('<span><img class="lazy-img" data-original="${image_url}" height="400" width="400" /></span><br/>');

function downloadContent(){
    Papa.parse("csv_dump.csv", {
        download: true,
        dynamicTyping: true,
        header:true,
        skipEmptyLines:true,
        complete: function(results) {

            var LIMIT = 100000;  // Just for testing

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
            for (var i = 0; i < raw_data.length; i++) {
                if (i > LIMIT) {
                    break;
                }
                // console.log(JSON.stringify(raw_data[i]));
                var current = raw_data[i];

                var image_id = current.photos[0];  // we take the first image
                var image_url = 'http://imgur.com/' + image_id

                // image_url = image_url.substr(0, image_url.length-4);
                var image_url_large = image_url + "l.jpg"
                var image_url_medium = image_url + "m.jpg"
                var image_url_small = image_url + "s.jpg"

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
                var html = '<div><img class="lazy-img" data-original="' + image_url_medium + '" height="400" width="400" /></div>';
                listView.append(html);
                // console.log('appending: ' + c);
                // alert(result[i]);
                //Do something
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
    var $el = $('#my-infinite-container');
    listView = new infinity.ListView($el, {
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

    // Lazy load images
    downloadContent();
    // ... When adding new content:



    // var $newContent = $('<p>Hello World</p>');
    // listView.append($newContent);



});
