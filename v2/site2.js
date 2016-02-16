function downloadContent(){
    Papa.parse("csv_dump.csv", {
        download: true,
        dynamicTyping: true,
        header:true,
        skipEmptyLines:true,
        complete: function(results) {

            // Using JSON
            // raw_data = data.result;

            // Parse the imgur urls:
            raw_data = results.data;
            // console.log(raw_data);
            for (var i = 0; i < raw_data.length; i++){
                // console.log(raw_data[i]);
                //console.log(typeof raw_data[i].current_weight_lbs)
                //assert(typeof raw_data[i].current_weight_lbs === 'number', 'Error: Weight is not a number');
                raw_data[i]['photos'] = raw_data[i].photos.split(',');
            }



            // console.log(raw_data);



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

        }
    });
}

jQuery(document).ready(function ($) {
    downloadContent();
    var $win = $(window),
        $imgs = $("img"),
        $con = $('#container').isotope();

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

    $('#all').click(function (event) {
        $con.isotope({
            sortAscending: true,
            filter: '',
            sortBy: 'original'
        });
    });
});