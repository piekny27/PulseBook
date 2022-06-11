
google.charts.load('current', {
  packages: ['corechart']
}).then(function () {

  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'Day');
  data.addColumn('number', "Saturation");
  data.addColumn('number', "Pulse");
  
  var a= dict;
  console.log(dict);
  var obj = JSON.parse(dict);
  console.log(obj.bmi_message);
  for(var i=0; i<obj.measurements.length;i++)
  {
    data.addRows([
      [new Date(obj.measurements[i].date),
      obj.measurements[i].hr_val,
      obj.measurements[i].sp_val]
    ]);
  }
  

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