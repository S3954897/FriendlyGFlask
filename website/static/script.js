

$(document).ready(function() {
  // get the element to be refreshed
  const element = $('#myTable');

  // set the interval to refresh the element
  setInterval(() => {
    // make an AJAX request to get the latest value of item1
    $.ajax({
      url: '/display',
      type: 'GET',
      success: function(data) {
        // update the content of the element with the new value
        element.text(data.item1);
      }
    });
  }, 5000); // refresh every 5 seconds
});



