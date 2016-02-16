var raw_data = null;

// http://stackoverflow.com/questions/610406/javascript-equivalent-to-printf-string-format
// First, checks if it isn't implemented yet.
if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined'
                ? args[number]
                : match
                ;
        });
    };
}

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

                var grid_element_html = '<div class="grid-item {0}"><img src="grey.gif" height="400" width="400" data-original="{1}" alt="TODO" /></div>'.format(gender_string, image_url_medium);
                all_grid_element_html.push(grid_element_html);
                // all_grid_element_html = all_grid_element_html + grid_element_html;

                // alert(result[i]);
                //Do something
            }
            $( "#container" ).html(all_grid_element_html.join('\n'));
            // Now that everything is added, NOW call the layout method
            layoutGrid();

        }
    });
}

function layoutGrid() {
    var $win = $(window),
        $imgs = $("img"),
        $con = $('#container').isotope({
            masonry: {
                columnWidth: 50,
                gutter: 10
            }
        });

    function loadVisible($els, trigger) {
        $els.filter(function () {
            var rect = this.getBoundingClientRect();
            return rect.top >= 0 && rect.top <= window.innerHeight;
        }).trigger(trigger);
    }

    $con.isotope('on', 'layoutComplete', function () {
        loadVisible($imgs, 'lazylazy');
    });

    $win.on('scroll', function () {
        loadVisible($imgs, 'lazylazy');
    });

    $imgs.lazyload({
        effect: "fadeIn",
        failure_limit: Math.max($imgs.length - 1, 0),
        event: 'lazylazy'
    });

    $('#asc').click(function (event) {
        $con.isotope({
            sortAscending: true,
            sortBy: 'original'
        });
    });

    $('#desc').click(function (event) {
        $con.isotope({
            sortAscending: false,
            sortBy: 'original'
        });
    });

    $('#thin').click(function (event) {
        $con.isotope({
            sortAscending: true,
            filter: 'img[width="333"]',
            sortBy: 'original'
        });
    });

    $('#male_select').click(function (event) {
        $con.isotope({
            sortAscending: true,
            filter: '.male',
            sortBy: 'original'
        });
    });

    $('#all').click(function (event) {
        $con.isotope({
            sortAscending: true,
            filter: '',
            sortBy: 'original'
        });
    });
}

jQuery(document).ready(function ($) {
    downloadContent();

});