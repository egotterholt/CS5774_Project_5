$(document).ready(function () {

    // Left arrow clicked
    leftArrowClick();

    // Right arrow clicked
    rightArrowClick();

    // Search method
    searchResults();

    // Rental notice
    var active = false;
    rentalNotice(active);

    deleteWarning();

});

// When left home button is clicked, cycle through the options
function leftArrowClick() {
    $('#left-arrow').click(function () {
        const newItemMsg = $(this).siblings('div.item-box').eq(0).clone();

        $(newItemMsg).insertBefore( $(this).siblings("h1:last") ).fadeIn(3000, function () {
            $(this).siblings('div.item-box').eq(0).remove();
        });

        console.log("Left arrow button clicked...");
    });
}

// When right arrow button on the home screen is clicked, cycle through the options
function rightArrowClick() {
    $('#right-arrow').click(function () {
        const newItemMsg = $(this).siblings('div.item-box').eq(2).clone();

        $(newItemMsg).insertAfter($(this).siblings("h1:first")).fadeIn(3000, function () {
            $(this).siblings('div.item-box').eq(2).remove();
        });

        console.log("Right arrow button clicked...");
    });
}

// Display no results page if search does not match expected input, or result for specific item
function searchResults() {
    // Take in query string
    var queryString = window.location.search;

    // Pass query string to url params to extract keyword
    var urlParams = new URLSearchParams(queryString);

    // Read search string and return resultant page
    if (urlParams.has('search-items')) {
        var keyword = urlParams.get("search-items");

        // Update page title for search
        var newSearchTitle = "Search Results for \"" + keyword + "\"";
        $('#home-content h1').text(newSearchTitle);

        var itemResults =
            `<div class="item-box">
                <h3 class="item-title">Weed Eater</h3>
                <img src="./img/weedeater.png" alt="Item Photo"><!-- Check README for photo credits -->
                <p class="item-period">5-day rental</p>
                <a href="./item.html" class="item-cost">$25</a>
            </div><!-- #item-box -->`;
        var noItemResults = '<h3>No results for "' + keyword + '", please try another search</h3>';

        // If keyword matches expected values, print good alert
        if (keyword.toLowerCase() == ('Weed Eater').toLowerCase()) {
            $('div#items').append(itemResults);
        } else {
            $('div#items').append(noItemResults);
        }
    }
}

// When the rent button is clicked on an item page, display popup information
function rentalNotice(active) {
    $('div#rental-options input[type="submit"]').click(function () {
        // var className = $(this).attr('class');
        // var ownerRating = $(this).parent().siblings('#ratings').children('h3:first').text();
        // var ownerName = ownerRating.slice(0, ownerRating.indexOf('\''));
        //
        // if (!active) {
        //     active = true;
        //     if (className != 'disabled') {
        //         var rentalMsg = '<p>Renting from ' + ownerName + '</p>';
        //         $(this).addClass('disabled');
        //         $(rentalMsg).appendTo($(this).parent().parent()).fadeOut(3000, function () {
        //             $(rentalMsg).remove();
        //             active = false;
        //         });
        //     } else {
        //         var disabledMsg = '<p>Already renting from ' + ownerName + '</p>';
        //         $(disabledMsg).appendTo($(this).parent().parent()).fadeOut(3000, function () {
        //             $(disabledMsg).remove();
        //             active = false;
        //         });
        //     }
        // }


        var item_id = $(this).attr('data-item-id');
        var owner = $(this).attr('data-item-owner');
        var rented_by = $(this).attr('data-item-rented-by');
        var ajax_url = $(this).attr('data-ajax-url');

        // Using the core $.ajax() method
        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                item_id: item_id,
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType : "json",

            headers: {'X-CSRFToken': csrftoken},

            context: this
        })
        // Code to run if the request succeeds (is done);
        // The response is passed to the function
        .done(function( json ) {
            // alert("Request received successfully");
            if (json.success === 'success') {
                var className = $(this).attr('class');

                if (!active) {
                    active = true;
                    if (className !== 'disabled') {
                        var rentalMsg = '<p>Now renting from ' + owner + '</p>';
                        $(this).addClass('disabled');
                        $(rentalMsg).appendTo($(this).parent().parent()).fadeOut(5000, function () {
                            $(rentalMsg).remove();
                            active = false;
                        });
                        // alert("Now renting from " + owner )
                    } else {
                        var disabledMsg = '<p>Already renting from ' + owner + '</p>';
                        $(disabledMsg).appendTo($(this).parent().parent()).fadeOut(5000, function () {
                            $(disabledMsg).remove();
                            active = false;
                        });
                        // alert("Already renting from " + owner )
                    }
                }
            } else {
                alert("Error: " + json.error);
            }
        })
        // Code to run if the request fails; the raw request and
        // status codes are passed to the function
        .fail(function( xhr, status, errorThrown ) {
            alert( "Sorry, there was a problem!" );
            // console.log( "Error: " + errorThrown );
            // console.log( "Status: " + status );
            // console.dir( xhr );
        })
        // Code to run regardless of success or failure;
        .always(function( xhr, status ) {
            // alert( "The request is complete!" );
        });

    })
}

// Confirmation browser popup window to prevent accidental deletion by an administrator
function deleteWarning() {
    $('input[type="submit"]#account-item-delete').click(function (event) {
        if (confirm('Warning: Are you sure you want to delete this item?')) {
            alert("Successfully deleted item");
        } else {
            event.preventDefault();
            alert("Successfully cancelled item deletion");
        }
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');