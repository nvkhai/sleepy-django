#!/usr/bin/env python

# Copyright (C) 2008 Panos Laganakos <panos.laganakos@gmail.com>
#	 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#	 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#	 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from string import Template
from optparse import OptionParser
try:
	from django.conf import settings
except ImportError:
	print 'Cancelled:\n\tYou need Django 0.96 or greater to use this script.'


site_settings = {}
project_structure = ['website', 'templates', 'static']
settings_template = Template('''DEBUG = True
TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
	'$dir',
)
''')


def _make_page(template, output_dir=''):
	from django.shortcuts import render_to_response
	from django.template import TemplateDoesNotExist
	print template
	try:
		rsp = render_to_response(template)
	except TemplateDoesNotExist, e:
		print 'Error: template %s does not exist' % e,
		return
	template_name = locals()['template']
	if output_dir == '':
		page = file(template_name+'_output.html', 'w')
	else:
		page = file(output_dir+'/'+template_name, 'w')
	page.write(rsp.content)
	page.close()

def _make_pages(template_dir, output_dir, recursive=True):
	try:
		for template in os.listdir(template_dir):
			if not template.startswith('.') and not os.path.isdir(os.path.join(template_dir, template)):
				_make_page(template, output_dir)
			if os.path.isdir(os.path.join(template_dir, template)):
				#print os.path.join(template_dir, template)
				_make_pages(os.path.join(template_dir, template), output_dir)
	except OSError, e:
		print 'Error: %s' % (e,)

def _start_project(name):
	cur_dir = os.path.abspath(os.path.curdir)
	project_dir = os.path.join(cur_dir, name)
	try:
		os.mkdir(project_dir)
	except OSError:
		print 'Directory \'%s\' already exists.' % (project_dir,)
		return
	[os.mkdir(os.path.join(project_dir, directory)) for directory in project_structure]
	settings_content = settings_template.substitute(dir=os.path.join(project_dir, 'templates'))
	settings_file = file(os.path.join(project_dir, 'settings.py'), 'w')
	settings_file.write(settings_content)
	settings_file.close()

def make_html_callback(option, opt_str, value, parser):
	try:
		_make_pages(site_settings['TEMPLATE_DIRS'][0],
			os.path.join(os.path.abspath(os.path.curdir), 'website'))
	except KeyError:
		print 'Error: No settings.py available. Try running sleepy.py from within your project dir.'

def start_project_callback(option, opt_str, value, parser):
	_start_project(name=value)

def run_server_callback(option, opt_srt, value, parser):
	pass

def main():
	try:
		execfile(os.path.join(os.path.curdir, 'settings.py'), {}, site_settings)
		settings.configure(**site_settings)
	except:
		pass
	if len(sys.argv) < 2:
		print 'Type sleepy.py --help'
	parser = OptionParser()
	parser.add_option('--make', action='callback', callback=make_html_callback)
	parser.add_option('--startproject', action='callback', callback=start_project_callback,
		type='string', dest='name', help='start a new project NAME')
	(options, args) = parser.parse_args()


if __name__ == '__main__':
	main()
