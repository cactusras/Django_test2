function submitDoctorForm() {
    var formData = new FormData($('#doctorForm')[0]);
    $.ajax({
        type: 'POST',
        url: '/doc_uploading/',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.status === 'success') {
                $('#step1').hide();
                $('#step2').show();
            } else {
                alert(response.message);
            }
        }
    });
}

function submitExpertiseForm() {
    var expertise = $('#expertise').val();
    $.ajax({
        type: 'POST',
        url: '/doc_exp_uploading/',
        data: JSON.stringify({'expertise': expertise}),
        contentType: 'application/json',
        success: function(response) {
            if (response.status === 'success') {
                $('#step2').hide();
                $('#step3').show();
            } else {
                alert(response.message);
            }
        }
    });
}

function submitWorkingHourForm() {
    var formData = $('#workingHourForm').serialize();
    $.ajax({
        type: 'POST',
        url: '/workinghour_upload/',
        data: formData,
        success: function(response) {
            if (response.status === 'success') {
                $('#step3').hide();
                $('#step4').show();
            } else {
                alert(response.message);
            }
        }
    });
}

function submitSchedulingForm() {
    var formData = {
        'StartDate': $('#StartDate').val(),
        'EndDate': $('#EndDate').val()
    };
    $.ajax({
        type: 'POST',
        url: '/scheduling_upload/',
        data: JSON.stringify(formData),
        contentType: 'application/json',
        success: function(response) {
            if (response.status === 'success') {
                $('#step4').hide();
                $('#result').show();
                fetchSessionData();
            } else {
                alert(response.message);
            }
        }
    });
}

function fetchSessionData() {
    $.ajax({
        type: 'GET',
        url: '/doc_session/',
        success: function(response) {
            $('#responseData').text(JSON.stringify(response, null, 2));
        }
    });
}
