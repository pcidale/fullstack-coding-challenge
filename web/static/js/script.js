$(document).ready(function() {

    // Submit translation
    $(document.body).on('click', '#submit-btn', function() {
        $.ajax({
            url: '/en-es/translations',
            data: JSON.stringify({'source-text': $('#source-text').val()}),
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(result) {
                window.location.reload(true);
            }
        });
    });

    // Delete Translation
    $(document.body).on('click', '.delete-translation', function(e) {
        if (confirm('Are you sure you want to delete the translation ' + e.target.dataset['uid'] + '?')) {
            $.ajax({
                url: '/en-es/translations/' + e.target.dataset['uid'] + '/',
                type: 'DELETE',
                success: function(result) {
                    if (result['success']) {
                        window.location.replace("/en-es/");
                    }
                }
            });
        }
    });

    // Check for updates
    function check_for_updates() {
        // console.log('checking for updates')
        jQuery.each($('tbody tr[data-status!="translated"]'), function(idx, row) {
            $.ajax({
                url: '/en-es/translations/' + $(row).find('td:first-child()').text() + '/',
                type: 'PATCH',
                success: function(result) {
                    if (result['success']) {
                        if (result['status'] == 'translated') {
                            $('#translation-tb tbody tr[data-status!="translated"]:nth-child(' + String(idx + 1) + ') td:nth-child(2) button').removeClass('btn-light').removeClass('btn-warning').addClass('btn-success').text('translated');
                            $('#translation-tb tbody tr[data-status!="translated"]:nth-child(' + String(idx + 1) + ') td:nth-child(4)').text(result['output_text']);
                            $('#translation-tb tbody tr[data-status!="translated"]:nth-child(' + String(idx + 1) + ')').attr({'data-status': 'translated'})
                            sortTable();
                        } else {
                            $('#translation-tb tbody tr[data-status!="translated"]:nth-child(' + String(idx + 1) + ') td:nth-child(2) button').removeClass('btn-light').addClass('btn-warning').text('pending');
                            $('#translation-tb tbody tr[data-status!="translated"]:nth-child(' + String(idx + 1) + ')').attr({'data-status': 'pending'})
                        };
                    };
                }
            });
        })
    }

    // Check for updates every 10 sec in the next 40 sec
    var refreshIntervalId = setInterval(check_for_updates ,10000);
    setTimeout(function() {
        clearInterval( refreshIntervalId );
    }, 40000);

    // Character counter
    $("#source-text").keyup(function(){
        $("#chr-counter").text("Characters: " + (50 - $(this).val().length));
    });

    // Sort table
    function sortTable() {
        continue_sorting = true;
        // console.log('start sorting');
        while (continue_sorting) {
            continue_sorting = false;
            rows = $('#translation-tb tbody tr');

            jQuery.each(rows, function(idx, row) {
                if (rows[idx + 1]) {
                    if ($(row).find('td:nth-child(4)').text().length > $(rows[idx + 1]).find('td:nth-child(4)').text().length) {
                        $(rows[idx + 1]).after($(row));
                        continue_sorting = true;
                    };
                } else {
                    return false;
                }
            })
        };
    };

});