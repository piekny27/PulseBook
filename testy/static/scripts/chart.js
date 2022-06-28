google.charts.load('current', {
  packages: ['corechart']
}).then(function () {

  var data = new google.visualization.DataTable();
  var date_formatter = new google.visualization.DateFormat({ 
    pattern: "dd MMM YYYY, HH:mm"
  });
  var formatSat = new google.visualization.NumberFormat({
    suffix: ' %'
  });
  var formatPul = new google.visualization.NumberFormat({
    suffix: ' bpm',
    pattern:'#0'
  });

  data.addColumn('datetime', 'Day');
  data.addColumn('number', "Saturation");
  data.addColumn('number', "Pulse");
  
  var obj = JSON.parse(dict);
  //console.log(obj)
  for(var i=0; i<obj.length;i++)
  {
    data.addRows([
      [new Date(obj[i].date),
      obj[i].hr_val,
      obj[i].sp_val]
    ]);
  }

  date_formatter.format(data, 0);
  formatSat.format(data, 1)
  formatPul.format(data, 2)

var options = {
  legend: {
    maxLines: 2,
    position: 'top',
    alignment: 'center'
  },
  chartArea:{top:20,width:"100%",height:150},
  width:'100%',
  animation: {
    duration: 1000,
    easing: 'out',
    startup: true
  },
  hAxis: {
    format: 'dd/MM'
  },
  //pointsVisible: true
};

var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
chart.draw(data, options);
});

