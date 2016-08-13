from django.core.management.base import BaseCommand, CommandError
import csv
from reviews.models import Employee

class Command(BaseCommand):

	def add_arguments(self, parser):
		parser.add_argument('csv_file', nargs='+', type=str)

	def handle(self, *args, **options):
		for csv_file in options['csv_file']:
			dataReader = csv.reader(open(csv_file), delimiter=',', quotechar='"')
			for row in dataReader:
				emp = Employee()
				emp.tracking_id = row[0]
				emp.first_name = row[1]
				emp.last_name = row[2]
				emp.email = row[3]
				emp.level = row[4]
				emp.service_area = row[5]
				emp.service_line = row[6]
				emp.office = row[7]
				emp.save()
				self.stdout.write(
					'Created employee {} {}'.format(emp.first_name, emp.last_name)
				)