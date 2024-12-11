console.log('jQuery version:', $.fn.jquery); // برای بررسی بارگذاری jQuery

$(document).ready(function() {
    console.log('Document ready, running track_ip script...'); // برای بررسی بارگذاری صفحه

    // نمایش اطلاعات مرورگر و سیستم عامل
    $('#browser-info').text('Browser: ' + navigator.userAgent);
    $('#os-info').text('Platform: ' + navigator.platform);

    // نمایش اطلاعات کشور
    $('#country-info').text('Country: ' + $('#country').val());

    // تنظیم مقادیر فرم برای ارسال اطلاعات
    $('#browserInfo').val(navigator.userAgent);
    $('#osInfo').val(navigator.platform);

    // ارسال اطلاعات فرم به سرور
    $('#trackIpForm').submit(function(event) {
        event.preventDefault();
        $.ajax({
            url: '/submit_track_ip',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                userIp: $('#userIp').val(),
                country: $('#country').val(),
                browserInfo: $('#browserInfo').val(),
                osInfo: $('#osInfo').val()
            }),
            success: function(response) {
                console.log('Track IP data submitted successfully:', response);
            },
            error: function(error) {
                console.log('Error submitting Track IP data:', error);
            }
        });
    });
});
