console.log('jQuery version:', $.fn.jquery); // برای بررسی بارگذاری jQuery

// دریافت لیست ماژول‌ها
function loadModules() {
    console.log('Loading modules...'); // برای بررسی فراخوانی تابع
    $.ajax({
        url: '/get_modules',
        method: 'GET',
        success: function(data) {
            console.log('Modules data:', data); // برای بررسی داده‌های دریافتی
            var tableBody = $('#moduleTableBody');
            tableBody.empty();
            data.modules.forEach(function(module) {
                var row = $('<tr></tr>');
                row.append('<td>' + module.name + '</td>');
                row.append('<td><button class="btn btn-danger" onclick="deleteModule(' + module.id + ')">Delete</button></td>');
                tableBody.append(row);
            });
        }
    });
}

// حذف ماژول
function deleteModule(moduleId) {
    console.log('Deleting module...', moduleId); // برای بررسی فراخوانی تابع
    $.ajax({
        url: '/delete_module/' + moduleId,
        method: 'POST',
        success: function() {
            loadModules();
        }
    });
}

$(document).ready(function() {
    console.log('Document ready, loading modules...'); // برای بررسی بارگذاری صفحه
    loadModules();
    $('#moduleForm').submit(function(event) {
        event.preventDefault();
        var moduleName = $('#moduleName').val();
        var moduleCode = $('#moduleCode').val();
        $.ajax({
            url: '/save_module',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ name: moduleName, code: moduleCode }),
            success: function() {
                loadModules();
                $('#moduleForm')[0].reset();
            }
        });
    });
});
