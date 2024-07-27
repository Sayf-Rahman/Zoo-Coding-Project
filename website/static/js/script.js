var endDate = new Date();
endDate.setFullYear(endDate.getFullYear() + 1, 11, 31); 

flatpickr("#availability-calendar", {
  inline: true,
  dateFormat: "Y-m-d",
  minDate: "today",
  maxDate: endDate,
  onChange: function(selectedDates, dateStr) {
    // updates the selected date box when a customer chooses their desired date
    document.getElementById("selected-date").innerHTML = "Selected Date: " + dateStr;
  }
});
