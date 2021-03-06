from django.shortcuts import render
from mentor.counter.models import Counter 
from datetime import date, datetime, timedelta 
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.timezone import localtime

from django.contrib.admin.views.decorators import staff_member_required
from mentor.utils import UnicodeWriter
from mentor.questionaire.forms import DownloadResponseForm
# Create your views here.

def goto(request, url=None):

	if url:

		counter = Counter(url=url)
		counter.save()
		# import pdb; pdb.set_trace();
		return HttpResponseRedirect(url)
	else:
		raise Http404()

@staff_member_required
def report(request):
	"""
	This report view is to report a csv file contains all the counter data
	Only can viewed by staff members
	"""
	title = " Click-through Data "
	if request.POST:
		form = DownloadResponseForm(request.POST)
		if form.is_valid():
			start_date = form.cleaned_data['start_date']
			end_date = form.cleaned_data['end_date'] + timedelta(days=1)

			counters = list(Counter.objects.filter(timestamp__lt=end_date,timestamp__gte=start_date))
			timestamp = datetime.today()
			filename = "Report Click-through data at " + timestamp.strftime("%Y-%m-%d %H:%M:%S") + " from " + start_date.strftime("%Y-%m-%d") + " to " + end_date.strftime("%Y-%m-%d")

			http_response = HttpResponse()
			http_response = HttpResponse(content_type='text/csv')
			http_response['Content-Disposition'] = 'attachment; filename="%s.csv"' % (filename)

			writer = UnicodeWriter(http_response)
			header = ["url", "timestamp"]
			writer.writerow(header)
			
			for counter in counters:
				csv_row = []
				csv_row.append(counter.url)
				csv_row.append(localtime(counter.timestamp).strftime("%Y-%m-%d %H:%M:%S"))
	
				writer.writerow(csv_row)

			return http_response
	else:
		form = DownloadResponseForm()

	return render(request, "admin/download_csv.html", {
		"form" : form,
		"title" : title,
	})
