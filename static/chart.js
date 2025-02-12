document.addEventListener("DOMContentLoaded", function() {
   var ctx = document.getElementById("expenseChart").getContext("2d");

   var categories = JSON.parse(document.getElementById("categories").textContent);
   var amounts = JSON.parse(document.getElementById("amounts").textContent);

   var chart = new Chart(ctx, {
       type: "pie",
       data: {
           labels: categories,
           datasets: [{
               data: amounts,
               backgroundColor: ["#ff6384", "#36a2eb", "#ffce56", "#66ff66", "#9966ff"],
               hoverOffset: 8
           }]
       },
       options: {
           responsive: true,
           plugins: {
               legend: {
                   position: 'top'
               },
               title: {
                   display: true,
                   text: 'Expense Distribution'
               }
           }
       }
   });
});
