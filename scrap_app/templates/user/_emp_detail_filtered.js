$('div#emptable').html('{% filter escapejs %}{{ html }}{% endfilter %}');
$('div#emptable').show();