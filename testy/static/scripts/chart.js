
google.charts.load('current', {
  packages: ['corechart']
}).then(function () {

  var data = new google.visualization.DataTable();
  data.addColumn('date', 'Day');
  data.addColumn('number', "Saturation");
  data.addColumn('number', "Pulse");
  
  var a= dict;
  console.log(dict);
  var obj = JSON.parse(dict);
  console.log(obj.bmi_message);
  data.addRows([
    [new Date(2014, 0),  -.5,  5.7],
    [new Date(2014, 1),   .4,  8.7],
    [new Date(2014, 2),   .5,   12],
    [new Date(2014, 3),  2.9, 15.3],
    [new Date(2014, 4),  6.3, 18.6],
    [new Date(2014, 5),    9, 20.9],
    [new Date(2014, 6), 10.6, 19.8],
    [new Date(2014, 7), 10.3, 16.6],
    [new Date(2014, 8),  7.4, 13.3],
    [new Date(2014, 9),  4.4,  9.9],
    [new Date(2014, 10), 1.1,  6.6],
    [new Date(2014, 11), -.2,  4.5]
  ]);

var options = {
  legend: {
    maxLines: 2,
    position: 'bottom'
  },
  width: 450
};

var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
chart.draw(data, options);
});