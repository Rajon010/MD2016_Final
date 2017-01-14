import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 %s <input>' % sys.argv[0])
        exit(1)
    input_name = sys.argv[1]
    
    with open(input_name, 'r') as input_file, open('index.html', 'w') as output_file:
        output_file.write(
'''<!DOCTYPE html>
<html>
	<head>
		<title>Machine Discovery Demo</title>
		<meta charset="utf-8">
		<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
		<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
		<script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	</head>

	<body>''')
        lines = list(map(str.rstrip, input_file.readlines()))
        assert len(lines) % 7 == 0
        indices = lines[::7]
        pic_origin = lines[1::7]
        mid_origin = lines[2::7]
        pic_bad = lines[3::7]
        mid_bad = lines[4::7]
        pic_good = lines[5::7]
        mid_good = lines[6::7]
        

        # output_file.write('\t\t<div class="jumbotron">\n')
        for i in range(len(lines) // 7):
            output_file.write(
            '''
		<div class="panel panel-primary">
			<div class="panel-heading">
				<h1 class="panel-title">%s</h1>
			</div>
			<div class="panel-body">
''' % indices[i])
            
            # output_file.write('\t\t\t<h1>%s</h1>\n' % indices[i])
            output_file.write('\t\t\t\t<h3>Original input sheet (<a href="%s">midi</a>)</h3><br>\n' % mid_origin[i])
            output_file.write('\t\t\t\t<img src="%s"><hr>\n' % pic_origin[i])
            output_file.write('\t\t\t\t<h3>Naive output sheet (<a href="%s">midi</a>)</h3><br>\n' % mid_bad[i])
            output_file.write('\t\t\t\t<img src="%s"><hr>\n' % pic_bad[i])
            output_file.write('\t\t\t\t<h3>Better output sheet (<a href="%s">midi</a>)</h3><br>\n' % mid_good[i])
            output_file.write('\t\t\t\t<img src="%s"><hr>' % pic_good[i])

            output_file.write('''
			</div>
		</div>
''')
        # output_file.write('\t\t</div>\n')
        output_file.write(
'''	</body>
</html>''')
