// Example JavaScript to add interactivity (if needed)

// Example: Toggle input fields based on dropdown selection
document.getElementById('account_type').addEventListener('change', function () {
    var semesterField = document.getElementById('semester');
    var labField = document.getElementById('lab_code');
    
    if (this.value === 'course') {
        semesterField.parentElement.style.display = 'block';
        labField.parentElement.style.display = 'none';
    } else {
        semesterField.parentElement.style.display = 'none';
        labField.parentElement.style.display = 'block';
    }
});
