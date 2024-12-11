console.log('jQuery version:', $.fn.jquery); // برای بررسی بارگذاری jQuery

function loadLogs() {
    console.log('Loading logs...'); // برای بررسی فراخوانی تابع
    $.ajax({
        url: '/logs',
        method: 'GET',
        success: function(data) {
            console.log('Logs data:', data); // برای بررسی داده‌های دریافتی
            var tableBody = $('#logTableBody');
            tableBody.empty();
            data.logs.forEach(function(log) {
                var row = $('<tr></tr>');
                row.append('<td>' + log.ip + '</td>');
                row.append('<td>' + log.user_agent + '</td>');
                row.append('<td>' + log.browser_name + '</td>');
                row.append('<td>' + log.platform + '</td>');
                row.append('<td>' + log.country + '</td>');

                var moduleSelector = $('<select multiple class="form-control" data-log-id="' + log.id + '"></select>');
                $.ajax({
                    url: '/get_modules',
                    method: 'GET',
                    success: function(modulesData) {
                        console.log('Modules data:', modulesData); // برای بررسی داده‌های ماژول
                        modulesData.modules.forEach(function(module) {
                            var option = $('<option value="' + module.id + '">' + module.name + '</option>');
                            moduleSelector.append(option);
                        });

                        // انتخاب ماژول‌های اختصاص داده شده
                        $.ajax({
                            url: '/get_assigned_modules/' + log.id,
                            method: 'GET',
                            success: function(assignedModules) {
                                console.log('Assigned modules:', assignedModules); // برای بررسی داده‌های اختصاص داده شده
                                assignedModules.forEach(function(moduleId) {
                                    moduleSelector.find('option[value="' + moduleId + '"]').prop('selected', true);
                                });
                            }
                        });
                    }
                });
                row.append($('<td></td>').append(moduleSelector));

                // اضافه کردن دکمه حذف برای هر لاگ
                row.append('<td><button class="btn btn-danger" onclick="deleteLog(' + log.id + ')">Delete</button></td>');

                tableBody.append(row);
            });
        }
    });
}

function saveAssignments() {
    console.log('Saving assignments...'); // برای بررسی فراخوانی تابع
    var assignments = [];
    $('#logTableBody select').each(function() {
        var logId = $(this).data('log-id');
        var selectedModuleIds = $(this).val() || [];
        assignments.push({ logId: logId, moduleIds: selectedModuleIds });
    });

    $.ajax({
        url: '/assign_modules',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(assignments),
        success: function(response) {
            console.log('Save response:', response); // برای بررسی پاسخ سرور
            if (response.success) {
                console.log("Assignments saved successfully.");
                $('#successMessage').show().delay(3000).fadeOut();
            } else {
                console.log("Duplicate log detected, not saved.");
                $('#errorMessage').text(response.message).show().delay(3000).fadeOut();
            }
        }
    });
}

// تابع حذف لاگ
function deleteLog(logId) {
    console.log('Deleting log...', logId); // برای بررسی فراخوانی تابع
    $.ajax({
        url: '/delete_log/' + logId,
        method: 'POST',
        success: function() {
            loadLogs();
        }
    });
}

$(document).ready(function() {
    console.log('Document ready, loading logs...'); // برای بررسی بارگذاری صفحه
    loadLogs();

    $('#saveAssignments').click(function() {
        saveAssignments();
    });

    // به روزرسانی هر 10 ثانیه
    setInterval(loadLogs, 10000);
});
