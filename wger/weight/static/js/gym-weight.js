/*
 This file is part of wger Workout Manager.

 wger Workout Manager is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 wger Workout Manager is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 */
'use strict';

$(document).ready(function () {
    var url;
    var ourParams;
    var weightChart;
    weightChart = {};
  $("#main_member_list input[type='checkbox']").change(function() {
    if ($( "input:checked" ).length == 2){
      $('#compareButton').prop('disabled', false)
    }else{
      $('#compareButton').prop('disabled', true)
    }
  });
  $("#compareButton").click(function (){

    setTimeout(() => {
      var checkedUsers = $('#main_member_list input[type=\'checkbox\']');
      url = '/weight/api/compare_weight_data/';
      var x = 0;
      var chartName;
      checkedUsers.each((index)=>{
        var gymId = $(checkedUsers[index]).data('gym');
        chartName = $(checkedUsers[index]).attr('value')
        if (checkedUsers[index].checked){
          if (x == 0){
            url += gymId+'/'+chartName;
            x++;
          }else
            url += '/'+chartName
        
        } // end of if checked
      });
      d3.json(url, function (json) {
        for(let key in json){
          var ourParams = {
            animate_on_load: true,
            full_width: true,
            top: 10,
            left: 30,
            right: 10,
            show_secondary_x_label: true,
            xax_count: 10,
            target: '#chart-'+key,
            x_accessor: 'date',
            y_accessor: 'weight',
            min_y_from_data: true,
            colors: ['#3465a4']
          }
          var data;
          if (Object.keys(json).length) {
            $('#weight_diagram').append("<div id=chart-"+key+"><h2>"+key+"</h2></div>");
            data = MG.convert.date(json[key], 'date');
            weightChart.data = data;
            // Plot the data
            ourParams.data = data;
            MG.data_graphic(ourParams);
          }
        }
      });
    }, 500);
  });

});

