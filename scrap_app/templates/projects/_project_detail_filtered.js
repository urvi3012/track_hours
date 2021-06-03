$('div#project_table').html('{% filter escapejs %}{{ html }}{% endfilter %}');
$('div#project_table').show();