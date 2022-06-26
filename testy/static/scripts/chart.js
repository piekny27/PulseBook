google.charts.load('current', {
  packages: ['corechart']
}).then(function () {

  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'Day');
  data.addColumn('number', "Saturation");
  data.addColumn('number', "Pulse");
  
  var obj = JSON.parse(dict);
  console.log(obj)
  for(var i=0; i<obj.length;i++)
  {
    data.addRows([
      [new Date(obj[i].date),
      obj[i].hr_val,
      obj[i].sp_val]
    ]);
  }
  

var options = {
  legend: {
    maxLines: 2,
    position: 'top'
  },
  width: 500
};

var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
chart.draw(data, options);
});

